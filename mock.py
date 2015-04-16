import random
from http.server import BaseHTTPRequestHandler, HTTPServer

from requests import codes


class Handler(BaseHTTPRequestHandler):
    CHOICES = [codes.OK, codes.TOO_MANY, codes.FORBIDDEN]
    def do_POST(self):
        self.send_response(random.choice(self.CHOICES))
        self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()
