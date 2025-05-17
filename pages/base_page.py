from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


class BasePage:
    """
    Base Page class that contains all common methods for page interaction.
    All page classes inherit from this base class.
    """

    def __init__(self, driver):
        """
        Initialize the BasePage with a WebDriver instance

        :param driver: Selenium WebDriver instance
        """
        self.driver = driver

    def open_url(self, url):
        """
        Open a specific URL

        :param url: URL to navigate to
        """
        self.driver.get(url)

    def find_element(self, locator):
        """
        Find a web element using the locator provided

        :param locator: Tuple containing locator strategy and value (e.g. (By.ID, 'username'))
        :return: WebElement object
        """
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        """
        Find multiple web elements using the locator provided

        :param locator: Tuple containing locator strategy and value
        :return: List of WebElement objects
        """
        return self.driver.find_elements(*locator)

    def click(self, locator):
        """
        Click on an element

        :param locator: Tuple containing locator strategy and value
        """
        self.find_element(locator).click()

    def input_text(self, locator, text):
        """
        Input text into a field

        :param locator: Tuple containing locator strategy and value
        :param text: Text to input
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """
        Get text from an element

        :param locator: Tuple containing locator strategy and value
        :return: Text content of the element
        """
        return self.find_element(locator).text

    def is_displayed(self, locator):
        """
        Check if an element is displayed

        :param locator: Tuple containing locator strategy and value
        :return: Boolean indicating if element is displayed
        """
        try:
            return self.find_element(locator).is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def wait_for_element(self, locator, timeout=10):
        """
        Wait for an element to be visible

        :param locator: Tuple containing locator strategy and value
        :param timeout: Time to wait in seconds
        :return: WebElement once it's visible
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(ec.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator, timeout=10):
        """
        Wait for an element to be clickable

        :param locator: Tuple containing locator strategy and value
        :param timeout: Time to wait in seconds
        :return: WebElement once it's clickable
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(ec.element_to_be_clickable(locator))

    def take_screenshot(self, name):
        """
        Take a screenshot

        :param name: Name of the screenshot file
        """
        self.driver.save_screenshot(f"reports/screenshots/{name}.png")