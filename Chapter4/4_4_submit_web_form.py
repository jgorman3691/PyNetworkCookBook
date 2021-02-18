#!/usr/bin/env python3

import http
import urllib
import ssl
from http import client
from http import server
from urllib import requests as rqt
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
   response = rqt.do_GET(payload)