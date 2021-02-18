#!/usr/bin/env python3

import ssl
import urllib
from urllib import request as rqt
from urllib import parse as prs
from urllib import error as err

URL = 'https://www.github.com'
PROXY_ADDRESS = '172.16.1.13:8080'
CA = '/etc/ssl/certs/ca-certificates.crt'
purpose = ssl.Purpose.SERVER_AUTH
context = ssl.create_default_context(purpose, cafile=CA)

if __name__ == '__main__':
   prox = rqt.getproxies()
   response = rqt.urlopen(URL, prox, context=context)
   print(f"Proxy server returns response headers : {response.headers}")