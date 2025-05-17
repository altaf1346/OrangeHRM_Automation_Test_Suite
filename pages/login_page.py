from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page object for OrangeHRM Login page
    """
    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, ".orangehrm-login-forgot")
    BRAND_LOGO = (By.CSS_SELECTOR, ".orangehrm-login-branding > img")

    def __init__(self, driver):
        """
        Initialize LoginPage object

        :param driver: WebDriver instance
        """
        super().__init__(driver)
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    def open(self):
        """
        Open the login page
        """
        self.open_url(self.url)
        return self

    def login(self, username, password):
        """
        Perform login with given credentials

        :param username: Username to login with
        :param password: Password to login with
        :return: HomePage object (after successful login)
        """
        self.wait_for_element(self.USERNAME_INPUT)
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

        # Importing locally to avoid circular imports
        from pages.dashboard_page import DashboardPage
        return DashboardPage(self.driver)

    def login_with_invalid_credentials(self, username, password):
        """
        Attempt login with invalid credentials

        :param username: Invalid username
        :param password: Invalid password
        :return: LoginPage object (as login will fail)
        """
        self.wait_for_element(self.USERNAME_INPUT)
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def get_error_message(self):
        """
        Get error message displayed after failed login

        :return: Text of the error message
        """
        self.wait_for_element(self.ERROR_MESSAGE)
        return self.get_text(self.ERROR_MESSAGE)

    def click_forgot_password(self):
        """
        Click on Forgot Password link

        :return: ForgotPasswordPage object
        """
        self.click(self.FORGOT_PASSWORD_LINK)

        # Would normally import and return ForgotPasswordPage
        # For simplicity, just returning self for now
        return self

    def is_brand_logo_displayed(self):
        """
        Check if brand logo is displayed

        :return: Boolean indicating if the logo is displayed
        """
        return self.is_displayed(self.BRAND_LOGO)