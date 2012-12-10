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
from re import search
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
    LOG_DIRECTORY = '%s/logging' % HOME

    parser = ArgumentParser()
    parser.add_argument('-c', dest='script',   help='expect script', required=True)
    parser.add_argument('-f', dest='target',   help='server list', required=True)
    parser.add_argument('-u', dest='username', help='username, (default: %(default)s)', default='root')
    parser.add_argument('-p', dest='port',     help='port, (default: %(default)s)', default=22)
    parser.add_argument('-l', dest='log',      help='log level to record, (default: %(default)s)', default='stat')
    parser.add_argument('-i', dest='secret',   help='user identity file, (default: %(default)s)', default='%s/.ssh/id_rsa' % HOME)
    parser.add_argument('-s', dest='shadow',   help='user password file, (default: %(default)s)', default='%s/.ssh/password' % HOME)
    parser.add_argument('-b', dest='procs',    help='max process number, (default: %(default)s)', default=250)
    ssh_checking_group = parser.add_argument_group('SCRIPT:ssh_checking')
    run_commands_group = parser.add_argument_group('SCRIPT:run_commands')
    run_commands_group.add_argument('-e', dest='commands', help='commands file')
    opts = vars(parser.parse_args())

    subdirectories = '%s/%s' % (LOG_DIRECTORY, strftime("%Y%m%d%H%M"))
    running_command('mkdir -p %s' % subdirectories)
    running_command('mv -f %s/*.txt %s' % (LOG_DIRECTORY, subdirectories))
    running_command('mv -f %s/*.stat %s' % (LOG_DIRECTORY, subdirectories))

    file = open(opts['target'])
    hosts = list()
    for oneline in file:
        hosts.append(oneline.rsplit()[0])
    file.close()

    pool = Pool(processes=opts['procs'])

    for host in hosts:
        if search('ssh_checking.exp', opts['script']) is not None: 
            command = 'expect %s u %s h %s p %s i %s s %s' % (opts['script'], opts['username'], host, opts['port'], opts['secret'], opts['shadow'])
        elif search('run_commands.exp', opts['script']) is not None: 
            command = 'expect %s u %s h %s p %s i %s s %s e %s' % (opts['script'], opts['username'], host, opts['port'], opts['secret'], opts['shadow'], opts['commands'])
        pool.apply_async(running_command, (command, ))

    pool.close()
    pool.join()
