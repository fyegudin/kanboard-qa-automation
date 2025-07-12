import os

import pytest
import logging
from playwright.sync_api import sync_playwright

from config.config import Config
from utilities.database import Database

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("test_execution.log"),
            logging.StreamHandler()
        ]
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