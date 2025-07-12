from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utilities.constants import SMALL_TIMEOUT
import allure

class TaskPage(BasePage):
    """
    Page object for Kanboard Task functionalities.
    """
    def __init__(self, page: Page):
        """
        Initializes the TaskPage with a Playwright Page object and defines its locators.
        """
        super().__init__(page)
        # Define common static locators
        self.add_new_task_link = (page.locator("#board div").filter(has_text="Backlog Hide this column").
                                 locator("div").get_by_role("link"))
        self.task_title_input = page.locator("#form-title")
        self.task_description_textarea = page.get_by_role("textbox", name="Description")
        self.save_button = page.get_by_role("button", name="Save")

    @allure.step("Creating task with title: '{title}' and description: '{description}'")
    def create_task(self, title: str, description: str = ""):
        """
        Creates a new task with the given title and optional description.
        """
        self.click(self.add_new_task_link, locator_description="Add new task link")
        self.fill(self.task_title_input, title, locator_description="Task title input")

        if description:
            self.fill(self.task_description_textarea, description, locator_description="Task description textarea")

        self.click(self.save_button, locator_description="Save task button")

        # Dynamic locator for the created task title on the board
        task_title_on_board = self.page.get_by_text(title)
        self.wait_for_locator(task_title_on_board, locator_description=f"Task '{title}' on board")

    def get_column_locator_by_name(self, column_name: str):
        # Step 1: Find the column header (<th>) that contains the column name
        column_header = self.page.locator(f"th.board-column-header:has(a:text('{column_name}'))")

        # Get the data-column-id from the header
        column_id = column_header.get_attribute("data-column-id")
        if not column_id:
            raise ValueError(f"Could not find data-column-id for column: {column_name}")

        # Step 2: Locate the <td> that corresponds to this column_id
        # Then, crucially, target only the 'expanded' task list div.
        # This will select the *visible* droppable area.
        return self.page.locator(f"td.board-column-{column_id} div.board-task-list.board-column-expanded")

    @allure.step("Moving task '{title}' through workflow columns to 'Done'")
    def move_task_to_done(self, title: str):
        workflow_columns = [
            "Backlog",  # Assuming the initial column, verify this name
            "Ready",
            "Work in progress",
            "Done"
        ]

        for i, column_name in enumerate(workflow_columns):
            # or if the task is already in this column
            if i == 0 and column_name == "Backlog":  # Adjust "Backlog" to your actual starting column
                # Verify task is in the starting column before any moves
                starting_column_locator = self.get_column_locator_by_name(column_name)
                expect(starting_column_locator.get_by_text(title)).to_be_visible(timeout=SMALL_TIMEOUT)
                print(f"Task '{title}' confirmed in starting column '{column_name}'.")
                continue

            with allure.step(f"Step: Moving to '{column_name}'"):
                # Get the source column (the one the task is currently in)
                source_column_name = workflow_columns[
                    i - 1] if i > 0 else "Backlog"  # Adjust if "Backlog" is not always the first
                source_column_locator = self.get_column_locator_by_name(source_column_name)
                source_column_locator.get_by_text(title)

                # Get the target column (the one we want to move the task to)
                target_column_locator = self.get_column_locator_by_name(column_name)

                # Perform the move
                self._move_task_single_step(title, column_name)

                # Assertion to confirm placement in the new column
                task_in_target_column = target_column_locator.get_by_text(title)
                expect(task_in_target_column).to_be_visible(timeout=SMALL_TIMEOUT)

    # Assuming this is your drag and drop method
    def _move_task_single_step(self, task_title: str, target_column_name: str):
        """
        Performs a single drag-and-drop operation for a task.
        This method needs to be robust.
        """
        # Locate the task to drag
        # Find the task title specifically within an active task card
        task_card = self.page.locator(f".task-board-title a:text('{task_title}')").locator("..").locator("..")

        # Locate the target column's droppable area
        target_drop_area = self.get_column_locator_by_name(target_column_name)

        expect(task_card).to_be_visible(timeout=SMALL_TIMEOUT)  # Ensure the task is visible before dragging
        expect(target_drop_area).to_be_visible(timeout=SMALL_TIMEOUT)  # Ensure the target is visible

        # Perform the drag-and-drop operation
        task_card.drag_to(target_drop_area)

