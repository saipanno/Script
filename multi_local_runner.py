#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#    multi_local_runner.py,
#
#         本地并发执行脚本 
#
#
#    Created by Ruoyan Wong on 2013/10/10.


import os
import sys
import time
import subprocess
from jinja2 import Template
from multiprocessing import Pool, Manager
from argparse import ArgumentParser


def running_command(template, data=None, fruit=None):

    if isinstance(data, dict):
        template = Template(template)
        script = template.render(data)
    else:
        script = template

    proc = subprocess.Popen(script,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    (stdout, stderr) = proc.communicate()

    if isinstance(fruit, dict):
        fruit[data[address]] = stdout


if __name__ == '__main__':

    HOME = os.environ['HOME']

    parser = ArgumentParser()
    parser.add_argument('target', help='hostname or address file')
    parser.add_argument('-d', dest='logdir',  help='syslog directory, (default: %(default)s)', default='%s/logging' % HOME)
    parser.add_argument('-r', dest='proc',   help='process number, (default: %(default)s)', default=250, type=int)
    parser.add_argument('-s', dest='script', help='script or template script file')
    parser.add_argument('-v', dest='variable', help='variable for template file')
    config = vars(parser.parse_args())

    sub_directory = '%s/%s' % (config['logdir'], time.strftime("%Y%m%d%H%M"))
    running_command('mkdir -p %s' % sub_directory)
    running_command('mv -f %s/*.txt %s' % (config['logdir'], sub_directory))
    running_command('mv -f %s/*.stat %s' % (config['logdir'], sub_directory))

    manager = Manager()
    kitten = manager.dict()
    pool = Pool(processes=config['proc'])

    hosts = list()
    with open(config['target']) as f:
        for oneline in f:
            hosts.append(oneline.rstrip())

    script_template = str()
    with open(config['script']) as f:
        script_template = '\n'.join(oneline.rstrip() for oneline in f)

    template_data = dict()
    if config['variable'] is not None and os.path.isfile(config['variable']):
        try:
            f = open(config['variable'])
            for oneline in file:
                detail_address = oneline.split("|")[0]
                detail_information = oneline.split("|")[1]
                template_data[detail_address] = dict()
                for var in detail_information.split(","):
                    key = var.split("=")[0].strip()
                    value = var.split("=")[1].strip()
                    template_data[detail_address][key] = value
            f.close()
        except Exception, e:
            print 'get variable error: %s' % e
            sys.exit(1)

    for host in hosts:
        pool.apply_async(running_command, (script_template, template_data.get(host, dict()), kitten))

    pool.close()
    pool.join()

    for address in kitten.keys():
        with open('%s/%s.stat' % (config['logdir'], address), 'a') as f:
            for oneline in kitten[address].split('\n'):
                f.write('%s\n' % oneline)