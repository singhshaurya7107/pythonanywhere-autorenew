import os
import sys
import time
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

# The domain itself is lowercase, but the URL path requires exact casing
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
    
    wait.until(EC.url_changes("https://www.pythonanywhere.com/login/"))
    print(f"Login successful! Landed on: {driver.current_url}")
    
    # Use exact casing from the GitHub Secret (ShauryaSingh7107) for the URL
    webapps_url = f"https://www.pythonanywhere.com/user/{username}/webapps/"
    print(f"Navigating to Web tab: {webapps_url}")
    driver.get(webapps_url)
    
    time.sleep(5) 
    
    print("Locating the 'Run until 1 month from today' button...")
    
    # Target the exact button text
    extend_btn = wait.until(EC.presence_of_element_located((
        By.XPATH, 
        "//input[@value='Run until 1 month from today'] | //button[contains(text(), 'Run until 1 month from today')]"
    )))
    
    print("Button found! Force-clicking it via JavaScript...")
    driver.execute_script("arguments[0].click();", extend_btn)
    
    time.sleep(3)
    print(f"Successfully renewed {domain} for another month!")

except Exception as e:
    print(f"Failed to renew: {e}")
    print(f"Failed on URL: {driver.current_url}")
    try:
        # If it fails, print the HTML text to see what went wrong
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print("\n--- PAGE TEXT DUMP ---")
        print(body_text[:1500])
    except:
        pass
    sys.exit(1)
finally:
    driver.quit()
