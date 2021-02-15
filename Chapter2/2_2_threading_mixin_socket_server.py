#!/usr/bin/env python3

import socket
import os
import threading
import socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 0
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server!'

class ThreadedClient():
   """ A client to test a multithreaded server """
   def __init__(self, ip, port):
      # Create a socket
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # Connect to the server
      self.sock.connect((ip, port))

   def run(self):
      """ Client playing with the server """
      # Send the data to the server
      current_thread_id = threading.current_thread()
      print("Thread ID %s sending echo message to the server: %s" % (str(current_thread_id), ECHO_MSG))
      sent_data_length = self.sock.send(ECHO_MSG.encode("utf-8"))
      print("Sent: %d characters so far..." % sent_data_length)

      # Display the server response
      response = self.sock.recv(BUF_SIZE)
      current_thread = threading.current_thread()
      print("TID %s received: %s" % (current_thread.name, response.decode("utf-8")[5:]))

   def shutdown(self):
      # Clean up
      self.sock.close()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
   def handle(self):
      # Return the echo
      data = self.request.recv(BUF_SIZE)
      current_thread = threading.current_thread()
      response = ("%s: %s" % (current_thread.name, data))
      self.request.sendall(response.encode("utf-8"))
      return

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
   # Nothing to add here, we have inherited what we need from the parent classes
   pass

def main():
   # Run the server
   server = ThreadedTCPServer((SERVER_HOST,SERVER_PORT), ThreadedTCPRequestHandler)
   ip, port = server.server_address

   # Start a thread with the server -- one thread per request
   server_thread = threading.Thread(target=server.serve_forever)

   # Exit the server thread when the main thread exits
   server_thread.daemon = True
   server_thread.start()
   print("Server loop running on thread: %s" % server_thread.name)

   # Run the clients

   client1 = ThreadedClient(ip, port)
   client2 = ThreadedClient(ip, port)
   client3 = ThreadedClient(ip, port)
   client1.run()
   client2.run()
   client3.run()
   
   # It's the Final Cleanup!
   server.shutdown()
   client1.shutdown()
   client2.shutdown()
   client3.shutdown()
   server.socket.close()
   
if __name__ == '__main__':
   main()
