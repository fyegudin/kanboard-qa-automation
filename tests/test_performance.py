import pytest
import allure
from utilities.helpers import generate_task_title, generate_project_name, generate_description, measure_execution_time
from utilities.constants import NUM_TASKS_FOR_PERFORMANCE


@allure.feature("Performance Testing")
class TestPerformance:
    @pytest.mark.usefixtures("login")
    def test_task_retrieval_performance(self, page, db_connection):
        num_tasks = NUM_TASKS_FOR_PERFORMANCE
        project_name = generate_project_name()
        task_description = generate_description()
        task_titles = [generate_task_title() for _ in range(num_tasks)]

        with allure.step("Create project and tasks"):
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

            for title in task_titles:
                task_page.create_task(title, task_description)

        @measure_execution_time("Initial task count retrieval from DB", time_expected=1.0)
        @allure.step("Measure database retrieval time")
        def get_initial_task_count(db_conn, proj_id):
            query = "SELECT COUNT(*) FROM tasks WHERE project_id = %s"
            return db_conn.fetch_one(query, (proj_id,))[0]

        initial_count = get_initial_task_count(db_connection, project_id)
        assert initial_count == num_tasks, f"Expected 1 task in DB for project_id {project_id}, but found {initial_count}"

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