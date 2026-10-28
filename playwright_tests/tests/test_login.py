# Авторизация

from pages.login_page import LoginPage
from config import *


def test_login(page):
    login_page = LoginPage(page)
    login_page.goto(BASE_URL)
    login_page.login(EMAIL, PASSWORD)