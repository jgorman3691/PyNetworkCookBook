#!/usr/bin/env python3

import argparse
import sys
import http
from http import server as sv
from http import client as cl
from http.server import BaseHTTPRequestHandler, HTTPServer

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 97531

class RequestHandler(BaseHTTPRequestHandler): # Our Custom request handler!
   
   def do_GET(self):
      """The Handler for the GET requests"""
      self.send_response(200)
      self.send_header("Content-Type", "text/html", "charset=utf-8")
      self.send_header("Server", "Apache/2.4.38", "Debian")
      self.end_headers()
      
      # Send the message to the browser.  This might need to be encoded
      self.wfile.write('Hello from the server!')
      
class CustomHTTPServer(HTTPServer):
   """ A custom HTTP server, to imitate the previous"""
   def __init__(self, host, port):
      server_address = (host, port)
      super(HTTPServer).__init__(self, server_address, RequestHandler)
      
def run_server(port):
   try:
      server = CustomHTTPServer(DEFAULT_HOST, port)
      print(f'Custom HTTP server started on port: {port}')
      sv.serve_forever()
   except Exception as err:
      print(f"Error: {err}")
   except KeyboardInterrupt:
      print("The server has been interrupted by a typed command and is shutting down...")
      sv.socket.close()
      
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Simple HTTP Server Example')
   parser.add_argument('--port', action="store", dest="port", type=int, default=DEFAULT_PORT)
   given_args = parser.parse_args
   port = given_args.port
   run_server(port)