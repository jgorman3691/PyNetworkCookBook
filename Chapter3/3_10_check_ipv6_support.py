#!/usr/bin/env python3

import socket
import argparse
import netifaces as ni

def inspect_ipv6_support():
   # Find the IPv6 address
   doesIt = socket.has_ipv6
   print(f"Is IPv6 support built into Python 3: {doesIt}")
   ipv6_addr = {}
   hardware = [i for i in ni.interfaces()]
   for interface in hardware:
      all_addresses = ni.ifaddresses(interface)
      print(f"Current Interface: {interface}")
      for family,addrs in all_addresses.items():
         fam_name = ni.address_families[family]
         print(f' Address family: {fam_name}')
         for addr in addrs:
            if fam_name == 'AF_INET6':
               ipv6_addr[interface] = addr['addr']
            print(f"IPv6 Address: {addr['addr']}")
            nmask = addr.get('netmask', None)
            if nmask:
               print(f'Netmask: {nmask}')
            bcast = addr.get('broadcast', None)
            if bcast:
               print(f'Broadcast: {bcast}')
      if ipv6_addr:
         print(f"Found IPv6 address: {ipv6_addr}")
      else:
         print("No IPv6 interface found!")
      
if __name__ == '__main__':
   inspect_ipv6_support()