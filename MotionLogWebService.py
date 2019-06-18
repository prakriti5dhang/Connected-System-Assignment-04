#!/usr/bin/env python3

#~ $ curl -v 'http://localhost:8080/?startTime=2&endTime=258'

import http
import http.server
import mimetypes
import urllib.parse
import datetime

port = 8066

class WebServer(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        req = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(req.query)
        print(qs)

        if req.path == '/':
            try:
                start = datetime.datetime.strptime((qs['startTime'][0]), '%Y-%m-%dT%H:%M')
                end = datetime.datetime.strptime((qs['endTime'][0]), '%Y-%m-%dT%H:%M')

            except (KeyError):
                self.send_response(http.HTTPStatus.BAD_REQUEST)
                self.send_header('Access-Control-Allow-Origin', '*')

            self.send_response(http.HTTPStatus.OK)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', mimetypes.types_map['.txt'])
            self.end_headers()

            with open('Log', 'r') as file:
                for line in file:
                    if start <= datetime.datetime.strptime(line.strip(), '%Y-%m-%d %H:%M:%S') < end:
                        self.wfile.write(line.encode('utf8'))

        else:
            self.send_response(http.HTTPStatus.NOT_FOUND)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()


httpd = http.server.HTTPServer(('', port), WebServer)
try:
    print('Serving...')
    httpd.serve_forever()
except (KeyboardInterrupt, SystemExit):
    print('Shutting down...')
    httpd.server_close()
