from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
from os.path import join, dirname
from dotenv import load_dotenv
import time

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Using GoogleChrome as driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install(), options=chrome_options))

# Google login
driver.delete_all_cookies()
url = 'https://www.google.com/accounts/Login?hl=ja&continue=http://www.google.co.jp/'
driver.get(url)

google_email_input = driver.find_element(
    By.CSS_SELECTOR, 'input[type="email"][name="identifier"]')
google_email_input.send_keys(os.environ.get('EMAIL'))
google_email_input.send_keys(Keys.RETURN)

# Add a delay using explicit wait
wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds

try:
    wait.until(EC.presence_of_element_located((By.ID, 'username')))
except TimeoutException:
    print("Timeout occurred. The element did not appear within the specified timeout.")


# Signin
username_field = driver.find_element(By.ID, 'username')
username_field.send_keys(os.environ.get('USERNAME'))
password_field = driver.find_element(By.ID, 'password')
password_field.send_keys(os.environ.get('PASSWORD'))
driver.find_element(
    By.CSS_SELECTOR, 'input.btn.btn-lg.btn-primary.btn-block.btn-uppercase').send_keys(Keys.RETURN)

try:
    wait.until(EC.presence_of_element_located((By.XPATH, '(//button)[1]')))
except TimeoutException:
    print("Timeout occurred. The element did not appear within the specified timeout.")

authentication_button = driver.find_element(By.XPATH, '(//button)[1]')
authentication_button.send_keys(Keys.RETURN)

# Go to MOOCs slide page
try:
    wait.until(EC.presence_of_element_located(
        (By.TAG_NAME, 'img')))
except TimeoutException:
    print("Timeout occurred. The element did not appear within the specified timeout.")
driver.get('https://moocs.iniad.org/courses/2023/CS112/09/01')

# Authentication to MOOCs
try:
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'a.btn.btn-lg.btn-info[href="/auth/iniad"]')))
except TimeoutException:
    print("Timeout occurred. The element did not appear within the specified timeout.")
driver.find_element(
    By.CSS_SELECTOR, 'a.btn.btn-lg.btn-info[href="/auth/iniad"]').click()

# Switch to colelct text from google slide
try:
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
except TimeoutException:
    print("Timeout occurred. The element did not appear within the specified timeout.")
iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[allowfullscreen="true"]')
print(iframe)
driver.switch_to.frame(iframe)

# Find all text in the slide
text = ''
time.sleep(3)

while True:
    # Find all <g> tags on current page
    g_elements = driver.find_elements(By.TAG_NAME, 'g')
    for element in g_elements:
        element_text = element.get_attribute('aria-label')
        if element_text and not element_text.strip().isdigit():
            text += element_text
            print(element_text)

    # Go to next page
    next_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.punch-viewer-navbar-next')))
    print(next_button)
    if 'goog-flat-button-disabled' in next_button.get_attribute('class'):
        # If next page is disabled, exit the loop
        break
    next_button.send_keys(Keys.RETURN)

with open('text.txt', mode='w', encoding='utf-8') as f:
    f.write(text)

# Close the browser
time.sleep(60)

driver.quit()
