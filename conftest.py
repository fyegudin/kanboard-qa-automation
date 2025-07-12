import os

import pytest
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

from config.config import Config
from utilities.database import Database

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(autouse=True)
def setup_logging():
    # Get the absolute path to the directory containing this conftest.py file.
    project_root = Path(__file__).parent.resolve()

    # Define the logs directory as a subdirectory of the project root
    log_dir = project_root / "logs"

    # Define the full path to the log file
    log_file_path = log_dir / "test_execution.log"

    # Create the logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path), # Use the absolute path here
            logging.StreamHandler()
        ],
        force=True
    )

@pytest.fixture
def page(playwright):
    browser = playwright.chromium.launch(
        headless=False if os.getenv("HEADFUL") == "True" else True,
        channel="chrome",  # Uses Chrome instead of Chromium
        args=["--start-maximized"],
        slow_mo=1000
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    yield page
    context.close()
    browser.close()

@pytest.fixture
def db_connection():
    db = Database()
    yield db
    db.close()

@pytest.fixture
def login(page):
    from pages.login_page import LoginPage
    login_page = LoginPage(page)
    login_page.navigate(Config.APP_URL)
    login_page.login(Config.ADMIN_USER, Config.ADMIN_PASSWORD)
    yield