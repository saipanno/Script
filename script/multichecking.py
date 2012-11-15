#/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#    multichecking,
#
#          Support ping and socket check.
#
#
#    Created by Ruoyan Wong on 2012/11/04.

import os
import sys
import time
import socket
import subprocess
from multiprocessing import Pool, Manager


def connectivity_checking(address, result, COUNT, TIMEOUT):
    command = 'ping -c%s -W%s %s' % (COUNT, TIMEOUT, address)
    try:
        connectivity = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        connectivity = -1
    finally:
        result[address] = connectivity

def socket_checking(address, port, result, TIMEOUT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    status = 0
    try:
        s.connect((address, port))
    except socket.timeout:
        status = 1
    except Exception:
        status = -1
    finally:
        s.close()
        result[address] = status


if __name__ == '__main__':

    # Globals Variable.
    COUNT = 5
    TIMEOUT = 2
    MAX_PROCESSES = 250

    try:
        item   = sys.argv[1]
        target = sys.argv[2]
    except Exception:
        print "Usage:\n\tpython multichecking.py socket|ping host-address.txt"
        sys.exit(1)

    bakup_logging_dir = '%s/logging/%s' % (os.environ['HOME'], time.strftime("%Y%m%d%H%M"))
    subprocess.call('mkdir -p %s' % bakup_logging_dir, shell=True)
    subprocess.call('mv -f %s/logging/*.txt %s' % (os.environ['HOME'], bakup_logging_dir), shell=True)       

    manager = Manager()
    kitten = manager.dict()

    file = open(target)
    tasks = list()
    for oneline in file:
        oneline = oneline.rsplit()[0]
        tasks.append(oneline.split(','))
    file.close()

    pool = Pool(processes=MAX_PROCESSES)

    jobs = list()
    if item == 'ping':
        for task in tasks:
            # task = [address]
            pool.apply_async(connectivity_checking, (task[0], kitten, COUNT, TIMEOUT))
    elif item == 'socket':
        for task in tasks:
            # task = [address, port]
            pool.apply_async(socket_checking, (task[0], int(task[1]), kitten, TIMEOUT))

    pool.close()
    pool.join()

    result_log_file = '%s/logging/checking.txt' % os.environ['HOME']
    file = open(result_log_file, 'w')
    for address in kitten.keys():
        file.write('%s : %s\n' % (address, kitten[address]))
    file.close()
