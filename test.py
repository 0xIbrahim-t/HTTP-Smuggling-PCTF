import requests
import time

SERVER_URL = "http://54.198.62.41"

def login_user(username="user", password="user123"):
    """Login as user"""
    login_data = {
        "username": username,
        "password": password
    }
    r = requests.post(f"{SERVER_URL}/api/auth/login", json=login_data)
    return r.json()['token']

def test_cache():
    user_token = login_user()
    print(f"[+] Got user token: {user_token[:20]}...")

    # First test without cache key
    print("\n[1] Testing without cache key:")
    headers = {
        'Authorization': f'Bearer {user_token}'
    }
    r = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Cache-Control: {r.headers.get('Cache-Control')}")
    print(f"Content: {r.text[:200]}")

    # Test with cache key
    print("\n[2] Testing with cache key:")
    headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key'
    }
    r = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Cache-Control: {r.headers.get('Cache-Control')}")
    print(f"Content: {r.text[:200]}")

    # Test caching behavior
    print("\n[3] Testing multiple requests with cache key:")
    for i in range(3):
        r = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=headers)
        print(f"\nRequest {i+1}:")
        print(f"Status: {r.status_code}")
        print(f"Cache-Control: {r.headers.get('Cache-Control')}")
        print(f"X-Cache-Key: {r.headers.get('X-Cache-Key')}")
        print(f"X-Cache-Debug: {r.headers.get('X-Cache-Debug')}")
        time.sleep(1)

    # Get admin token to test admin view
    print("\n[4] Testing with admin token:")
    # Using the correct admin credentials
    admin_token = login_user("admin", "admin123")
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'X-Special-Key': 'secret_cache_key',
        'X-Admin-Request': 'true'  # Add this to match admin bot headers
    }
    r = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Cache-Control: {r.headers.get('Cache-Control')}")
    print(f"X-Debug-Admin-Status: {r.headers.get('X-Debug-Admin-Status')}")
    print(f"X-Cache-Debug: {r.headers.get('X-Cache-Debug')}")
    print(f"Content: {r.text[:200]}")

    # Test if cache is deleted after admin view
    print("\n[5] Testing if cache was deleted after admin view:")
    headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key'
    }
    r = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Cache-Control: {r.headers.get('Cache-Control')}")
    print(f"X-Cache-Debug: {r.headers.get('X-Cache-Debug')}")
    print(f"Content: {r.text[:200]}")

if __name__ == "__main__":
    print("[+] Starting cache testing...")
    test_cache()