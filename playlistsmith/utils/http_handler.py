from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        code = params.get("code", [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(
            b"Authorization successful! You can close this window.")
        self.server.code = code


def start_http_server(port=8888):
    """Start the HTTP server and capture the authorization code."""
    server = HTTPServer(("localhost", port), RedirectHandler)
    print(f"Starting HTTP server on port {port}...")
    server.handle_request()
    server.server_close()
    print("HTTP server stopped.")
    return server.code
