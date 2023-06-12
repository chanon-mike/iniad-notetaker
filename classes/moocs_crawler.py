import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .driver_base import WebDriverBase


class MOOCsCrawler(WebDriverBase):
    def __init__(self, driver):
        super().__init__(driver)

    def go_to_slide(self, url):
        # Go to MOOCs slide page
        self.driver.get(url)

    def extract_text(self):
        # Switch to extract text from google slide
        iframe = self.wait_for_element_presence(
            By.CSS_SELECTOR, 'iframe[allowfullscreen="true"]')
        self.driver.switch_to.frame(iframe)

        text = ''
        time.sleep(3)

        while True:
            # Find all <g> tags on current page
            g_elements = self.driver.find_elements(By.TAG_NAME, 'g')
            for element in g_elements:
                element_text = element.get_attribute('aria-label')
                if element_text and not element_text.strip().isdigit():
                    text += element_text
                    print(element_text)

            # Go to next page
            next_button = self.wait_for_element_clickable(
                By.CSS_SELECTOR, '.punch-viewer-navbar-next')
            if 'goog-flat-button-disabled' in next_button.get_attribute('class'):
                # If next page is disabled, exit the loop
                break
            next_button.send_keys(Keys.RETURN)

        self.driver.switch_to.default_content()

        return text
