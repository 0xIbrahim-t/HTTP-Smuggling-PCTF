from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from flask import Flask, request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class AdminBot:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL', 'http://nginx')
        self.admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        self.admin_password = os.getenv('ADMIN_PASSWORD', 'complex_admin_pass_123')
        self.admin_token = None
        
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        self.options = chrome_options

    def login_admin(self):
        logger.info("Attempting admin login...")
        driver = webdriver.Chrome(options=self.options)
        try:
            login_url = f"{self.base_url}/admin/login"
            logger.info("Accessing login page: %s", login_url)
            driver.get(login_url)
            
            username_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_input = driver.find_element(By.NAME, "password")
            
            username_input.send_keys(self.admin_username)
            password_input.send_keys(self.admin_password)
            password_input.submit()
            
            time.sleep(2)
            self.admin_token = driver.execute_script(
                "return localStorage.getItem('token')"
            )
            
            if not self.admin_token:
                raise Exception("Failed to get admin token")
            
            logger.info("Admin login successful")
                
        except Exception as e:
            logger.error("Admin login failed: %s", str(e))
            raise
        finally:
            driver.quit()

    def visit_post(self, post_id):
        logger.info("Visiting post %s", post_id)
        if not self.admin_token:
            self.login_admin()
            
        driver = webdriver.Chrome(options=self.options)
        try:
            driver.execute_script(
                f"localStorage.setItem('token', '{self.admin_token}')"
            )
            
            post_url = f"{self.base_url}/post/{post_id}"
            logger.info("Accessing post URL: %s", post_url)
            driver.get(post_url)
            
            time.sleep(5)
            
            return {"status": "success", "message": "Post visited"}
            
        except Exception as e:
            logger.error("Error visiting post: %s", str(e))
            return {"status": "error", "message": str(e)}
            
        finally:
            driver.quit()

# Create bot instance
admin_bot = AdminBot()

@app.route('/visit', methods=['POST'])
def visit_reported_post():
    try:
        post_id = request.args.get('post_id')
        if not post_id:
            return {"error": "Missing post_id parameter"}, 400
            
        result = admin_bot.visit_post(post_id)
        return result
        
    except Exception as e:
        logger.error("Error handling visit request: %s", str(e))
        return {"error": str(e)}, 500

if __name__ == '__main__':
    # Just start the Flask server, no login at startup
    logger.info("Starting admin bot service...")
    app.run(host='0.0.0.0', port=3000)