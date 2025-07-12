from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from utilities.constants import SMALL_TIMEOUT
import allure


class ProjectPage(BasePage):
    class ProjectPage(BasePage):
        """
        Page object for the Kanboard Project Management functionalities.
        """

    def __init__(self, page: Page):
        super().__init__(page)
        # Define locators specific to the Project Page
        self.new_project_button = page.get_by_role("link", name="New project")
        self.project_name_input = page.locator("#form-name")
        self.project_identifier_input = page.locator("#form-identifier")
        self.save_button = page.get_by_role("button", name="Save")
        self.cancel_button = page.get_by_role("link", name="cancel")
        self.remove_link = page.get_by_role("link", name="Remove")
        self.confirm_remove_link = page.get_by_role("button", name="Yes")
        self.configure_project_label = page.get_by_label("Configure this project")
        self.manage_projects_link = page.get_by_role("link", name="Manage projects")
        self.project_row = page.get_by_role("link", name="#33 ")
        self.configure_project_link = page.get_by_role("link", name="Configure this project")

    def create_project(self, name: str):
        """
        Creates a new project with the given name.
        """
        with allure.step(f"Creating project: '{name}'"):  # Add an Allure step for the entire action
            self.click(self.new_project_button, locator_description="New project button")
            self.fill(self.project_name_input, name, locator_description="Project name input")
            self.click(self.save_button, locator_description="Save button")
            # For dynamic elements like a project name appearing, we can create the locator here
            project_name_on_list = self.page.get_by_text(name)
            self.wait_for_locator(project_name_on_list, locator_description=f"Project '{name}' in list")
            expect(project_name_on_list).to_be_visible()

    @allure.step("Deleting project: '{project_id}'")
    def delete_project(self, project_id: int):
        """
        Navigates to the project list, finds the project, clicks delete,
        and confirms the deletion.
        """
        # 1. Navigate to the projects management page (if not already there)
        self.navigate_to_projects_management()

        # 2. Find the project row and click its delete action
        project_row = self.page.get_by_role("link", name=f"#{project_id} ")
        self.click(project_row, locator_description=f"Project row for project ID '{project_id}'")
        self.click(self.configure_project_link,
                   locator_description=f"Configure project link for project ID '{project_id}'")

        self.click(self.remove_link, locator_description=f"Delete button for project '{project_id}'")

        # 3. Handle the confirmation modal
        self.wait_for_locator(self.confirm_remove_link, locator_description="Confirmation link")
        self.click(self.confirm_remove_link, locator_description="Confirm deletion button")

        # 4. Wait for the project to disappear from the list or for a success message
        expect(project_row).not_to_be_visible(timeout=SMALL_TIMEOUT)

    # You might need this method if your test doesn't start on the projects management page
    @allure.step("Navigating to Projects Management page")
    def navigate_to_projects_management(self):
        # This assumes you have a way to open the user dropdown and click "Projects management"
        self.click(self.configure_project_label, locator_description="User dropdown menu")
        # Click the "Projects management" link
        self.click(self.manage_projects_link, locator_description="Projects management link")
        self.wait_for_url("**/project**")  # Wait for the URL to change to the projects list

    @allure.step("Getting project ID from current URL")
    def get_project_id_from_url(self) -> str | None:
        """
        Retrieves the project ID from the current URL if the page is a project-specific page.
        Assumes URL pattern like /project/{id} or /board/{id}.
        """
        current_url = self.page.url
        import re
        match = re.search(r'/(?:project|board)/(\d+)', current_url)
        if match:
            project_id = match.group(1)
            # self.log_info(f"Extracted project ID '{project_id}' from URL: {current_url}")
            return project_id
        else:
            # self.log_warning(f"Could not extract project ID from URL: {current_url}")
            allure.attach(self.page.screenshot(full_page=True, path=None),
                          name="URL_NoProjectID_Extract",
                          attachment_type=allure.attachment_type.PNG)
            return None
