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
import sys
import time
import subprocess
from multiprocessing import Pool
from argparse import ArgumentParser

def running_command(command):
    try:
        do = subprocess.call('%s >> /dev/null 2>&1' % command, shell=True)
    except Exception:
        pass

if __name__ == '__main__':

    MAX_PROCESSES = 200
    LOG_DIRECTORY = '%s/logging' % os.environ['HOME']

    parser = ArgumentParser(description='Process some integers.')
    parser.add_argument('-p', dest='port',     help='ssh port, (default: %(default)s)', type=int, default=22    )
    parser.add_argument('-u', dest='username', help='user name, (default: %(default)s)',          default='root')
    parser.add_argument('-f', dest='target',   help='server address', required=True )
    parser.add_argument('-i', dest='secret',   help='identity file')
    parser.add_argument('-s', dest='shadow',   help='password file')
    parser.add_argument('-e', dest='script',   help='script want to run')
    args = parser.parse_args()

    sys.exit(1)

    try:
        script = sys.argv[1]
        target = sys.argv[2]
    except Exception:
        print "Usage:\n    python multiexpect.py expect_commands.exp host-address.txt [task_file]"
        sys.exit(1)

    subdirectories = '%s/%s' % (LOG_DIRECTORY, time.strftime("%Y%m%d%H%M"))
    running_command('mkdir -p %s' % subdirectories)
    running_command('mv -f %s/*.ssh %s' % (LOG_DIRECTORY, subdirectories))
    running_command('mv -f %s/*.txt %s' % (LOG_DIRECTORY, subdirectories))
    running_command('mv -f %s/*.ping %s' % (LOG_DIRECTORY, subdirectories))

    file = open(target)
    hosts = list()
    for oneline in file:
        oneline = oneline.rsplit()[0]
        hosts.append(oneline.split(','))
    file.close()

    pool = Pool(processes=MAX_PROCESSES)

    for host in hosts:
        if len(sys.argv) == 4:
            tasks  = sys.argv[3]
            command = 'expect %s u %s h %s e %s' % (username, script, host[0], tasks)
        elif len(sys.argv) == 3:
            command = 'expect %s h %s' % (script, host[0])
        pool.apply_async(running_command, (command, ))

    pool.close()
    pool.join()
