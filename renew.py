import requests
from bs4 import BeautifulSoup
import os
import sys

username = os.environ.get('PA_USERNAME')
password = os.environ.get('PA_PASSWORD')

if not username or not password:
    print("Error: Missing credentials in GitHub Secrets.")
    sys.exit(1)

domain = f"{username.lower()}.pythonanywhere.com"

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

# 1. Log into PythonAnywhere
login_url = "https://www.pythonanywhere.com/login/"
r = session.get(login_url)
soup = BeautifulSoup(r.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

login_data = {
    'csrfmiddlewaretoken': csrf_token,
    'auth-username': username,
    'auth-password': password,
    'login_view-current_step': 'auth'
}
r = session.post(login_url, data=login_data, headers={'Referer': login_url})

# 2. Verify Login
webapps_url = f"https://www.pythonanywhere.com/user/{username}/webapps/"
r = session.get(webapps_url)
if "Log out" not in r.text:
    print("Login failed. Please check your GitHub Secrets.")
    sys.exit(1)

# 3. Click the Renew Button
soup = BeautifulSoup(r.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
extend_url = f"https://www.pythonanywhere.com/user/{username}/webapps/{domain}/extend"

r = session.post(extend_url, data={'csrfmiddlewaretoken': csrf_token}, headers={'Referer': webapps_url})

if r.status_code == 200:
    print(f"Successfully renewed {domain} for another 3 months!")
else:
    print("Failed to renew the web app.")
    sys.exit(1)
