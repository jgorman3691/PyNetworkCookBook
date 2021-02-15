#!/usr/bin/env python3

import socket, ntplib
from time import ctime

def print_time():
   client = ntplib.NTPClient()
   response = client.request('pool.ntp.org', version=3)
   answer = ctime(response.tx_time)
   print("{}".format(ctime(response.tx_time)))
   
if __name__ == '__main__':
   print_time()