"""
This minimal HTTP server is used to keep the container alive in environments like Azure App Service,
which expects a response on port 80. It is not part of the application domain or business logic.
"""


from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start():
    def run():
        server = HTTPServer(("0.0.0.0", 80), HealthCheckHandler)
        server.serve_forever()

    threading.Thread(target=run, daemon=True).start()
