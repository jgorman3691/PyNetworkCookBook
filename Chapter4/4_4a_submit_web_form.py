#!/usr/bin/env python3

import http
import socket
import ssl
import requests
from http import client
from http import server
from urllib import request as rqt
from urllib import error as erf

ID_EMAIL = 'email'
ID_PASSWORD = 'pass'
EMAIL = 'jed.gorman@gmail.com'
PASSWORD = 'Paniagua202'
LOGIN_URL = 'https://www.facebook.com'
CA = '/etc/ssl/certs/ca-certificates.crt'

def submit_form():
   """ Submit the information to Facebook """
   payload = { ID_EMAIL: EMAIL, ID_PASSWORD: PASSWORD }
   purpose = ssl.Purpose.SERVER_AUTH
   context = ssl.create_default_context(purpose, cafile=CA)
   
   # Make a GET request
   response = requests.get(LOGIN_URL)
   print(f"Response to GET request: {response.content}")
   
   # Send a POST request
   respond = requests.post(LOGIN_URL, params=payload)
   print(f"Headers from a POST request response: {respond.headers}")
   
if __name__ == '__main__':
   submit_form()