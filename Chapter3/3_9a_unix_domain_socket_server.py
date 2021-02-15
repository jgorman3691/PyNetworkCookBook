#!/usr/bin/env python3

import socket
import os
import time
from pathlib import Path

SERVER_PATH = Path("/tmp/python_unix_socket_server")

def run_unix_domain_socket_server():
   if Path.exists(SERVER_PATH):
      Path.remove(SERVER_PATH)

   print("Starting Unix Domain Socket Serer")
   server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
   server.bind(bytes("/tmp/python_unix_socket_server", "utf-8"))

   print("Listening on path: {}".format(SERVER_PATH))
   while True:
      datagram = server.recv(1024)
      if not datagram:
         break
      else:
         print("-"*20)
         d = datagram.decode("utf-8")
         print(d)
      if "DONE" == d:
            break
   print("-"*20)
   print("Server is now shutting down.")
   server.close()
   Path.remove(SERVER_PATH)
   print("The server has been shut down, and the path removed.")

if __name__ == '__main__':
   run_unix_domain_socket_server()
