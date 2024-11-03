import requests

# Define the target URL
url = "https://54.198.62.41/post/1"

# Admin request with special header to set cache content
admin_headers = {
    "Authorization": "Bearer role=admin",
    "X-Special-Key": "secret_cache_key",
    "User-Agent": "CachePoisonTestAdmin"
}

# Normal user request with no admin privileges
normal_headers = {
    "User-Agent": "CachePoisonTestNormal"
}

# Perform the admin request to populate the cache
print("Sending admin request...")
admin_response = requests.get(url, headers=admin_headers, verify=False)
print("Admin Response Headers:")
print(admin_response.headers)
print("Admin Response Body:")
print(admin_response.text)

# Perform the normal request to test if it retrieves the cached admin content
print("\nSending normal request...")
normal_response = requests.get(url, headers=normal_headers, verify=False)
print("Normal Response Headers:")
print(normal_response.headers)
print("Normal Response Body:")
print(normal_response.text)

# Check for cache status in response headers
print("\nCache Status in Admin Response:", admin_response.headers.get("X-Cache-Status", "No X-Cache-Status header"))
print("Cache Status in Normal Response:", normal_response.headers.get("X-Cache-Status", "No X-Cache-Status header"))

# Check if admin-specific information leaked to normal user
if admin_response.text == normal_response.text:
    print("\nPotential cache poisoning vulnerability detected: Normal user received cached admin content.")
else:
    print("\nNo cache poisoning detected: Normal user received non-admin content.")
