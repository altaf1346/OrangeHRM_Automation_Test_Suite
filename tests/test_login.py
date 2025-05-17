import pytest
import allure
from pages.login_page import LoginPage
from utils.data_reader import DataReader
from utils.logger import logger


@allure.epic("Authentication")
@allure.feature("Login")
class TestLogin:

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test login with valid credentials")
    def test_valid_login(self, driver):
        """
        Test login with valid credentials

        :param driver: WebDriver fixture
        """
        logger.info("Starting valid login test")

        # Get test data
        user_data = DataReader.get_user_data()["valid_users"][0]
        username = user_data["username"]
        password = user_data["password"]

        # Perform login
        login_page = LoginPage(driver)
        login_page.open()

        with allure.step(f"Login with username: {username} and password: {password}"):
            dashboard_page = login_page.login(username, password)

        # Verify login was successful
        with allure.step("Verify user is logged in and dashboard is displayed"):
            assert dashboard_page.is_dashboard_displayed(), "Dashboard page is not displayed after login"

        # Logout
        with allure.step("Logout after successful login"):
            dashboard_page.logout()

        logger.info("Valid login test completed successfully")

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test login with invalid credentials")
    @pytest.mark.parametrize("test_data", DataReader.get_user_data()["invalid_users"])
    def test_invalid_login(self, driver, test_data):
        """
        Test login with invalid credentials

        :param driver: WebDriver fixture
        :param test_data: Test data containing username, password and expected error
        """
        username = test_data["username"]
        password = test_data["password"]
        expected_error = test_data["expected_error"]

        logger.info(f"Starting invalid login test with username: {username}")

        # Perform login with invalid credentials
        login_page = LoginPage(driver)
        login_page.open()

        with allure.step(f"Attempt login with invalid credentials - username: {username}"):
            login_page.login_with_invalid_credentials(username, password)

        # Verify error message
        with allure.step(f"Verify error message contains: {expected_error}"):
            error_message = login_page.get_error_message()
            assert expected_error in error_message, f"Expected error message '{expected_error}' not found in '{error_message}'"

        logger.info("Invalid login test completed successfully")

    @allure.story("Login UI Elements")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Test login page UI elements")
    def test_login_page_ui(self, driver):
        """
        Test login page UI elements

        :param driver: WebDriver fixture
        """
        logger.info("Starting login page UI test")

        login_page = LoginPage(driver)
        login_page.open()

        # Verify logo is displayed
        with allure.step("Verify brand logo is displayed"):
            assert login_page.is_brand_logo_displayed(), "Brand logo is not displayed"

        # Verify forgot password link exists
        with allure.step("Verify forgot password link is available"):
            login_page.click_forgot_password()
            # Here we would verify we're on the forgot password page
            # For now, we'll just navigate back to login page
            login_page.open()

        logger.info("Login page UI test completed successfully")

    @allure.story("Data Driven Login")
    @allure.severity(allure.severity_level.CRITICAL)  # Changed from HIGH to CRITICAL
    @allure.description("Test login with credentials from CSV file")
    def test_login_with_csv_data(self, driver):
        """
        Test login using data from CSV file

        :param driver: WebDriver fixture
        """
        logger.info("Starting data driven login test")

        # Get credentials from CSV
        credentials = DataReader.get_login_credentials()

        for cred in credentials:
            login_page = LoginPage(driver)
            login_page.open()

            username = cred["username"]
            password = cred["password"]
            expected_result = cred["expected_result"]

            with allure.step(f"Login with username: {username}, expected result: {expected_result}"):
                if expected_result == "success":
                    dashboard_page = login_page.login(username, password)
                    assert dashboard_page.is_dashboard_displayed(), "Dashboard page is not displayed after login"
                    dashboard_page.logout()
                else:
                    login_page.login_with_invalid_credentials(username, password)
                    # We should have an error message, but won't check specific message in this test

        logger.info("Data driven login test completed successfully")