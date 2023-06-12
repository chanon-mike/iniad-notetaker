from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .driver_base import WebDriverBase


class Authentication(WebDriverBase):
    def __init__(self, driver, email, iniad_username, iniad_password):
        super().__init__(driver)
        self.url = 'https://www.google.com/accounts/Login?hl=ja&continue=http://www.google.co.jp/'
        self.email = email
        self.iniad_username = iniad_username
        self.iniad_password = iniad_password

    def login(self):
        self.driver.get(self.url)

        # Go to Google and enter email
        google_email_input = self.wait_for_element_presence(
            By.CSS_SELECTOR, 'input[type="email"][name="identifier"]')
        google_email_input.send_keys(self.email)
        google_email_input.send_keys(Keys.RETURN)

        # Sign in to INIAD authentication for email
        iniad_username_field = self.wait_for_element_presence(
            By.ID, 'username')
        iniad_username_field.send_keys(self.iniad_username)
        iniad_password_field = self.driver.find_element(By.ID, 'password')
        iniad_password_field.send_keys(self.iniad_password)
        self.driver.find_element(
            By.CSS_SELECTOR, 'input.btn.btn-lg.btn-primary.btn-block.btn-uppercase').send_keys(Keys.RETURN)

        # Last step authentication
        authentication_button = self.wait_for_element_presence(
            By.XPATH, '(//button)[1]')
        authentication_button.send_keys(Keys.RETURN)

        # Wait for loading delay before scraping
        self.wait_for_element_presence(By.TAG_NAME, 'img')

    def iniad_login(self):
        # Login after go to MOOCs for the first time
        iniad_login_btn = self.wait_for_element_presence(
            By.CSS_SELECTOR, 'a.btn.btn-lg.btn-info[href="/auth/iniad"]')
        iniad_login_btn.click()
