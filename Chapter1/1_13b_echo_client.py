#!/usr/bin/env python3

import socket
import sys
import argparse

host = 'localhost'

def echo_client(port):
   """A simple echo client, dual to the simple echo server"""
   # Create a TCP/IP socket
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   # Connect the socket to the server
   server_address = (host, port)
   print("Connecting to %s on port %s"% server_address)
   sock.connect(server_address)
   
   # Send data in try-except form
   try:
      #Send data
      message = "Test message.  This will be echoed back by the server."
      print("Sending: %s" % message)
      sock.sendall(message.encode("utf-8"))
      
      # Look for the response
      amount_received = 0
      amount_expected = len(message)
      while (amount_received < amount_expected):
         data = sock.recv(16)
         amount_received += len(data)
         print("Received: %s" % data.decode("utf-8"))
   except socket.errno as e:
      print("Socket error: %s" % str(e))
   except Exception as e:
      print("Other exception: %s" % str(e))
   finally:
      print("Closing the connection to the server")
      sock.close()
      
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Socket Server Example (Client)')
   parser.add_argument('--port', action="store", dest="port", type=int, required=True)
   given_args = parser.parse_args()
   port = given_args.port
   echo_client(port)