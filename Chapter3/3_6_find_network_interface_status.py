#!/usr/bin/env python3
"""
This program works perfectly...except for the part where it can't find
the python3-nmap I installed, along with the even more powerful nmap I
installed from the package.
"""

import argparse
import fcntl
import socket
import struct
import nmap

SAMPLE_PORTS='21-23'

def get_interface_status(ifname):
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   ip_address = socket.inet_ntoa(
   fcntl.ioctl(
            sock.fileno(),
            0x8915,  # SIOCGIFADDR, C socket library sockios.h
            struct.pack('256s', bytes(ifname[:15], 'utf-8')))[20:24])
   nm = nmap.PortScanner()
   nm.scan(ip_address, SAMPLE_PORTS)
   return nm(ip_address).state()

if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Python Networking Utils')
   parser.add_argument('--ifname', action="store", dest="ifname", required=True)
   given_args = parser.parse_args()
   ifname = given_args.ifname
   print("Interface [%s] is: %s" % (ifname, get_interface_status(ifname)))
