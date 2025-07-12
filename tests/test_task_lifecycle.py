import pytest
import allure
from playwright.sync_api import expect
from utilities.helpers import generate_project_name, generate_task_title, generate_description


@allure.feature("Task Lifecycle")
class TestTaskLifecycle:
    @pytest.mark.usefixtures("login")
    def test_task_lifecycle(self, page, db_connection):
        project_name = generate_project_name()
        task_title = generate_task_title()
        task_description = generate_description()

        with allure.step("Create project and task"):
            from pages.project_page import ProjectPage
            from pages.task_page import TaskPage
            from pages.project_dashboard_page import ProjectDashboardPage
            project_page = ProjectPage(page)
            task_page = TaskPage(page)
            project_dashboard_page = ProjectDashboardPage(page)

            project_page.create_project(project_name)
            project_id = project_page.get_project_id_from_url()
            assert project_id is not None, f"Failed to get project ID from URL for '{project_name}'"

            project_dashboard_page.navigate_to_board_view(project_id)

            task_page.create_task(task_title,task_description)
            expect(page.get_by_text(task_title)).to_be_visible()

        with allure.step("Verify initial task status"):
            query = "SELECT is_active FROM tasks WHERE title = %s AND project_id = %s"
            result = db_connection.fetch_one(query, (task_title, project_id))
            assert result[0] is True

        with allure.step("Move task to Done and verify status"):
            task_page.move_task_to_done(task_title)
            allure.attach(f"Verifying DB status for task '{task_title}' (project_id: {project_id})",
                          name="DB Verification", attachment_type=allure.attachment_type.TEXT)
            query = "SELECT is_active FROM tasks WHERE title = %s AND project_id = %s"
            result = db_connection.fetch_one(query, (task_title, project_id))

            assert result is not None, f"Task '{task_title}' not found in database for project_id {project_id}"

            # If 'Done' means it's still 'active' but completed
            assert result[0] is True, f"Expected is_active to be True for task '{task_title}', but got {result[0]}"
            allure.attach(f"DB verification successful: is_active is {result[0]}", name="DB Verification Result",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Delete project and verify cleanup"):
            project_page.delete_project(int(project_id))

            # Verify project is deleted
            query = "SELECT COUNT(*) FROM projects WHERE name = %s"
            project_count = db_connection.fetch_one(query, (project_name,))[0]
            assert project_count == 0

            # Verify tasks are deleted
            query = "SELECT COUNT(*) FROM tasks WHERE project_id = %s"
            task_count = db_connection.fetch_one(query, (project_id,))[0]
            assert task_count == 0