"""Simple HTTP server for serving the landing page - no 403 errors!"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
FRONTEND_DIR = BASE_DIR / 'frontend'

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server(port=5000):
    os.chdir(str(FRONTEND_DIR))
    
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, CustomHandler)
    
    print("\n" + "="*60)
    print("🚀 Starting Mirror Landing Page Server")
    print("="*60)
    print(f"📍 Serving from: {FRONTEND_DIR}")
    print(f"🌐 Server running on: http://localhost:{port}")
    print(f"📝 Landing page: http://localhost:{port}/")
    print("="*60)
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        httpd.server_close()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    run_server(port)

