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


def remote_runner_by_ssh(host, script_template, data, config, fruit):

    """
    :Return Code Description:

        0: PING SUCCESS(SUCCESS)
        1: PING FAIL(TIMEOUT)

        0: SSH SUCCESS(SUCCESS)
        1: SSH FAIL(TIMEOUT, RESET, NO_ROUTE)
        2: SSH AUTHENTICATE FAIL(验证错误, 密钥格式错误, 密钥无法找到)
        3: COMMAND EXECUTE TIMEOUT(脚本执行超时)
        4: COMMAND EXECUTE FAIL(脚本中途失败)

        10: NETWORK ERROR(ADDRESS ERROR)

        20: OTHER ERROR
        100: DEFAULT

        SSH认证是先看private_key，后看password.
    """

    template = Template(script_template)
    script = template.render(data.get(host, dict()))

    ssh_prefix = 'sudo ssh %s@%s' % (config['user'], host)

    for oneline_cmd in script.split('\n'):

        try:
            r = subprocess_caller('%s %s' % (ssh_prefix, oneline_cmd))
        except Exception, e:
            fruit[host] = dict(code=2,
                               error_message=e,
                               message='')
        else:
            fruit[host] = dict(code=r.code,
                               error_message=r.error,
                               message=r.output)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('target',
                        help='hostname or address file')
    parser.add_argument('-u', dest='user',
                        help='Username when making SSH connections, (default: %(default)s)', default='root')
    parser.add_argument('-p', dest='password',
                        help='Password when making SSH connections')
    parser.add_argument('-i', dest='private',
                        help='Private key when making SSH connections, (default: %(default)s)',
                        default='%s/.ssh/saipanno_rsa' % os.environ['HOME'])
    parser.add_argument('-P', dest='port',
                        help='Port when making SSH connections, (default: %(default)s)', default=22, type=int)
    parser.add_argument('-d', dest='logdir',
                        help='Syslog directory, (default: %(default)s)', default='%s/logging' % os.environ['HOME'])
    parser.add_argument('-r', dest='proc',
                        help='Process number, (default: %(default)s)', default=250, type=int)
    parser.add_argument('-f', dest='script',
                        help='Script or template script file')
    parser.add_argument('-v', dest='variable',
                        help='Env for template file')
    config = vars(parser.parse_args())

    sub_directory = '%s/%s' % (config['logdir'], time.strftime('%Y%m%d%H%M%S'))
    try:
        os.makedirs(sub_directory)
        for f in os.listdir(config['logdir']):
            if f.endswith('.txt'):
                shutil.move(os.path.join(config['logdir'], f), sub_directory)
    except (OSError, shutil.Error):
        print('Failed to initialize the log dir.')
        sys.exit(1)

    hosts = list()
    with open(config['target']) as f:
        for oneline in f:
            hosts.append(oneline.rstrip())

    script_template = str()
    with open(config['script']) as f:
        script_template = '\n'.join(oneline.rstrip() for oneline in f)

    template_data = dict()
    if config['variable'] is not None and os.path.isfile(config['variable']):
        with open(config['variable']) as f:
            for oneline in f:
                try:
                    address = oneline.split("|")[0]
                    data = oneline.split("|")[1]
                    template_data[address] = dict()
                    for var in data.split(","):
                        k, v = var.split("=")
                        template_data[address][k.strip()] = v.strip()
                except ValueError:
                    pass

    manager = Manager()
    final_result = manager.dict()

    pool = Pool(processes=config['proc'])

    jobs = list()

    for host in hosts:
        pool.apply_async(remote_runner_by_ssh, (host, script_template, config, final_result))

    print final_result