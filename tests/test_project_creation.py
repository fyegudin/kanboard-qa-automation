import pytest
import allure
from playwright.sync_api import expect
from utilities.helpers import generate_project_name


@allure.feature("Project Creation")
class TestProjectCreation:
    @pytest.mark.usefixtures("login")
    def test_project_creation(self, page, db_connection):
        project_name = generate_project_name()

        with allure.step("Create project via UI"):
            from pages.project_page import ProjectPage
            project_page = ProjectPage(page)
            project_page.create_project(project_name)
            expect(page.get_by_text(project_name)).to_be_visible()

        with allure.step("Verify project in database"):
            query = "SELECT name, is_active, is_public FROM projects WHERE name = %s"
            result = db_connection.fetch_one(query, (project_name,))
            assert result[0] == project_name
            assert result[1] is True
            assert result[2] is False