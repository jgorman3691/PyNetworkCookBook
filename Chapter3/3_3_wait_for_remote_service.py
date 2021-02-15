#!/usr/bin/env python3

import argparse
import socket
import errno
from time import time as now

DEFAULT_TIMEOUT = 120
DEFAULT_SERVER_HOST = 'localhost'
DEFAULT_SERVER_PORT = 80
BUF_SIZE = 4096

class NetServiceChecker(object):
   # Wait for a network service to come online
   def __init__(self, host, port, timeout=DEFAULT_TIMEOUT):
      self.host = host
      self.port = port
      self.timeout = timeout
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
   def end_wait(self):
      self.sock.close()
      
   def check(self):
      # Check the service
      if self.timeout:
         end_time = now() + self.timeout
         while True:
            try:
               self.sock.connect((self.host, self.port))
               if self.timeout:
                  next_timeout = end_time - now()
                  if next_timeout < 0:
                     return False
                  elif self.sock.recv(BUF_SIZE) or (end_time == now()):
                     print("Still waiting on a connection!")
                     continue
                  else:
                     print("Setting socket next timeout %s sec" % str(round(next_timeout)))
                     self.sock.settimeout(next_timeout)
            # Handle Exceptions
            except socket.timeout as err:
               if self.timeout:
                  return False
            except socket.error as err:
               print("Exception: %s" % err)
            #If all goes well!
            else:
               self.end_wait()
               
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Wait for Network Service')
   parser.add_argument('--host', action="store", dest="host", default=DEFAULT_SERVER_HOST)
   parser.add_argument('--port', action="store", dest="port", type=int, default=DEFAULT_SERVER_PORT)
   parser.add_argument('--timeout', action="store", dest="timeout", type=int, default=DEFAULT_TIMEOUT)
   given_args = parser.parse_args()
   host, port, timeout = given_args.host, given_args.port, given_args.timeout
   service_checker = NetServiceChecker(host, port, timeout=timeout)
   print("Checking for network service %s:%s..." % (host, port))
   if service_checker.check():
      print("Service is available again!")