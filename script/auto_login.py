#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#    auto_login.py,
#
#         expect ssh login script. 
#
#
#    Created by Ruoyan Wong on 2012/11/06.

import os
import re
import sys
import subprocess
from argparse import ArgumentParser

if __name__ == '__main__':

    HOME = os.environ['HOME']
    AUTO_EXPECT = '%s/bin/auto_login.expect' % HOME

    opts = dict()
    if re.search('ssh.ku', sys.argv[0]) is not None:
        opts['port'] = 22
        opts['username'] = 'root'
        opts['secret'] = '%s/.ssh/id_rsa.ku' % HOME
        opts['shadow'] = '%s/.ssh/password.ku' % HOME

    parser = ArgumentParser() 
    parser.add_argument('address', help='server address')
    parser.add_argument('-u', dest='user',     help='user')
    parser.add_argument('-p', dest='port',     help='port')
    parser.add_argument('-i', dest='secret',   help='identity file')
    parser.add_argument('-s', dest='shadow',   help='password file')
    parser.add_argument('-t', dest='timeout',  help='timeout', default=15)

    for key,value in vars(parser.parse_args()).items():
        if value is not None:
            opts[key] = value

    parameters = str()
    for key,value in opts.items():
        if key == 'address':
            parameters = '%s a %s' % (parameters, value)
        elif key == 'user':
            parameters = '%s u %s' % (parameters, value)
        elif key == 'port':
            parameters = '%s p %s' % (parameters, value)
        elif key == 'secret':
            parameters = '%s i %s' % (parameters, value)
        elif key == 'shadow':
            parameters = '%s s %s' % (parameters, value)
        elif key == 'timeout':
            parameters = '%s t %s' % (parameters, value)

    command = 'expect %s o %s %s' % (AUTO_EXPECT, 'interact', parameters)
    subprocess.call('%s' % command, shell=True)
