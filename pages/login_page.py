from pages.base_page import BasePage
from playwright.sync_api import Page
from utilities.constants import BASE_URL

class LoginPage(BasePage):
    """
      Page object for the Kanboard Login Page.
      """

    def __init__(self, page: Page):
        """
        Initializes the LoginPage with a Playwright Page object and defines its locators.
        """
        super().__init__(page)
        # Define locators as instance variables for clarity and reusability
        self.username_input = page.locator("#form-username")
        self.password_input = page.locator("#form-password")  # Corrected from your previous HTML: id was 'form-password'
        self.remember_me_checkbox = page.get_by_role("checkbox", name="Remember Me")
        self.sign_in_button = page.get_by_role("button", name="Sign in")
        self.forgot_password_link = page.get_by_role("link", name="Forgot password?")

    def login(self, username: str, password: str, remember_me: bool = False):
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        if remember_me:
            self.remember_me_checkbox.check()
        self.click(self.sign_in_button)
        self.wait_for_url(BASE_URL)