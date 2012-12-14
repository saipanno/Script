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
from multiprocessing import Process
from argparse import ArgumentParser

def get_status(logdir):

    subprocess.call('rm -f %s/interact.stat' % logdir, shell=True)
    while True:
        try:
            file = open('%s/interact.stat' % logdir)
            print file.readline()
            file.close()
            break
        except:
            continue

def start_expect_script(COMMAND):
    try:
        subprocess.call('%s' % COMMAND, shell=True)
    except:
        pass

if __name__ == '__main__':

    HOME = os.environ['HOME']
    AUTO_EXPECT = '%s/bin/auto_login.expect' % HOME

    opts = dict()
    if re.search('ssh.ku', sys.argv[0]) is not None:
        opts['port'] = 22
        opts['user'] = 'root'
        opts['secret'] = '%s/.ssh/id_rsa.ku' % HOME
        opts['shadow'] = '%s/.ssh/password.ku' % HOME
        opts['logdir'] = '%s/logging' % HOME

    parser = ArgumentParser() 
    parser.add_argument('address', help='server address')
    parser.add_argument('-u', dest='user',     help='user')
    parser.add_argument('-p', dest='port',     help='port')
    parser.add_argument('-i', dest='secret',   help='user identity file')
    parser.add_argument('-s', dest='shadow',   help='password file')
    parser.add_argument('-d', dest='logdir',   help='syslog directory, (default: %(default)s)', default='%s/logging' % HOME)
    parser.add_argument('-t', dest='timeout',  help='expect build-in timeout, (default: %(default)s)', default=15)

    for key,value in vars(parser.parse_args()).items():
        if value is not None:
            opts[key] = value

    COMMAND = 'expect %s o %s ' % (AUTO_EXPECT, 'interact')
    for key,value in opts.items():
        if key == 'address':
            COMMAND = '%s a %s' % (COMMAND, value)
        elif key == 'user':
            COMMAND = '%s u %s' % (COMMAND, value)
        elif key == 'port':
            COMMAND = '%s p %s' % (COMMAND, value)
        elif key == 'secret':
            COMMAND = '%s i %s' % (COMMAND, value)
        elif key == 'shadow':
            COMMAND = '%s s %s' % (COMMAND, value)
        elif key == 'logdir':
            COMMAND = '%s d %s' % (COMMAND, value)
        elif key == 'timeout':
            COMMAND = '%s t %s' % (COMMAND, value)

    workers = list()
    workers.append(Process(target=start_expect_script, args=(COMMAND, )))
    workers.append(Process(target=get_status, args=(opts['logdir'], )))

    for worker in workers: worker.start()
    for worker in workers: worker.join()
