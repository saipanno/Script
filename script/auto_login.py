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
import subprocess
from argparse import ArgumentParser

if __name__ == '__main__':

    HOME = os.e

    parser = ArgumentParser()
    parser.add_argument('-a', dest='address',  help='server address', required=True)
    parser.add_argument('-u', dest='username', help='username, (default: %(default)s)', default='root')
    parser.add_argument('-p', dest='port',     help='port, (default: %(default)s)', default=22)
    parser.add_argument('-i', dest='secret',   help='user identity file, (default: %(default)s)', default='%s/.ssh/id_rsa' % HOME)
    parser.add_argument('-s', dest='shadow',   help='user password file, (default: %(default)s)', default='%s/.ssh/password' % HOME)
    opts = vars(parser.parse_args())

    command = 'expect %s u %s h %s p %s i %s s %s' % (opts['script'], opts['username'], opts['address'], opts['port'], opts['secret'], opts['shadow'])
    subprocess.call
