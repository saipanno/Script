#/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#    multiexpect.py,
#
#          multi Starter for expect script. 
#
#
#    Created by Ruoyan Wong on 2012/11/06.


import sys
import subprocess
from multiprocessing import Pool

def usage():

    print """
    Usage:

        python multiexpect.py expect_commands.exp host-address.txt [task_file]"

    """

def start_expect_script(command):
    try:
        do = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        print 'Run command: %s fail.' % command

if __name__ == '__main__':

    # Globals Variable.
    MAX_PROCESSES = 200

    try:
        script = sys.argv[1]
        target = sys.argv[2]
    except Exception, e:
        usage()
        sys.exit(1)

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
        else:
            usage()
            sys.exit(1)
        pool.apply_async(start_expect_script, (command, ))

    pool.close()
    pool.join()
