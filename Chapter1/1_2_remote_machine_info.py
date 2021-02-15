#!/usr/bin/env python3

import socket

def get_remote_machine_info():
   remote_host = 'www.wncna.org'
   try:
      print("IP address: %s" % socket.gethostbyname(remote_host))
   except OSError(err_msg):
      print("%s: %s" % remote_host, err_msg)

if __name__ == '__main__':
   get_remote_machine_info()