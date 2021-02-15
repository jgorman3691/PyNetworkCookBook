#!/usr/bin/env python3

import socket
import sys
import argparse

def main():
   # Set up argument parsing
   parser = argparse.ArgumentParser(description='Socket Error Examples')
   parser.add_argument('--host', action="store", dest="host", required=False)
   parser.add_argument('--port', action="store", dest="port", type=int, required=False)
   parser.add_argument('--file', action="store", dest="file", required=False)
   given_args = parser.parse_args()
   host = given_args.host
   port = given_args.port
   filename = given_args.file

   # The First try-except block -- create socket
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   except socket.error as e:
      print("Error creating socket: %s" % e)
      sys.exit(1)
   
   # The Second try-except block -- connect to the given host and port
   try:
      s.connect((host, port))
   except socket.gaierror as e:
      print("Address-related error connecting to server: %s" % e)
   except socket.error as e:
      print("Connection error: %s" % e)
      sys.exit(1)
   
   # The Third try-except block -- sending data
   try:
      s.sendall("GET %s HTTP/1.0\r\n\r\n" % filename)
   except socket.error as e:
      print("Error sending data: %s" % e)
      sys.exit(1)
      
   while(True):
   # The Fourth try-except block -- waiting to receive data from the remote host
      try:
         buf = s.recv(2048)
      except socket.error as e:
         print("Error receiving data: %s" % e)
         sys.exit(1)
      if not len(buf):
         break
   # Write the received data to the screen
      sys.stdout.write(buf)
      
if __name__ == '__main__':
   main()
