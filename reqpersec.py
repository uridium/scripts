#!/usr/bin/python

import urllib2
import getopt
import time
import sys

request = "http://localhost/server-status"
server = "nginx"
refresh = False
oneshot = False

def usage():
    print "usage: %s [-h] [-1] [-r] [-u URL]" % sys.argv[0]

try:
    opts, args = getopt.getopt(sys.argv[1:], '1hru:')
except getopt.GetoptError as msg:
    print msg
    usage()
    sys.exit(1)

for o, a in opts:
    if o == "-h":
        usage()
        print
        print "This script displays number of requests per second in nginx/apache server"
        print
        print "Options:"
        print " -h"
        print "   Print detailed help screen"
        print " -1"
        print "   Display number of requests once and exit"
        print " -r"
        print "   Refresh output instead of displaying it continously"
        print " -u"
        print "   URL of status module, eg:"
        print "   http://domain/server-status for nginx,"
        print "   http://domain/server-status?auto for apache"
        print "   ?auto is required for apache! You have been warned!"
        sys.exit(1)
    elif o == "-1":
        oneshot = True
    elif o == "-r":
        refresh = True
    elif o == "-u":
        request = a
    else:
        usage()
        sys.exit(1)

if request.endswith("?auto"):
    server = "apache"

while True:
    try:
        response1 = urllib2.urlopen(request)
        time.sleep(1)
        response2 = urllib2.urlopen(request)
    except urllib2.HTTPError as exmsg:
        print "HTTP error:", exmsg.code
        sys.exit(1)
    except urllib2.URLError as exmsg:
        print "URL error:", exmsg.reason
        sys.exit(1)
    except KeyboardInterrupt:
        sys.stdout.flush()
        sys.exit(0)
    else:
        if server == "nginx":
            line1 = response1.read().split("\n")[2]
            line2 = response2.read().split("\n")[2]
        elif server == "apache":
            line1 = response1.read().split("\n")[0]
            line2 = response2.read().split("\n")[0]

        col1 = line1.split()[2]
        col2 = line2.split()[2]
        reqpersec = int(col2) - int(col1)

        if refresh:
            sys.stdout.write("requests per second: " + str(reqpersec) + "\r")
            sys.stdout.flush()
        else:
            print reqpersec
            if oneshot:
                sys.exit(0)
