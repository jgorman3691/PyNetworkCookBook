#!/usr/bin/env python3

import argparse
import socket
import sys

HOST = 'localhost'
SERVER_PORT = 50057

def echo_server(port, host=HOST):
   #Echo Server using IPv6
   for res in socket.getaddrinfo(
      host,
      port,
      socket.AF_INET6,
      socket.SOCK_STREAM,
      0,
      socket.AI_PASSIVE):
      af, socktype, proto, canonname, sa = res
      try:
         sock = socket.socket(af, socktype, proto)
         # sock.setsockopt(IPV6_ONLY=False)
      except socket.error as e:
         print(f"Error: {e}")
         sock = None
      except KeyboardInterrupt:
         sys.exit(1)
      try:
         sock.bind(sa)
         sock.listen(1)
         print(f"Server listening on {sa[0]}:{sa[1]}")
      except socket.error as msg:
         print(f"Error: {msg}")
         sock.close()
         sock = None
         break
      except KeyboardInterrupt:
         sys.exit(1)
   conn,addr = sock.accept()
   print(f'Connected to: {addr}')
   while(True):
      data = conn.recv(1024)
      if not data:
         break
      ddata = data.decode()
      print(f"Received data from the client: [ {ddata} ]")
      edata = data
      conn.send(edata)
      edata = repr(edata)
      print(f"Sent data echoed back to the client [ {edata} ]")
   conn.close()
   

if __name__ == '__main__':
   # parser = argparse.ArgumentParser(description='IPv6 Socket Server Example')
   # parser.add_argument('--port', action="store", dest="port", type=int, required=True)
   # given_args = parser.parse_args()
   # port = given_args.port
   echo_server(SERVER_PORT)