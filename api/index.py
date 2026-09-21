"""
Vercel Serverless Function Handler for AI Smart Complaint Resolver.
-------------------------------------------------------------------
Receives HTTP requests and returns ML analysis (category, urgency, department, summary).
"""

import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# Add root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.resolver import ComplaintResolver

# Pre-load resolver globally for fast serverless warm starts
models_dir = os.path.join(root_dir, "models")
try:
    resolver = ComplaintResolver(models_dir=models_dir)
except Exception as e:
    resolver = None
    _init_error = str(e)


class handler(BaseHTTPRequestHandler):
    """Vercel Python Serverless Function entrypoint."""

    def _send_json(self, status_code: int, data: dict):
        """Sends a JSON response with proper CORS headers."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self._send_json(200, {
            "status": "healthy",
            "service": "AI Smart Complaint Resolver API",
            "models_ready": resolver is not None,
        })

    def do_POST(self):
        if resolver is None:
            self._send_json(500, {
                "error": f"Model initialization failed: {_init_error}"
            })
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                body_bytes = self.rfile.read(content_length)
                payload = json.loads(body_bytes.decode("utf-8"))
            else:
                payload = {}

            message = payload.get("message", "").strip()

            if not message:
                self._send_json(400, {
                    "error": "Please provide a valid complaint message in the 'message' field."
                })
                return

            result = resolver.analyze(message)
            self._send_json(200, result)

        except Exception as err:
            self._send_json(500, {
                "error": f"Internal server error: {str(err)}"
            })


# Aliases for Vercel discovery
app = handler
application = handler
