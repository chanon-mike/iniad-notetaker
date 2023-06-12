
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class WebDriverBase:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element_presence(self, by, value):
        # Wait for website loading delay until it presence
        try:
            wait_element = self.wait.until(EC.presence_of_element_located(
                (by, value)))
            return wait_element
        except TimeoutException:
            print("Timeout occurred. Element didn't appear within the specified timeout.")

    def wait_for_element_clickable(self, by, value):
        # Wait for website loading delay until clickable
        try:
            wait_element = self.wait.until(EC.element_to_be_clickable(
                (by, value)))
            return wait_element
        except TimeoutException:
            print("Timeout occurred. Element didn't appear within the specified timeout.")
