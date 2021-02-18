#!/usr/bin/env python3

import socket
import netifaces as ni
import ipaddress as ip6

def extract_ipv6_info():
   # Extracts the desired IPv6 Information
   answer = socket.has_ipv6
   print(f"Is IPv6 support built into Python 3? {answer}")
   for interface in ni.interfaces():
      all_addresses = ni.ifaddresses(interface)
      print(f"Interface: {interface}")
      for family, addrs in all_addresses.items():
         fam_name = ni.address_families[family]
         print(f'Address(es) of Interface(s): {fam_name}')
         for addr in addrs:
            if fam_name == 'AF_INET6':
               addr = addr['addr']
               ipaddr = ip6.IPv6Network(addr)
               ipvers = ip6.IPv6Network(addr).version
               ipprefix = ip6.IPv6Network(addr).prefixlen
               ipnet = ip6.IPv6Network(addr).network_address
               ipcast = ip6.IPv6Network(addr).broadcast_address
               print(f"\t IP Address: {ipaddr}")
               print(f"\t IP Version: {ipvers}")
               print(f"\t IP Prefix Length: {ipprefix}")
               print(f"\t Network: {ipnet}")
               print(f"\t Broadcast: {ipcast}")
   
if __name__ == '__main__':
   extract_ipv6_info()
