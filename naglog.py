#!/usr/bin/python
#
# view nagios log in pretty format

import time
import sys

if len(sys.argv) - 1 == 0:
    log = '/var/log/nagios/nagios.log'
else:
    log = sys.argv[1]

states = {
        ';OK;HARD':';\033[1;92mOK\033[0m;HARD', 
        ';WARNING;HARD':';\033[1;93mWARNING\033[0m;HARD', 
        ';CRITICAL;HARD':';\033[1;91mCRITICAL\033[0m;HARD', 
        ';UNKNOWN;HARD':';\033[1;94mUNKNOWN\033[0m;HARD'
        }

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

try:
    file = open(log, 'r')
except:
    print >>sys.stderr, "Can't open %s" % log
    sys.exit(1)
else:
    for line in file:
#         epoch = line[line.find("[")+1:line.find("]")]
        epoch = line[1:11]
        rest = line[13:]
        restcolor = replace_all(rest, states)
        human = time.strftime("%Y%m%d %H:%M:%S", time.localtime(int(epoch)))
        print "[%s] %s" %(human, restcolor),
    file.close()
