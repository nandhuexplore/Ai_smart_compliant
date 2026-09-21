"""
Vercel Serverless Function Handler for AI Smart Complaint Resolver.
-------------------------------------------------------------------
Receives HTTP POST requests with JSON payload {"message": "..."}
and returns the ML analysis (category, urgency, department, summary).
"""

import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# Add root directory to sys.path so we can import src.resolver
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

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(
            json.dumps({
                "status": "healthy",
                "service": "AI Smart Complaint Resolver API",
                "models_ready": resolver is not None,
            }).encode("utf-8")
        )

    def do_POST(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        
        if resolver is None:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": f"Model initialization failed: {_init_error}"}).encode("utf-8")
            )
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            payload = json.loads(body_bytes.decode("utf-8"))
            message = payload.get("message", "").strip()

            if not message:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Please provide a valid complaint message."}).encode("utf-8"))
                return

            result = resolver.analyze(message)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))

        except Exception as err:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Internal server error: {str(err)}"}).encode("utf-8"))
