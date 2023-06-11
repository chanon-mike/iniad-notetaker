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

# Chrome profile path setting
# options = Options()
# options.add_argument(
#     f"--user-data-dir={os.environ.get('GOOGLE_PROFILE_PATH')}")
# options.add_argument("--profile-directory=Profile 1")

# Replace with the appropriate web driver for your browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.delete_all_cookies()
url = 'https://www.google.com/accounts/Login?hl=ja&continue=http://www.google.co.jp/'
driver.get(url)

google_email_input = driver.find_element(
    By.CSS_SELECTOR, 'input[type="email"][name="identifier"]')
google_email_input.send_keys(os.environ.get('EMAIL'))
google_email_input.send_keys(Keys.RETURN)

# URL of MOOCs slide page
# target_url = 'https://moocs.iniad.org/courses/2023/CS114/03-2/02'
# driver.get(target_url)


# Add a delay using explicit wait
wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds

try:
    wait.until(EC.presence_of_element_located((By.ID, 'username')))
except TimeoutException:
    print("Timeout occurred. The element did not appear within the specified timeout.")


# driver.find_element(
#     By.CSS_SELECTOR, 'a.btn.btn-lg.btn-info[href="/auth/iniad"]').click()

# Signin
username_field = driver.find_element(By.ID, 'username')
username_field.send_keys(os.environ.get('USERNAME'))
password_field = driver.find_element(By.ID, 'password')
password_field.send_keys(os.environ.get('PASSWORD'))
driver.find_element(
    By.CSS_SELECTOR, 'input.btn.btn-lg.btn-primary.btn-block.btn-uppercase').click()

try:
    wait.until(EC.presence_of_element_located((By.XPATH, '(//button)[1]')))
except TimeoutException:
    print("Timeout occurred. The element did not appear within the specified timeout.")


authentication_button = driver.find_element(By.XPATH, '(//button)[1]')
authentication_button.send_keys(Keys.RETURN)


# Close the browser
time.sleep(100)

driver.quit()
