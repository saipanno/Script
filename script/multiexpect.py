#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#    multiexpect.py,
#
#         expect并发执行脚本 
#
#
#    Created by Ruoyan Wong on 2012/11/06.

import os
import subprocess
from time import strftime
from multiprocessing import Pool
from argparse import ArgumentParser

def running_command(command):
    try:
        do = subprocess.call('%s >> /dev/null 2>&1' % command, shell=True)
    except Exception:
        pass

if __name__ == '__main__':

    HOME = os.environ['HOME']
    AUTO_EXPECT = '%s/bin/auto_login.expect' % HOME

    parser = ArgumentParser()
    parser.add_argument('target',   help='server address file')
    parser.add_argument('-o', dest='operate',  help='operate type, (support: run, test)', required=True)
    parser.add_argument('-u', dest='user',     help='user, (default: %(default)s)', default='root')
    parser.add_argument('-p', dest='port',     help='port, (default: %(default)s)', default=22)
    parser.add_argument('-d', dest='logdir',   help='log directory, (default: %(default)s)', default='%s/logging' % HOME)
    parser.add_argument('-i', dest='secret',   help='identity file, (default: %(default)s)', default='%s/.ssh/id_rsa' % HOME)
    parser.add_argument('-s', dest='shadow',   help='password file, (default: %(default)s)', default='%s/.ssh/password' % HOME)
    parser.add_argument('-b', dest='procs',    help='process number, (default: %(default)s)', default=250, type=int)
    parser.add_argument('-t', dest='timeout',  help='timeout, (default: %(default)s)', default=45)
    run_commands_group = parser.add_argument_group('OPERATE: run')
    run_commands_group.add_argument('-c', dest='commands', help='remote command file, required')
    opts = vars(parser.parse_args())

    subdirectories = '%s/%s' % (opts['logdir'], strftime("%Y%m%d%H%M"))
    running_command('mkdir -p %s' % subdirectories)
    running_command('mv -f %s/*.txt %s' % (opts['logdir'], subdirectories))
    running_command('mv -f %s/*.stat %s' % (opts['logdir'], subdirectories))

    hosts = list()
    file = open(opts['target'])
    for oneline in file:
        hosts.append(oneline.rsplit()[0])
    file.close()

    pool = Pool(processes=opts['procs'])

    COMMAND = 'expect %s' % AUTO_EXPECT

    for key,value in opts.items():
        if key == 'operate' and value is not None:
            COMMAND = '%s o %s' % (COMMAND, value)
        elif key == 'user' and value is not None:
            COMMAND = '%s u %s' % (COMMAND, value)
        elif key == 'port' and value is not None:
            COMMAND = '%s p %s' % (COMMAND, value)
        elif key == 'secret' and value is not None:
            COMMAND = '%s i %s' % (COMMAND, value)
        elif key == 'shadow' and value is not None:
            COMMAND = '%s s %s' % (COMMAND, value)
        elif key == 'logdir' and value is not None:
            COMMAND = '%s d %s' % (COMMAND, value)
        elif key == 'timeout' and value is not None:
            COMMAND = '%s t %s' % (COMMAND, value)
        elif key == 'commands' and value is not None:
            COMMAND = '%s c %s' % (COMMAND, value)

    for host in hosts:
        print '%s a %s' % (COMMAND, host) 
        pool.apply_async(running_command, ('%s a %s' % (COMMAND, host)))

    pool.close()
    pool.join()
