#!/usr/bin/env python3
#nc 192.168.1.250 8077
#192.168.1.166

import socketserver
import datetime

class MyTCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print('Recieved one request from {}'.format(self.client_address[0]))
        msg = self.rfile.readline().strip()
        print('Data recieved from client is'.format(msg))
        print(msg)
        
        with open('Log', 'a') as file:
            file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

aServer = socketserver.TCPServer(('127.0.0.1', 8077), MyTCPRequestHandler)
aServer.serve_forever()
