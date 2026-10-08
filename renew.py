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

domain = f"{username.lower()}.pythonanywhere.com"

# Force desktop mode to bypass mobile responsive menus
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

try:
    print("Logging into PythonAnywhere...")
    driver.get("https://www.pythonanywhere.com/login/")
    
    wait.until(EC.presence_of_element_located((By.NAME, "auth-username"))).send_keys(username)
    driver.find_element(By.NAME, "auth-password").send_keys(password)
    driver.find_element(By.ID, "id_next").click()
    
    wait.until(EC.url_changes("https://www.pythonanywhere.com/login/"))
    print(f"Login successful! Landed on: {driver.current_url}")
    
    print("Navigating to Web tab...")
    driver.get(f"https://www.pythonanywhere.com/user/{username}/webapps/")
    
    # Wait 5 seconds to guarantee all React/JavaScript UI elements finish loading
    time.sleep(5) 
    
    print("Locating the Extend button...")
    extend_btn = None
    
    # Strategy 1: Find any button containing the text "Run until"
    try:
        extend_btn = driver.find_element(By.XPATH, "//input[contains(@value, 'Run until')] | //button[contains(text(), 'Run until')]")
    except:
        pass
        
    # Strategy 2: Find a form with an action containing "extend"
    if not extend_btn:
        try:
            extend_form = driver.find_element(By.XPATH, "//form[contains(@action, 'extend')]")
            extend_btn = extend_form.find_element(By.XPATH, ".//button | .//input[@type='submit']")
        except:
            pass
            
    # Strategy 3: Find the specific warning button class PythonAnywhere uses
    if not extend_btn:
        try:
            extend_btn = driver.find_element(By.XPATH, "//*[contains(@class, 'btn-warning')]")
        except:
            pass

    if extend_btn:
        print("Extend button found! Force-clicking it via JavaScript...")
        driver.execute_script("arguments[0].click();", extend_btn)
        print(f"Successfully renewed {domain} for another 30 days!")
    else:
        print("Extend button NOT FOUND. The app might already be fully renewed, or the UI has changed.")
        print("\n--- BEGIN VISUAL TEXT DUMP OF THE DASHBOARD ---")
        # Extract the text of the page so we can see exactly what the bot is looking at
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(body_text[:2000])
        print("--- END TEXT DUMP ---\n")
        sys.exit(1)

except Exception as e:
    print(f"Failed to renew: {e}")
    sys.exit(1)
finally:
    driver.quit()
