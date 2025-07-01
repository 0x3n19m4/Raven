from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        with open("out.txt", "a") as f:
            f.write(str(post_data) + "\n")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        self.wfile.write(b"Received POST data:\n")
        self.wfile.write(str(post_data).encode('utf-8'))

if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server running on port 8080")
    httpd.serve_forever()
