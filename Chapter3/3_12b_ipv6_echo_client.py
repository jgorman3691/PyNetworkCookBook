#!/usr/bin/env python3

import argparse
import sys
import socket

HOST = 'localhost'
PORT = 50057
BUFSIZE = 1024

def ipv6_echo_client(port=PORT, host=HOST):  
   for res in socket.getaddrinfo(
      HOST, # host,
      PORT, # port,
      socket.AF_INET6,
      socket.SOCK_STREAM,
      ):
      af, socktype, proto, canonname, sa = res
      print(af)
      print(socktype)
      print(proto)
      print(sa)
      try:
         sock = socket.socket(af, socktype, proto)
      except socket.error as err:
         print(f"Error: {err}")
         sock = None
      try:
         sock.connect(sa)
      except socket.error as msg:
         print(f"Error: {msg}")
         sock.close()
         sock = None
         continue
      break
   if sock is None:
      print("Failed to open socket...")
      sys.exit(1)
   message = "Hello from the IPv6 client!"
   print(f"Send data to the server: {message}")
   emessage = message.encode()
   sock.send(emessage)
   while True:
      data = sock.recv(BUFSIZE)
      if not data:
         break
      ddata = repr(data)
      print(f"Received data from the server: [ {ddata} ]")
   sock.close()
   
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='IPv6 Socket Client Example')
   #parser.add_argument('--port', action="store", dest="port", type=int, required=True)
   #given_args = parser.parse_args()
   #port = given_args.port
   ipv6_echo_client(PORT)