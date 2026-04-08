import sys
import os
from http.server import BaseHTTPRequestHandler
import json
import io
import contextlib
import traceback

# Add the 'tools' directory to sys.path so modules can import each other
tools_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools'))
if tools_path not in sys.path:
    sys.path.append(tools_path)

from incremental_sync import run_incremental_sync

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # CORS headers in case the dashboard is accessed differently
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        
        try:
            # Capture stdout to return it to the frontend
            f = io.StringIO()
            with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
                run_incremental_sync()
            
            output = f.getvalue()
            response = {
                "status": "success",
                "output": output,
                "error": ""
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e),
                "error": traceback.format_exc()
            }).encode('utf-8'))

    def do_POST(self):
        return self.do_GET()
