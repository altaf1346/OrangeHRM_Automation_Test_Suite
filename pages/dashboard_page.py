from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    Page object for OrangeHRM Dashboard page
    """
    # Locators
    DASHBOARD_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb > h6")
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_OPTION = (By.XPATH, "//a[text()='Logout']")
    SIDE_MENU_ITEMS = (By.CSS_SELECTOR, ".oxd-main-menu-item")

    def __init__(self, driver):
        """
        Initialize DashboardPage object

        :param driver: WebDriver instance
        """
        super().__init__(driver)

    def is_dashboard_displayed(self):
        """
        Check if dashboard page is loaded

        :return: Boolean indicating if dashboard is displayed
        """
        try:
            self.wait_for_element(self.DASHBOARD_HEADER)
            return self.get_text(self.DASHBOARD_HEADER) == "Dashboard"
        except:
            return False

    def get_dashboard_title(self):
        """
        Get the title of the dashboard page

        :return: Title text
        """
        self.wait_for_element(self.DASHBOARD_HEADER)
        return self.get_text(self.DASHBOARD_HEADER)

    def logout(self):
        """
        Perform logout action

        :return: LoginPage object
        """
        self.wait_for_element(self.USER_DROPDOWN)
        self.click(self.USER_DROPDOWN)
        self.wait_for_element(self.LOGOUT_OPTION)
        self.click(self.LOGOUT_OPTION)

        # Import locally to avoid circular imports
        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    def navigate_to_menu(self, menu_name):
        """
        Navigate to a specific menu item

        :param menu_name: Name of the menu to navigate to
        :return: Respective page object based on navigation
        """
        menu_locator = (By.XPATH, f"//span[text()='{menu_name}']/parent::a")
        self.wait_for_clickable(menu_locator)
        self.click(menu_locator)

        # Here you would normally return the appropriate page object
        # For simplicity, we'll just return self
        return self