#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#    multiexpect.py,
#
#          multi Starter for expect script. 
#
#
#    Created by Ruoyan Wong on 2012/11/06.

import os
import sys
import time
import subprocess
from multiprocessing import Pool, Manager

def running_command(command):
    try:
        do = subprocess.call('%s >> /dev/null 2>&1' % command, shell=True)
    except Exception:
        pass

if __name__ == '__main__':

    # Globals Variable.
    MAX_PROCESSES = 250

    try:
        script = sys.argv[1]
        target = sys.argv[2]
    except Exception:
        print "Usage:\n    python multiexpect.py expect_commands.exp host-address.txt [task_file]"
        sys.exit(1)

    bakup_logging_dir = '%s/logging/%s' % (os.environ['HOME'], time.strftime("%Y%m%d%H%M"))
    running_command('mkdir -p %s' % bakup_logging_dir)
    running_command('mv -f %s/logging/*.ssh %s' % (os.environ['HOME'], bakup_logging_dir))
    running_command('mv -f %s/logging/*.txt %s' % (os.environ['HOME'], bakup_logging_dir))
    running_command('mv -f %s/logging/*.ping %s' % (os.environ['HOME'], bakup_logging_dir))

    file = open(target)
    hosts = list()
    for oneline in file:
        oneline = oneline.rsplit()[0]
        hosts.append(oneline.split(','))
    file.close()

    pool = Pool(processes=MAX_PROCESSES)

    for host in hosts:
        # host = [address]
        if len(sys.argv) == 4:
            tasks  = sys.argv[3]
            command = 'expect %s %s %s' % (script, host[0], tasks)
        elif len(sys.argv) == 3:
            command = 'expect %s %s' % (script, host[0])
        pool.apply_async(running_command, (command, ))

    pool.close()
    pool.join()
