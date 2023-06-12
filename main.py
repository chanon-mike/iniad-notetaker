import os
import time
from os.path import dirname, join

from dotenv import load_dotenv

from classes import Authentication, MOOCsCrawler
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

# Initialize local env variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
email = os.environ.get('EMAIL')
iniad_username = os.environ.get('USERNAME')
iniad_password = os.environ.get('PASSWORD')

# Initialize driver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install(), options=chrome_options))
driver.delete_all_cookies()


# Initialize class
authentication = Authentication(driver, email, iniad_username, iniad_password)
moocs = MOOCsCrawler(driver)
is_first = True

# Google login
authentication.login()

# Go to MOOCs slide page and authenticate (only for first time)
moocs.go_to_slide('https://moocs.iniad.org/courses/2023/CS112/09/01')
if is_first:
    authentication.iniad_login()
    is_first = False

# Switch to iframe and find all text, then switch back
text = moocs.extract_text()

with open('text.txt', mode='w', encoding='utf-8') as f:
    f.write(text)

# Close the browser
time.sleep(60)
