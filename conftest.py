import pytest
import os
import platform
import allure
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.config import Config
from utils.logger import logger


def pytest_addoption(parser):
    """
    Add command line options to pytest
    """
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests (chrome or firefox)")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run browser in headless mode")


@pytest.fixture(scope="session")
def browser(request):
    """
    Return the browser name from command line option or default
    """
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request):
    """
    Return the headless flag from command line option or default
    """
    return request.config.getoption("--headless")


@pytest.fixture
def driver(browser, headless):
    """
    Setup WebDriver instance before test and teardown after test

    :param browser: Browser to use
    :param headless: Whether to run in headless mode
    :return: WebDriver instance
    """
    # Set environment variables based on fixture params
    os.environ["BROWSER"] = browser
    os.environ["HEADLESS"] = str(headless).lower()

    # Initialize WebDriver based on browser type
    try:
        if browser.lower() == "chrome":
            options = Config.get_browser_options("chrome")

            # On Windows, we need to handle WebDriver initialization differently
            if platform.system() == "Windows":
                driver = webdriver.Chrome(options=options)
            else:
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        elif browser.lower() == "firefox":
            options = Config.get_browser_options("firefox")

            # On Windows, we need to handle WebDriver initialization differently
            if platform.system() == "Windows":
                driver = webdriver.Firefox(options=options)
            else:
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {str(e)}")

        # Try alternative initialization method as fallback
        if browser.lower() == "chrome":
            driver = webdriver.Chrome()
        elif browser.lower() == "firefox":
            driver = webdriver.Firefox()
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    # Set implicit wait
    driver.implicitly_wait(Config.IMPLICIT_WAIT)

    # Maximize window
    driver.maximize_window()

    logger.info(f"Starting WebDriver session with {browser} browser")

    # Return driver for test use
    yield driver

    # Teardown after test
    logger.info("Closing WebDriver session")
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture test outcome and take screenshot on failure
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # If test phase is call, test has finished execution
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")

        # Check if failed (not expected) or passed unexpectedly
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Get the fixture
            fixture_driver = item.funcargs.get("driver", None)

            # Take screenshot if driver is available
            if fixture_driver:
                take_screenshot(fixture_driver, item.nodeid)


def take_screenshot(driver, node_id):
    """
    Take screenshot and attach to Allure report

    :param driver: WebDriver instance
    :param node_id: Test node ID
    """
    # Create screenshots directory if it doesn't exist
    if not os.path.exists(Config.SCREENSHOT_DIR):
        os.makedirs(Config.SCREENSHOT_DIR)

    # Generate unique screenshot filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_name = node_id.split("::")[-1]
    screenshot_path = f"{Config.SCREENSHOT_DIR}/{test_name}_{timestamp}.png"

    # Take screenshot
    driver.save_screenshot(screenshot_path)
    logger.info(f"Screenshot saved to {screenshot_path}")

    # Attach screenshot to Allure report
    allure.attach.file(
        screenshot_path,
        name=f"Screenshot_{test_name}",
        attachment_type=allure.attachment_type.PNG
    )