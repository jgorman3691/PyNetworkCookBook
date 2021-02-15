#!/usr/bin/env python3

import subprocess
import shlex

command_line = "ping -c 5 www.google.com"
args = shlex.split(command_line)
try:
   subprocess.check_call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   print("Google Web Server is up!")
except subprocess.CalledProcessError as e:
   print("Failed to get ping.  Error number:", e)