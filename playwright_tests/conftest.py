# Фикстуры pytest (создаёт чистый браузерный контекст на каждый тест)
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()
    browse = playwright.chromium.launch(headless=False)
    yield browse
    browse.close()
    playwright.stop()

@pytest.fixture
def page(browser):
    return browser.new_page()