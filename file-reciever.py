import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import cgi

class CustomHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
            for key in postvars:
                if key.startswith('file'):
                    file_data = postvars[key][0]
                    with open(os.path.join('uploads', key), 'wb') as f:
                        f.write(file_data)
        self.send_response(200)
        self.end_headers()

if not os.path.exists('uploads'):
    os.makedirs('uploads')

server_address = ('', 8000)
httpd = HTTPServer(server_address, CustomHandler)
print('Starting server on port 8000...')
httpd.serve_forever()
