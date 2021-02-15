#!/usr/bin/env python3

import socket
import sys
import argparse

host = 'localhost'
data_payload = 2048
backlog = 5

def echo_server(port):
   """A Simple Echo Example Server"""
   # Create a TCP socket
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # Enable the reuse of the address/port
   sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   # Bind the socket to the port
   server_address = (host, port)
   print("Starting up the echo server at %s on port %s..." % server_address)
   sock.bind(server_address)
   
   # Listen to clients, the backlog argument specifies the maximum number of simultaneous connections
   sock.listen(backlog)
   while True:
      print("Waiting to receive a message from the client")
      client, address = sock.accept()
      data = client.recv(data_payload)
      if data:
         print("Data: %s" % data.decode("utf-8"))
         client.send(data)
         print("Sent %s bytes back to %s" % (data.decode("utf-8"), address))
   # End the connection
   client.close()
   
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Socket Server Example')
   parser.add_argument('--port', action="store",  dest="port", type=int, required=True)
   given_args = parser.parse_args()
   port = given_args.port
   echo_server(port)