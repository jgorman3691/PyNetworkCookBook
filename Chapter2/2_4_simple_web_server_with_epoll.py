#!/usr/bin/env python3


"""
Once again, I'm having problems.  This time, the server works, but there's a blocking error (on an unblocked fucking port)
at line 45, with requests.  I'm going to create a global variable BUF_SIZE and make it much larger
"""
import errno
import socket
import select
import argparse

SERVER_HOST = 'localhost'
BUF_SIZE = 4096
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
SERVER_RESPONSE = b"""HTTP/1.1 200 OK\r\nDate: Friday, 5 February 2021 00:50 GMT\r\nContent-Type: text/plain\r\nContent-Length: 25 \r\n\r\nHello from Epoll Server!"""

class EpollServer(object):
   """ A socket server using epoll! """
   def __init__(self, host=SERVER_HOST, port=0):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind((host, port))
      self.sock.listen(1)
      self.sock.setblocking(0)
      self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
      print("Started EPoll Server")
      self.epoll = select.epoll()
      self.epoll.register(self.sock.fileno(), select.EPOLLIN)
      
   def run(self):
      """ Executes epoll server operation """
      try:
         connections = {}; requests = {}; responses = {}
         while True:
            events = self.epoll.poll(1)
            for fileno, event in events:
               if(fileno == self.sock.fileno()):
                  connection, address = self.sock.accept()
                  connection.setblocking(0)
                  self.epoll.register(connection.fileno(), select.EPOLLIN)
                  connections[connection.fileno()] = connection
                  requests[connection.fileno()] = b''
                  responses[connection.fileno()] = SERVER_RESPONSE
               elif(event and select.EPOLLIN):
                  requests[fileno].socket.setdefaulttimeout(1)
                  requests[fileno] += connections[fileno].recv(BUF_SIZE)
                  if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                     self.epoll.modify(fileno, select.EPOLLOUT)
                     dash = ('---------------------------------------------------------------------\n')
                     print(requests[fileno].decode()[:-2])
               elif(event and select.EPOLLOUT):
                  byteswritten = connections[fileno].send(responses[fileno].encode("utf-8"))
                  responses[fileno] = responses[fileno][byteswritten:]
                  if len(responses[fileno]) == 0:
                     self.epoll.modify(fileno, 0)
                     connections[fileno].shutdown(socket.SHUT_RDWR)
                  elif event and select.EPOLLHUP:
                     self.epoll.unregister(fileno)
                     connections[fileno].close()
                     del connections[fileno]
      finally:
         self.epoll.unregister(self.sock.fileno())
         self.epoll.close()
         self.sock.close()
         
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Socket Server Example with Epoll')
   parser.add_argument('--port', action="store", dest="port", type=int, required=True)
   given_args = parser.parse_args()
   port = given_args.port
   server = EpollServer(host=SERVER_HOST, port=port)
   server.run()