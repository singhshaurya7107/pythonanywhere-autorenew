import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = os.environ.get('PA_USERNAME')
password = os.environ.get('PA_PASSWORD')

if not username or not password:
    print("Error: Missing credentials in GitHub Secrets.")
    sys.exit(1)

domain = f"{username.lower()}.pythonanywhere.com"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

try:
    print("Logging into PythonAnywhere...")
    driver.get("https://www.pythonanywhere.com/login/")
    
    wait.until(EC.presence_of_element_located((By.NAME, "auth-username"))).send_keys(username)
    driver.find_element(By.NAME, "auth-password").send_keys(password)
    driver.find_element(By.ID, "id_next").click()
    
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Log out")))
    print("Login successful!")
    
    print("Navigating to Web tab...")
    driver.get(f"https://www.pythonanywhere.com/user/{username}/webapps/")
    
    print("Clicking the Extend button...")
    extend_form = wait.until(EC.presence_of_element_located((By.XPATH, "//form[contains(@action, 'extend')]")))
    extend_btn = extend_form.find_element(By.XPATH, ".//input[@type='submit']")
    extend_btn.click()
    
    print(f"Successfully renewed {domain} for another 30 days!")

except Exception as e:
    print(f"Failed to renew: {e}")
    sys.exit(1)
finally:
    driver.quit()
