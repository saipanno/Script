#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ruoyan Wong(@saipanno).
#
#                    Created at 2013/12/31.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import sys
import time
import shutil
import argparse
import subprocess
from jinja2 import Template
from multiprocessing import Pool, Manager


def subprocess_caller(cmd):

    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = p.communicate()
        code = p.returncode
    except (OSError, ValueError), e:
        return dict(output=str(), error=e, code=1)
    else:
        return dict(output=output, error=error, code=code)


def remote_runner_by_ssh(host, templates, env, share_dict):

    for template in templates:

        script_template = Template(template)
        script = script_template.render(env)

        r = subprocess_caller('sudo ssh %s %s' % (host, script))

        if share_dict.get(host, None) is None:
            share_dict[host] = dict(code=r['code'],
                                    error_message=r['error'].split('\n'),
                                    message=r['output'].split('\n'))
        elif share_dict.get(host, None) is not None and isinstance(share_dict[host], dict):
            share_dict[host]['code'] = r['code']
            share_dict[host]['error_message'].extend(r['error'].split('\n'))
            share_dict[host]['message'].extend(r['output'].split('\n'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('target',
                        help='hostname or address file')
    parser.add_argument('-d', dest='logdir',
                        help='Syslog directory, (default: %(default)s)', default='%s/logging' % os.environ['HOME'])
    parser.add_argument('-r', dest='proc',
                        help='Process number, (default: %(default)s)', default=250, type=int)
    parser.add_argument('-f', dest='script',
                        help='Script or template script file')
    parser.add_argument('-v', dest='variable',
                        help='Env for template file')
    config = vars(parser.parse_args())

    sub_directory = os.path.join(config['logdir'], time.strftime('%Y%m%d%H%M%S'))
    try:
        os.makedirs(sub_directory)
        for f in os.listdir(config['logdir']):
            if f.endswith('.txt') or f.endswith('.log'):
                shutil.move(os.path.join(config['logdir'], f), sub_directory)
    except (OSError, shutil.Error):
        print('Failed to initialize the log dir.')
        sys.exit(1)

    with open(config['target']) as f:
        hosts = [oneline.rstrip() for oneline in f]

    with open(config['script']) as f:
        template_script = [oneline.rstrip() for oneline in f]

    template_env = dict()
    if config['variable'] is not None and os.path.isfile(config['variable']):
        with open(config['variable']) as f:
            for oneline in f:
                try:
                    address = oneline.split("|")[0]
                    data = oneline.split("|")[1]
                    template_env[address] = dict()
                    for var in data.split(","):
                        k, v = var.split("=")
                        template_env[address][k.strip()] = v.strip()
                except ValueError:
                    pass

    manager = Manager()
    kitten = manager.dict()

    pool = Pool(processes=config['proc'])

    for node in hosts:
        pool.apply_async(remote_runner_by_ssh, (node, template_script, template_env.get(node, dict()), kitten))

    pool.close()
    pool.join()

    for address, x in kitten.items():
        with open(os.path.join(config['logdir'], 'status.txt'), 'a') as f:
            f.write('%s: %s\n' % (address, x.get('code', '-1')))

        for t, msgs in x.items():
            if len(msgs) > 0:
                with open(os.path.join(config['logdir'], '%s_%s.log' % (address, t)), 'a') as f:
                    for oneline in msgs:
                        f.write('%s\n' % oneline)