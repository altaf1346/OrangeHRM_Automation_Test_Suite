import os
import json


class Config:
    """
    Configuration class for test settings
    """

    # Base URL for the application
    BASE_URL = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")

    # Browser configuration
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

    # Test timeouts
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))

    # Screenshot settings
    SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "reports/screenshots")

    # Allure report settings
    ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")

    # Default test credentials
    DEFAULT_USERNAME = os.getenv("DEFAULT_USERNAME", "Admin")
    DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD", "admin123")

    @staticmethod
    def get_browser_options(browser_name):
        """
        Get browser-specific options

        :param browser_name: Name of the browser
        :return: Options object for the specified browser
        """
        if browser_name.lower() == "chrome":
            from selenium.webdriver.chrome.options import Options
            options = Options()

            if Config.HEADLESS:
                options.add_argument("--headless")

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")

            return options

        elif browser_name.lower() == "firefox":
            from selenium.webdriver.firefox.options import Options
            options = Options()

            if Config.HEADLESS:
                options.add_argument("--headless")

            return options

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    @staticmethod
    def load_test_data(file_path):
        """
        Load test data from a JSON file

        :param file_path: Path to the JSON file
        :return: Dictionary containing the test data
        """
        with open(file_path, 'r') as file:
            return json.load(file)