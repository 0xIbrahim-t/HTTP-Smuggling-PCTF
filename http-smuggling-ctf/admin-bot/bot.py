from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
from flask import Flask, request

app = Flask(__name__)

class AdminBot:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL', 'https://nginx')
        self.admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        self.admin_password = os.getenv('ADMIN_PASSWORD', 'complex_admin_pass_123')
        self.admin_token = None
        
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # Additional security headers that won't prevent the XSS
        chrome_options.add_argument('--disable-web-security')  # Intentionally vulnerable
        chrome_options.add_argument('--allow-running-insecure-content')
        
        self.options = chrome_options

    def login_admin(self):
        driver = webdriver.Chrome(options=self.options)
        try:
            # Login to get admin token
            driver.get(f"{self.base_url}/admin/login")
            
            # Wait for login form
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_input = driver.find_element(By.NAME, "password")
            
            # Fill credentials
            username_input.send_keys(self.admin_username)
            password_input.send_keys(self.admin_password)
            password_input.submit()
            
            # Wait for redirect and get token
            time.sleep(2)  # Vulnerable: Hard-coded wait
            self.admin_token = driver.execute_script(
                "return localStorage.getItem('token')"
            )
            
            if not self.admin_token:
                raise Exception("Failed to get admin token")
                
        finally:
            driver.quit()

    def visit_post(self, post_id):
        if not self.admin_token:
            self.login_admin()
            
        driver = webdriver.Chrome(options=self.options)
        try:
            # Inject admin token
            driver.execute_script(
                f"localStorage.setItem('token', '{self.admin_token}')"
            )
            
            # Visit the post
            post_url = f"{self.base_url}/post/{post_id}"
            driver.get(post_url)
            
            # Vulnerable: Wait long enough for XSS to execute
            time.sleep(5)
            
            # Look for any errors (won't catch XSS)
            if "Error" in driver.page_source:
                return {"status": "error", "message": "Failed to load post"}
                
            return {"status": "success", "message": "Post visited"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
        finally:
            driver.quit()

# Create bot instance
admin_bot = AdminBot()

@app.route('/visit', methods=['POST'])
def visit_reported_post():
    """Endpoint for triggering admin visit to a reported post"""
    try:
        post_id = request.args.get('post_id')
        if not post_id:
            return {"error": "Missing post_id parameter"}, 400
            
        result = admin_bot.visit_post(post_id)
        return result
        
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    # Initialize admin token on startup
    admin_bot.login_admin()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=3000)