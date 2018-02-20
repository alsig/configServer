#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import logging
import json

class Server(BaseHTTPRequestHandler):
    _config = None
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        query_components = parse_qs(urlparse(self.path).query)
        device = query_components["device"]
        data = self._config[device[0]]
    
        json_string = json.dumps(data)
        self.wfile.write("{}".format(json_string).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8081, configFile="config.json"):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)

    handler_class._config = json.load(open(configFile))
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 3:
        run(port=int(argv[1]), configFile=str(argv[2]))
    else:
        run()