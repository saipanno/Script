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

    TIMEOUT = 15
    HOME = os.environ['HOME']
    AUTO_EXPECT = '%s/bin/auto_login.expect' % HOME

    opts = dict()
    if re.search('ssh.ku', sys.argv[0]) is not None:
        opts['port'] = 22
        opts['username'] = 'root'
        opts['secret'] = '%s/.ssh/id_rsa.ku' % HOME
        opts['shadow'] = '%s/.ssh/password.ku' % HOME
    elif re.search('ssh.kr', sys.argv[0]) is not None:
        opts['port'] = 22
        opts['username'] = 'sndawangruoyan'
        opts['address'] = '122.11.32.36'
        opts['secret'] = '%s/.ssh/id_rsa' % HOME
        opts['shadow'] = '%s/.ssh/password' % HOME
    elif re.search('ssh.hc', sys.argv[0]) is not None:
        opts['port'] = 7035
        opts['username'] = 'root'
        opts['address'] = '106.187.89.40'
        opts['secret'] = '%s/.ssh/id_rsa' % HOME
        opts['shadow'] = '%s/.ssh/password' % HOME

    parser = ArgumentParser()
    parser.add_argument('-a', dest='address',  help='server address')
    parser.add_argument('-u', dest='username', help='username')
    parser.add_argument('-p', dest='port',     help='port')
    parser.add_argument('-i', dest='secret',   help='user identity file')
    parser.add_argument('-s', dest='shadow',   help='user password file')

    for key,value in vars(parser.parse_args()).items():
        if value is not None:
            opts[key] = value

    command = 'expect %s o %s u %s a %s p %s i %s s %s t %s' % (AUTO_EXPECT, 'interact', opts['username'], opts['address'], opts['port'], opts['secret'], opts['shadow'], TIMEOUT)
    subprocess.call('%s' % command, shell=True)
