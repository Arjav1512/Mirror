"""Serve React build files - production mode."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REACT_BUILD_DIR = BASE_DIR / 'frontend' / 'dist'

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve from React build directory if it exists, otherwise serve from frontend
        if REACT_BUILD_DIR.exists():
            self.directory = str(REACT_BUILD_DIR)
        else:
            # Fallback: serve from frontend for development
            self.directory = str(BASE_DIR / 'frontend')
        
        super().__init__(*args, directory=self.directory, **kwargs)
    
    def do_GET(self):
        # Handle React Router - serve index.html for all routes
        if self.path.startswith('/api'):
            # Don't handle API routes here
            self.send_error(404, "API routes not handled here")
            return
        
        # Check if it's a file request (has extension)
        if '.' in self.path.split('/')[-1] and self.path != '/':
            # It's a file, serve it normally
            super().do_GET()
        else:
            # It's a route, serve index.html for React Router
            self.path = '/index.html'
            super().do_GET()
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        pass

def run_server(port=5000):
    if REACT_BUILD_DIR.exists():
        os.chdir(str(REACT_BUILD_DIR))
        print(f"📦 Serving React production build from: {REACT_BUILD_DIR}")
    else:
        print(f"⚠️  React build not found. Run 'npm run build' in frontend directory first.")
        print(f"📁 Serving from: {BASE_DIR / 'frontend'}")
    
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, CustomHandler)
    
    print("\n" + "="*60)
    print("🚀 Starting Mirror Landing Page Server")
    print("="*60)
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
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    run_server(port)

