#!/usr/bin/env python3

import socket


def convert_ipv4_address():
    for ip_addr in ['127.0.0.1', '192.168.0.1']:
        packed_ip_addr = socket.inet_aton(ip_addr)
        unpacked_ip_addr = socket.inet_ntoa(packed_ip_addr)
        print("IP address: {} => Packed: {}, Unpacked: {}".format(ip_addr, packed_ip_addr.hex(), unpacked_ip_addr))

if __name__ == '__main__':
    convert_ipv4_address()
