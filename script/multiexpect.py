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
    AUTO_EXPECT = '%s/bin/auto_login.exp' % HOME

    parser = ArgumentParser()
    parser.add_argument('-o', dest='operate',  help='operate to do', required=True)
    parser.add_argument('-f', dest='target',   help='server address file', required=True)
    parser.add_argument('-u', dest='username', help='username, (default: %(default)s)', default='root')
    parser.add_argument('-p', dest='port',     help='port, (default: %(default)s)', default=22)
    parser.add_argument('-l', dest='logdir',   help='log directory, (default: %(default)s)', default='%s/logging' % HOME)
    parser.add_argument('-i', dest='secret',   help='user identity file, (default: %(default)s)', default='%s/.ssh/id_rsa' % HOME)
    parser.add_argument('-s', dest='shadow',   help='user password file, (default: %(default)s)', default='%s/.ssh/password' % HOME)
    parser.add_argument('-b', dest='procs',    help='max process number, (default: %(default)s)', default=250)
    parser.add_argument('-t', dest='timeout',  help='timeout second, (default: %(default)s)', default=45)
    ssh_checking_group = parser.add_argument_group('SCRIPT:ssh_checking')
    run_commands_group = parser.add_argument_group('SCRIPT:run_commands')
    run_commands_group.add_argument('-c', dest='commands', help='remote command file')
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

    for host in hosts:
        if opts['operate'] == "test": 
            command = 'expect %s o %s u %s a %s p %s i %s s %s d %s t %s' % (AUTO_EXPECT, opts['operate'], opts['username'], host, opts['port'], opts['secret'], opts['shadow'], opts['logdir'], opts['timeout'])
        elif opts['operate'] == "run": 
            command = 'expect %s o %s u %s a %s p %s i %s s %s d %s t %s c %s' % (AUTO_EXPECT, opts['operate'], opts['username'], host, opts['port'], opts['secret'], opts['shadow'], opts['logdir'], opts['timeout'], opts['commands'])
        pool.apply_async(running_command, (command, ))

    pool.close()
    pool.join()
