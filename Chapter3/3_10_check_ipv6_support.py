#!/usr/bin/env python3

import socket
import argparse
import netifaces as ni

def inspect_ipv6_support():
   # Find the IPv6 address
   print("IPv6 support built into Python 3: %s" % socket.has_ipv6)
   ipv6_addr = {}
   hardware = [i for i in ni.interfaces()]
   for interface in hardware:
      all_addresses = {family:addrs = [i for i in addrs] for (family,addrs) in ni.ifaddresses(interface)}
      print("Interface: {}".format(interface))
      for family,addrs in all_addresses:
         fam_name = ni.address_families[family]
         print(' Address family: {}'.format(fam_name))
         for addr in addrs:
            if fam_name == 'AF_INET6':
               ipv6_addr[interface] = addr['addr']
            print("Address: %s" % addr['addr'])
            nmask = addr.get('netmask', None)
            if nmask:
               print('Netmask: %s' % nmask)
            bcast = addr.get('broadcast', None)
            if bcast:
               print('Broadcast: %s' % bcast)
   if ipv6_addr:
      print("Found IPv6 address: %s" % ipv6_addr)
   else:
      print("No IPv6 interface found!")
      
if __name__ == '__main__':
   inspect_ipv6_support()