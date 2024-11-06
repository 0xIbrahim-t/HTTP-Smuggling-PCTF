from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from flask import Flask, request
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class AdminBot:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL', 'http://webserver')
        self.admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        self.admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        self.admin_token = None
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        self.options = chrome_options

    def login_admin(self):
        logger.info("Starting admin login process...")
        driver = None
        try:
            driver = webdriver.Chrome(options=self.options)
            
            # First visit home page
            logger.info("Loading home page first...")
            driver.get(self.base_url)
            time.sleep(2)
            
            login_url = f"{self.base_url}/admin/login"
            logger.info(f"Accessing login page: {login_url}")
            driver.get(login_url)
            time.sleep(2)

            logger.debug(f"Page title: {driver.title}")
            logger.debug(f"Current URL: {driver.current_url}")
            
            # Find and fill username
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(self.admin_username)
            logger.debug("Username entered")
            
            # Find and fill password
            password_input = driver.find_element(By.NAME, "password")
            password_input.send_keys(self.admin_password)
            logger.debug("Password entered")
            
            # Submit form
            password_input.submit()
            logger.debug("Form submitted")
            
            # Wait for login to complete
            time.sleep(2)
            
            # Go to home page to ensure proper context
            logger.debug("Going to home page to get token")
            driver.get(self.base_url)
            time.sleep(2)
            
            # Get token from localStorage
            self.admin_token = driver.execute_script(
                "return localStorage.getItem('token')"
            )
            
            if not self.admin_token:
                raise Exception("Failed to get admin token")
            
            logger.info("Admin login successful")
            logger.debug(f"Admin token obtained: {self.admin_token[:20]}...")
                
        except Exception as e:
            logger.error(f"Admin login failed: {str(e)}")
            if driver:
                logger.error(f"Page source at error: {driver.page_source}")
            raise
        finally:
            if driver:
                driver.quit()

    def visit_post(self, post_id):
        logger.info(f"Visiting post {post_id}")
        
        if not self.admin_token:
            self.login_admin()
            
        driver = None
        try:
            driver = webdriver.Chrome(options=self.options)
            
            # First establish proper page context
            logger.info("Loading home page first...")
            driver.get(self.base_url)
            time.sleep(2)

            # Set token in localStorage now that we have a proper context
            logger.debug("Setting admin token in localStorage")
            driver.execute_script(
                f"localStorage.setItem('token', '{self.admin_token}')"
            )
            
            # Set up request interceptor for admin headers
            logger.debug("Setting up admin headers")
            driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
                'headers': {
                    'Authorization': f'Bearer {self.admin_token}',
                    'X-Admin-Request': 'true'
                }
            })
            
            # Visit the post
            post_url = f"{self.base_url}/post/{post_id}"
            logger.info(f"Accessing post URL: {post_url}")
            
            driver.get(post_url)
            logger.debug("Post page loaded")
            
            # Wait for potential XSS
            logger.debug("Waiting for potential XSS execution...")
            time.sleep(5)
            
            # Log current state
            logger.debug(f"Current URL: {driver.current_url}")
            logger.debug(f"Page title: {driver.title}")
            
            # Check localStorage after visit
            token_check = driver.execute_script(
                "return localStorage.getItem('token')"
            )
            logger.debug(f"Token still in localStorage: {bool(token_check)}")
            
            return {"status": "success", "message": "Post visited successfully"}
            
        except Exception as e:
            logger.error(f"Error visiting post: {str(e)}")
            if driver:
                logger.error(f"Page source at error: {driver.page_source}")
            return {"error": str(e)}, 500
            
        finally:
            if driver:
                driver.quit()

admin_bot = AdminBot()

@app.route('/visit', methods=['POST'])
def visit_reported_post():
    try:
        post_id = request.args.get('post_id')
        if not post_id:
            return {"error": "Missing post_id parameter"}, 400
            
        logger.info(f"Received visit request for post {post_id}")
        return admin_bot.visit_post(post_id)
        
    except Exception as e:
        logger.error(f"Error handling visit request: {str(e)}")
        return {"error": str(e)}, 500

if __name__ == '__main__':
    logger.info("Starting admin bot service...")
    app.run(host='0.0.0.0', port=3000)