import sys
import os
from http.server import BaseHTTPRequestHandler
import json
import subprocess

# Add the parent directory to sys.path so we can import tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        try:
            # Execute the sync tool
            # Using subprocess to run the script and capture output
            result = subprocess.run(
                [sys.executable, "tools/incremental_sync.py"],
                capture_output=True,
                text=True,
                cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            )
            
            response = {
                "status": "success" if result.returncode == 0 else "error",
                "output": result.stdout,
                "error": result.stderr
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e)
            }).encode('utf-8'))

    def do_POST(self):
        return self.do_GET()
