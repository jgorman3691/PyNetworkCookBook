#!/usr/bin/env python3

import os
import socket
import threading
import socketserver

# Here we initialize some global variables

SERVER_HOST = 'localhost'
SERVER_PORT = 0 # This tells the kernel to pick up ports dynamically
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server!'

class ForkedClient():
   """ A client for the forking server """
   def __init__(self, ip, port):
      # Create a socket
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # Connect to the server
      self.sock.connect((ip, port))
      
   def run(self):
      """ The client playing with the server """
      # Send the data to the server
      current_process_id = os.getpid()
      print('PID %s Sending echo message to the server : "%s"' % (str(current_process_id), ECHO_MSG))
      sent_data_length = self.sock.send(ECHO_MSG.encode("utf-8"))
      print("Sent: %d characters so far..." % sent_data_length)
      
      # Display the server response
      response = self.sock.recv(BUF_SIZE)
      print("PID %s received: %s" % (str(current_process_id), response.decode("utf-8")[5:]))
      
   def shutdown(self):
      """ Clean up after ourselves! """
      self.sock.close()
      
class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
   def handle(self):
      # Send the echo back to the server from whence it came
      data = self.request.recv(BUF_SIZE)
      current_process_id = os.getpid()
      response = '%s: %s' % (str(current_process_id), data.decode("utf-8"))
      print("Server sending response [current_process_id: data] = %s" % response)
      self.request.send(response.encode("utf-8"))
      return

class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
   """ Nothing to see here, ladies and gents! """
   pass

def main():
   # Launch the server
   server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
   ip, port = server.server_address # Retrieve the port number
   server_thread = threading.Thread(target=server.serve_forever)
   server_thread.setDaemon(True) # Don't hang on exit, get the fuck out!
   server_thread.start()
   print('Server loop running PID: %s' % str(os.getpid()))
   
   # Launch the client(s)
   client1 = ForkedClient(ip, port)
   client1.run()

   client2 = ForkedClient(ip, port)
   client2.run()
   
   # Final cleanup
   server.shutdown()
   client1.shutdown()
   client2.shutdown()
   server.socket.close()
   
if __name__ == '__main__':
   main()