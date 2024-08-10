import http.server
import socket
import socketserver
import os

PORT = 1000

def wlan_ip():
    import subprocess
    result=subprocess.run('ipconfig',stdout=subprocess.PIPE,text=True).stdout.lower()
    scan=0
    for i in result.split('\n'):
        if 'wireless' in i: scan=1
        if scan:
            if 'ipv4' in i: return i.split(':')[1].strip()

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def find_free_port(starting_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while True:
            try:
                s.bind(("", starting_port))
                return starting_port
            except OSError:
                starting_port += 1

def main():
    global PORT
    PORT = find_free_port(PORT)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    handler_object = MyHttpRequestHandler
    with socketserver.TCPServer(("", PORT), handler_object) as httpd:
        print(f"Serving HTTP on http://{wlan_ip()}:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
