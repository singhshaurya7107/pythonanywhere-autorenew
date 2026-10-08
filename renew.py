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
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

try:
    print("Logging into PythonAnywhere...")
    driver.get("https://www.pythonanywhere.com/login/")
    
    wait.until(EC.presence_of_element_located((By.NAME, "auth-username"))).send_keys(username)
    driver.find_element(By.NAME, "auth-password").send_keys(password)
    driver.find_element(By.ID, "id_next").click()
    
    # Wait for the URL to change away from the login page to confirm success
    wait.until(EC.url_changes("https://www.pythonanywhere.com/login/"))
    print(f"Login successful! Landed on: {driver.current_url}")
    
    print("Navigating to Web tab...")
    driver.get(f"https://www.pythonanywhere.com/user/{username}/webapps/")
    
    print("Locating the Extend button...")
    extend_form = wait.until(EC.presence_of_element_located((By.XPATH, "//form[contains(@action, 'extend')]")))
    extend_btn = extend_form.find_element(By.XPATH, ".//button | .//input[@type='submit']")
    
    print("Clicking the Extend button...")
    # Force the click using JavaScript to bypass any hidden menus or intercepting banners
    driver.execute_script("arguments[0].click();", extend_btn)
    
    print(f"Successfully renewed {domain} for another 30 days!")

except Exception as e:
    print(f"Failed to renew: {e}")
    print(f"Failed on URL: {driver.current_url}")
    sys.exit(1)
finally:
    driver.quit()
