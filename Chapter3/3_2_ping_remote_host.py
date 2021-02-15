#!usr/bin/env python3

import os
import argparse
import socket
import struct
import select
import time

ICMP_ECHO_REQUEST = 8 # Platform specific
DEFAULT_TIMEOUT = 2
DEFAULT_COUNT = 5

class Pinger(object):
   """ Pings to a host -- the Pythonic way! """
   def __init__(self, target_host, count=DEFAULT_COUNT, timeout=DEFAULT_TIMEOUT):
      self.target_host = target_host
      self.count = count
      self.timeout = timeout
   def do_checksum(self, source_string):
      # Verify packet integrity
      sum = 0
      max_count = (len(source_string)/2) * 2
      count = 0
      while count < max_count:
         val = (source_string[count + 1]) * 256 + (source_string[count])
         sum = sum + val
         sum = sum & 0xffffffff
         count = count + 2
      if (max_count < len(source_string)):
         sum = sum + ord(source_string[len(source_string) - 1])
         sum = sum & 0xffffffff
      sum = (sum >> 16) + (sum & 0xffff)
      sum = sum + (sum >> 16)
      answer = ~sum
      answer = answer & 0xffff
      answer = answer >> 8 | (answer << 8 & 0xff00)
      return answer
   def receive_pong(self, sock, ID, timeout):
      # Receive the ping from the socket
      time_remaining = timeout
      while True:
         start_time = time.time()
         readable = select.select([sock], [], [], time_remaining)
         time_spent = (time.time() - start_time)
         if readable[0] == []: # Timeout
            return
         
         time_received = time.time()
         recv_packet, addr = sock.recvfrom(1024)
         icmp_header = recv_packet[20:28]
         type, code, checksum, packet_ID, sequence = struct.unpack("bbHHh", icmp_header)
         if packet_ID == ID:
            bytes_IN_double = struct.calcsize("d")
            time_sent = struct.unpack("d", recv_packet[28:28 + bytes_IN_double])[0]
            return time_received - time_spent
         time_remaining = time_remaining - time_spent
         if time_remaining <= 0:
            return
   def send_ping(self, sock, ID):
      # Send the ping to the target host
      target_addr = socket.gethostbyname(self.target_host)
      my_checksum = 0
      # Create a dummy header with a 0 checksum.
      header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
      bytes_IN_double = struct.calcsize("d")
      data = (192 - bytes_IN_double) * "Q"
      data = struct.pack("d", time.time()) + data.encode()
      
      # Get the checksum on the data and the dummy header.
      my_checksum = self.do_checksum(header + data)
      header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1)
      packet = header + data
      sock.sendto(packet, (target_addr, 1))
   def ping_once(self):
      """
      Returns the delay in seconds, or none on timeout
      """
      icmp = socket.getprotobyname("icmp")
      msg = ''
      try:
         sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
      except socket.error as errno:
         if errno == 1:
            # Not SuperUser or Root, so the operation is not permitted
            msg += "ICMP messages can only be sent from processes with root user permission"
            raise socket.error(msg)
      except Exception as e:
         print("Exception: (%s)" % e)
      my_ID = os.getpid() & 0xFFFF
      self.send_ping(sock, my_ID)
      delay = self.receive_pong(sock, my_ID, self.timeout)
      sock.close()
      return delay
   def ping(self):
      # Runs the ping process
      for i in range(self.count):
         print("Ping to %s..." % self.target_host)
         try:
            delay = self.ping_once()
         except socket.gaierror as e:
            print("Ping failed with socket error: %s" % e[1])
            break
         if delay == None:
            print("Ping failed.  Timeout within %s seconds" % self.timeout)
         else:
            delay = delay * 1000
            print("Get pong in {:0.4f}ms".format(delay))
            
if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Python Ping')
   parser.add_argument('--target-host', action="store", dest="target_host", required=True)
   given_args = parser.parse_args()
   target_host = given_args.target_host
   pinger = Pinger(target_host=target_host)
   pinger.ping()