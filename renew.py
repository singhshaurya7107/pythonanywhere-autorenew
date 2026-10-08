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

# Force desktop mode and mimic a real user
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
    
    # Use explicit IDs
    wait.until(EC.presence_of_element_located((By.ID, "id_auth-username"))).send_keys(username)
    driver.find_element(By.ID, "id_auth-password").send_keys(password)
    driver.find_element(By.ID, "id_next").click()
    
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Log out")))
    print("Login successful!")
    
    print("Navigating to Web tab...")
    driver.get(f"https://www.pythonanywhere.com/user/{username}/webapps/")
    
    print("Clicking the Extend button...")
    extend_form = wait.until(EC.presence_of_element_located((By.XPATH, f"//form[contains(@action, 'extend')]")))
    extend_btn = extend_form.find_element(By.XPATH, ".//button | .//input[@type='submit']")
    extend_btn.click()
    
    print(f"Successfully renewed {domain} for another 30 days!")

except Exception as e:
    print(f"Failed to renew: {e}")
    print(f"Failed on URL: {driver.current_url}")
    sys.exit(1)
finally:
    driver.quit()
