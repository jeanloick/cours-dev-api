import http.server # paramétrage : location, handler
import socketserver # écoute

class APIhandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        print("Esdeath is the best")
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write("coucou" .encode('utf-8'))

MyAPIhandler = APIhandler

# Server
try:
    with socketserver.TCPServer(("", 8080), MyAPIhandler) as httpd:
        print("Server working")
        httpd.allow_reuse_address = True 
        httpd.serve_forever()

except KeyboardInterrupt:
    print("Stopping server")
    httpd.server_close()