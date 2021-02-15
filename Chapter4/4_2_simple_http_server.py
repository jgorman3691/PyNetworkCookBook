#!/usr/bin/env python3

import argparse
import os
import socketserver, socket
import ssl
from socketserver import TCPServer
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8800
context = ssl.create_default_context()


class RequestHandler(BaseHTTPRequestHandler):
   # Custom request handler
   def __init__(self):
      super().__init__()
      
   def do_GET(self):
      # Handler for GET requests
      self.send_response(200)
      self.send_header('Content-Type', 'text/html')
      self.end_headers()
      self.flush_headers()
      # Send a message to the browser
      self.wfile.write(b'Hello from the server!')
      
   def do_POST(self):
      # Leaving Empty for now
      pass
      
class CustomHTTPServer(HTTPServer):
   # A custom HTTP Server
   def __init__(self, host, port):
      super(HTTPServer).__init__()
      self.host = host
      self.port = port
      self.edict = {}
      self.server_address = (self.host,self.port)
      
   # def run_server(self, port=DEFAULT_PORT):
   def run_server(self, handle=HTTPServer, handler=RequestHandler):
      try:
         handled = CustomHTTPServer(self, (self.host,self.port))
         served = handle(self.server_address, handler)
         print("Custom HTTP Server started on port: {}".format(self.server_address(1)))
         served.serve_forever()
      except Exception as e:
         # self.edict = handler.responses()
         self.edict = {k:v for (k,v) in handler.responses}
         print("Error: {} Short: {}, Long: {}".format(e, self.edict(e.items[0]), self.edict(e.items[1])))
         served.socket.close_connection()
      except KeyboardInterrupt:
         print("Server interrupted.  Shutting down...")
         served.socket.close_connection()

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="Simple HTTP Server Example")
   parser.add_argument('--port', action="store", dest="port", type=int, default=DEFAULT_PORT)
   given_args = parser.parse_args()
   port = given_args.port
   CustomHTTPServer.run_server(port)