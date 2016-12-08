#! /usr/bin/env python
"""
This is a simple mechanize script that logs into Comcast, retrieves the usage
information, and prints it to stdout.

Requires robobrowser.

Copyright (C) 2014 Jared Hobbs
Copyright (C) 2016 Andrii Petrenko aplsms@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import sys
import re

# print "808 1024 GB 78 #b84600"
# sys.exit(0)

sys.path.append('/usr/local/lib/python2.7/site-packages')
sys.path.append('/Library/Python/2.7/site-packages')

from getpass import getpass
from netrc   import netrc

from robobrowser.browser import RoboBrowser

LOGIN = 'https://login.comcast.net/login?' +\
        'continue=%2fMyServices%2fInternet%2f&s=ccentral-cima&r=comcast.net'
SERVICES = 'https://customer.xfinity.com/MyServices/Internet'
PRELOADER = 'https://customer.xfinity.com/Secure/Preloader.aspx'
AJAX = 'https://customer.xfinity.com/MyServices/Internet?AJAX=1'
USAGE = 'https://customer.xfinity.com/MyServices/Internet/UsageMeter'

# def debug(t, v, tb):
#     import pdb
#     import traceback
#     traceback.print_exception(t, v, tb)
#     print
#     pdb.pm()

# #sys.excepthook = debug


def getBrowser():
    br = RoboBrowser(
        history=True,
        parser='html.parser',
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) '
                   'AppleWebKit/534.48.3 (KHTML, like Gecko) '
                   'Version/5.1 Safari/534.48.3'
    )
    return br


def login(br):
    try:
        n = netrc()
        username, account, password = n.authenticators('login.comcast.net')
        if None in (username, password):
            raise
    except:
        username = raw_input('Username: ')
        password = getpass()
    br.open(LOGIN)
    form = br.get_form(attrs={'name': 'signin'})
    form['user'].value = username
    form['passwd'].value = password
    br.submit_form(form)
    try:
        form = br.get_form(attrs={'name': 'signin'})
        form['passwd'].value = password
        br.submit_form(form)
    except:
        pass
    try:
        form = br.get_form(attrs={'name': 'redir'})
    except:
        raise Exception('Failed to login')
    br.submit_form(form)


def printBandwidthUsage(br):
    br.open(PRELOADER)
    br.open(USAGE)
    try:
        result = br.select('.cui-usage-label')[1].text
    except:
        print result
        raise Exception('Failed to get usage')

    try:
        matches = re.finditer(r"(\d+)GB of (\d+)GB", result).next()
    except:
        print "Failed to determine usage"
        sys.exit(1)

    val     = int(matches.group(1))
    limit   = int(matches.group(2))
    percent = int(val)/10.24

    print "%d of %d GB %d %s" % (val, limit, percent, coloring(percent))

def coloring(prc):
    trLow=50
    trHigh=90
    if prc <= trLow :
        return "#%02x%02x%02x" % (0,255,0)
    elif prc >= trHigh :
        return "#%02x%02x%02x" % (255,0,0)
    else:
        R =  int((prc-trLow)*255/(trHigh-trLow))
        G =  int((trHigh-prc)*255/(trHigh-trLow))
        return "#%02x%02x%02x" % (R, G, 0)



def main():
    br = getBrowser()
    login(br)
    printBandwidthUsage(br)



if __name__ == '__main__':
    main()

