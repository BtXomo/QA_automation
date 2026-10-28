# Страница логина: локаторы + методы взаимодействия
from playwright.sync_api import Page, Locator
#from config import *

class LoginPage:
    def __init__(self, page:Page):
        self.page = page
        self.input_login_form_username: Locator = page.locator("input[maxlength='254']")
        self.input_login_form_password: Locator = page.locator("input[name='LoginForm[password]']")
        self.span_sign: Locator = page.locator("button span")


    def goto(self, url:str):
        self.page.goto(url)
        print("------------    goto done    -----------")


    def login(self, email:str, password:str):
        self.input_login_form_username.fill(email)
        self.input_login_form_password.fill(password)
        self.span_sign.click()
        print("------------    login done    -------------")