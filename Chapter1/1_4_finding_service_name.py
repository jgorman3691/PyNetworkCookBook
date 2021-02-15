#!/usr/bin/env python3

import socket

def find_service_name():
   protocolname = 'tcp'
   for port in [80, 25]:
      print("Port: %s => Service Name: %s" % (port, socket.getservbyport(port, protocolname)))
   print("Port: %s => Service Name: %s" % (53, socket.getservbyport(53, 'udp')))

if __name__ == '__main__':
   find_service_name()