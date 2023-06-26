import time
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .driver_base import WebDriverBase


class MOOCsCrawler(WebDriverBase):
    def __init__(self, driver):
        super().__init__(driver)

    def go_to_slide(self, url):
        # Go to MOOCs slide page
        self.driver.get(url)

    def match_url(self, url):
        pattern = r"https:\/\/moocs\.iniad\.org\/courses\/(\d+)\/([A-Z0-9-]+)\/([A-Z0-9-]+)\/(\d+)"
        result = re.search(pattern, url.strip())
        formatted_name = ''

        if result:
            formatted_name = re.sub(pattern, r"\1_\2_\3_\4", url)
        else:
            print("URLパターンが一致しないため、もう一回入力してください")

        return formatted_name

    def extract_text(self):
        # Switch to extract text from google slide
        iframe = self.wait_for_element_presence(
            By.CSS_SELECTOR, 'iframe[allowfullscreen="true"]')
        self.driver.switch_to.frame(iframe)

        text = ''
        page_number = 1
        time.sleep(3)

        while True:
            text += f'\n\n'
            # Find all <g> tags on current page
            g_elements = self.driver.find_elements(By.TAG_NAME, 'g')
            for element in g_elements:
                element_text = element.get_attribute('aria-label')
                if element_text and not re.search(r"Copyright.*INIAD", element_text) and not element_text.strip().isdigit():
                    text += element_text

            # Go to next page
            next_button = self.wait_for_element_clickable(
                By.CSS_SELECTOR, '.punch-viewer-navbar-next')
            if 'goog-flat-button-disabled' in next_button.get_attribute('class'):
                # If next page is disabled, exit the loop
                break
            next_button.send_keys(Keys.RETURN)

            page_number += 1

        self.driver.switch_to.default_content()

        return text
