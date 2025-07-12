from playwright.sync_api import Page
from pages.base_page import BasePage
from utilities.constants import BASE_URL, BOARD
import allure

class ProjectDashboardPage(BasePage): # Could be a new page object or part of ProjectPage
    def __init__(self, page: Page):
        super().__init__(page)
        # Using get_by_role is often the most robust:
        self.board_view_link = page.get_by_role("link", name="Board")
        # Alternative:
        # self.board_view_link = page.get_by_text("Board")
        # Alternative:
        # self.board_view_link = page.locator(".view-board")


    @allure.step("Navigating to the project board view")
    def navigate_to_board_view(self, project_id: str):
        """
        Clicks the 'Board' link to switch to the board view.
        """
        self.click(self.board_view_link, locator_description="Board view link")
        # Assuming the URL changes after clicking, you might want to wait for it
        self.wait_for_url(f"{BASE_URL}{BOARD}{project_id}/**")
