#!/usr/bin/env python

import http.server
import logging
import json

IP = '127.0.0.1'
PORT = 8001

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        headers = self.headers
        print('received request:', url)

        numbers = url.split('/')
        print('parsed numbers:', numbers)
        try:
            with open('data.txt') as json_file:
                data = json.load(json_file)
            self.respond(data)
        except ValueError as ex:
            logging.error('unable to parse value: %s' % num)
            self.respond(-1)

    def respond(self, sumTotal):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Send message back to client
        message = str(sumTotal)
        # Write content as utf-8 data
        self.wfile.write(bytes(message, 'utf8'))
        return

def main():
    address = (IP, PORT)
    httpd = http.server.HTTPServer(address, MyHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    main()