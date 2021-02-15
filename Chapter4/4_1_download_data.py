#!/usr/bin/env python3

import ssl
import argparse
import http.client as ht

REMOTE_SERVER_HOST = 'www.python.org'
REMOTE_SERVER_PATH = '/'
REMOTE_SERVER_PORT = 443

class HTTPSClient:
   def __init__(self, host=REMOTE_SERVER_HOST, port=REMOTE_SERVER_PORT):
      self.host = host
      self.port = port
      self.http_context = ssl.create_default_context()

   def fetch(self, path):
      self.path = path
      conn = ht.HTTPSConnection(self.host, self.port, timeout=10, context=self.http_context)

      # http_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
      # http_context.options |= ssl.OP_NO_TLSv1
      # http_context.options |= ssl.OP_NO_TLSv1_1

      # Prepare header
      conn.request("GET", self.path)
      #conn.putheader(Host: self.host:self.port)
      #conn.putheader(Accept: */*)
      #conn.endheaders()

      try:
         response = conn.getresponse()
         print(" {} {} {}".format(response.status, response.reason, response.version))
         data = response.read()
         data = data.decode("utf-8")
      except Exception as e:
         headers = conn.getresponse()
         status, reason = headers.status, headers.reason
         print("Client failed error code: {}, status: {}, reason: {}".format(e, status, reason))
      else:
         print("Got homepage from {}.".format(self.host))

      conn.close()
      response.close()
      return data

if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='HTTP Client Example')
   parser.add_argument('--host', action="store", dest="host", default=REMOTE_SERVER_HOST)
   parser .add_argument('--path', action="store", dest="path", default=REMOTE_SERVER_PATH)
   parser.add_argument('--port', action="store", dest="port", default=REMOTE_SERVER_PORT)
   given_args = parser.parse_args()
   host, path, port = given_args.host, given_args.path, given_args.port
   client = HTTPSClient(host, port)
   client.fetch(path)
   #print(client.fetch(path))
