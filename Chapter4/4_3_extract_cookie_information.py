#!/usr/bin/env python3

import http
from http import cookiejar as cookie
import urllib
from urllib import request as rqt
from urllib import parse as prs
import certifi, ssl

ID_NAME = 'ap_customer_name'
ID_USERNAME = 'ap_mail'
ID_PASSWORD = 'ap_password'
ID_PCHECK = 'ap_password_check'
USERNAME = 'xeno3691@gmail.com'
PASSWORD = 'DaylightTripping6969!'
LOGIN_URL = 'https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&'
NORMAL_URL = 'https://www.amazon.com/'

def extract_cookie_info():
    # Set up the SSL Context
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile='/etc/ssl/certs/ca-certificates.crt')
    # Set up the cookie jar
    cjar = cookie.CookieJar()
    login_data = prs.urlencode({ ID_USERNAME : USERNAME, ID_PASSWORD: PASSWORD})

    """Now we create the URL opener, and then send the login info"""
    opener = rqt.build_opener(rqt.HTTPSHandler(context=context, check_hostname=True), rqt.HTTPCookieProcessor(cjar))
    response = opener.open(LOGIN_URL, login_data.encode())

    # Now we send the login info
    for cmon in cjar:
        print(f'----First time cookie: {cmon.name} --> {cmon.value}')
    print(f'Headers: {response.headers}')

    # Now we access without any login info
    response = opener.open(NORMAL_URL)
    for cmon in cjar:
        print(f'++++Second time cookie: {cmon.name} -->  {cmon.value}')
    print(f'Headers: {response.headers}')

if __name__ == '__main__':
    extract_cookie_info()
