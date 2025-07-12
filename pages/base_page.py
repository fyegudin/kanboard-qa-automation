from playwright.sync_api import Page, Locator
from utilities.constants import DEFAULT_TIMEOUT
import allure

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Clicking element: '{locator_description}'")
    def click(self, locator: Locator, locator_description: str = "element"):
        """
        Clicks on a given Playwright Locator.
        Logs the action to Allure.
        """
        try:
            locator.click()
            allure.attach(
                self.page.screenshot(full_page=False, path=None), # Path=None returns bytes
                name=f"Clicked_{locator_description}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            allure.attach(
                self.page.screenshot(full_page=True, path=None),
                name=f"Error_Clicking_{locator_description}",
                attachment_type=allure.attachment_type.PNG
            )
            raise e

    @allure.step("Filling '{locator_description}' with value: '{value}'")
    def fill(self, locator: Locator, value: str, locator_description: str = "input field"):
        """
        Fills a given Playwright Locator with the specified value.
        Logs the action to Allure.
        """
        try:
            locator.fill(value)
            allure.attach(
                self.page.screenshot(full_page=False, path=None),
                name=f"Filled_{locator_description}_with_{value}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            allure.attach(
                self.page.screenshot(full_page=True, path=None),
                name=f"Error_Filling_{locator_description}",
                attachment_type=allure.attachment_type.PNG
            )
            raise e

    @allure.step("Waiting for '{locator_description}' to be visible")
    def wait_for_locator(self, locator: Locator, timeout: int = DEFAULT_TIMEOUT, locator_description: str = "element"):
        """
        Waits for a given Playwright Locator to become visible.
        Logs the action to Allure.
        """
        try:
            locator.wait_for(state="visible", timeout=timeout)
            allure.attach(
                self.page.screenshot(full_page=False, path=None),
                name=f"Waited_for_{locator_description}_visible",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            allure.attach(
                self.page.screenshot(full_page=True, path=None),
                name=f"Error_Waiting_for_{locator_description}_visible",
                attachment_type=allure.attachment_type.PNG
            )
            raise e

    @allure.step("Navigating to URL: '{url}'")
    def navigate(self, url: str):
        """
        Navigates the page to the specified URL.
        Logs the navigation to Allure.
        """
        try:
            self.page.goto(url)
            allure.attach(
                self.page.screenshot(full_page=True, path=None),
                name=f"Navigated_to_{url}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            allure.attach(
                self.page.screenshot(full_page=True, path=None),
                name=f"Error_Navigating_to_{url}",
                attachment_type=allure.attachment_type.PNG
            )
            raise e

    @allure.step("Waiting for URL to match pattern: '{url_pattern}'")
    def wait_for_url(self, url_pattern: str):
        """
        Waits for the page's URL to match a given pattern.
        The pattern can be a string, a regex, or a glob pattern (e.g., '**/dashboard/**').
        Logs the URL waiting action to Allure.
        """
        try:
            self.page.wait_for_url(url_pattern, timeout=DEFAULT_TIMEOUT)
            allure.attach(
                self.page.screenshot(full_page=True, path=None),
                name=f"URL_matched_{url_pattern}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            current_url = self.page.url  # Get current URL for error context
            allure.attach(
                self.page.screenshot(full_page=True, path=None),
                name=f"Error_Waiting_for_URL_{url_pattern}",
                attachment_type=allure.attachment_type.PNG
            )
            raise ValueError(
                f"URL did not match '{url_pattern}' within {DEFAULT_TIMEOUT / 1000} seconds."
                f" Current URL: {current_url}. Error: {e}")