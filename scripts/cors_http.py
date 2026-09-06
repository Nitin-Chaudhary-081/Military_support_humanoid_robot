#!/usr/bin/env python3
"""CORS HTTP server for Foxglove mesh fetching — serves install/ares1_description/share/ares1_description/meshes"""
import http.server, socketserver, os, pathlib
PORT = 8000
ROOT = pathlib.Path("/home/ubuntu/ms_robot/install/ares1_description/share/ares1_description/meshes")
class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()
    def do_OPTIONS(self):
        self.send_response(200); self.end_headers()
os.chdir(ROOT)
with socketserver.TCPServer(("0.0.0.0", PORT), CORSHandler) as httpd:
    print(f"Serving {ROOT} at http://0.0.0.0:{PORT} with CORS *")
    httpd.serve_forever()
