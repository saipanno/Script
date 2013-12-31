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
from fabric.api import env, run, show, hide, execute
from paramiko.ssh_exception import SSHException
from fabric.exceptions import NetworkError, CommandTimeout


def subprocess_caller(cmd):

    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = p.communicate()
        code = p.returncode
    except (OSError, ValueError):
        return dict()
    else:
        return dict(output=output, error=error, code=code)


def super_remote_runner(script_template, envs):

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
    script = template.render(envs.get(env.host, dict()))

    try:
        fruit = run(script, shell=True, quiet=True)
    except SystemExit:
        output = dict(code=2,
                      error_message='Ssh Authentication Failed',
                      message='')

    # 远程命令执行时间超过`env.command_timeout`时触发
    except CommandTimeout:
        output = dict(code=3,
                      error_message='Remote Command Execute Timeout',
                      message='')

    # 通过设定`env.disable_known_hosts = True`可以避归此问题，但在异常处理上依然保留此逻辑。
    except SSHException, e:
        if 'Invalid key' in e.__str__():
            output = dict(code=2,
                          error_message='User’s Known-Hosts Check Failed',
                          message='')
        else:
            output = dict(code=20,
                          error_message='SSHException Exception: %s' % e,
                          message='')

    # 匹配错误的密钥路径
    except IOError, e:
        if 'No such file or directory' in e.__str__():
            output = dict(code=2,
                          error_message='Ssh Private Key Not Found',
                          message='')
        else:
            output = dict(code=20,
                          error_message='IOError Exception: %s' % e,
                          message='')

    except NetworkError, e:
        # 匹配SSH连接超时
        if 'Timed out trying to connect to' in e.__str__() or 'Low level socket error connecting' in e.__str__():
            output = dict(code=1,
                          error_message='Ssh Connection Timeout',
                          message='')
        elif 'Name lookup failed for' in e.__str__():
            output = dict(code=10,
                          error_message='Incorrect Node Address',
                          message='')
        else:
            output = dict(code=20,
                          error_message='NetworkError Exception: %s' % e,
                          message='')

    except Exception, e:
        if 'Private key file is encrypted' in e.__str__():
            output = dict(code=2,
                          error_message='Private key file is encrypted',
                          message='')
        else:
            output = dict(code=20,
                          error_message='Base Exception: %s' % e,
                          message='')
    else:
        output = dict(code=fruit.return_code,
                      error_message=fruit.stderr if fruit.stderr else '',
                      message=fruit.stdout)

    return output


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

    sub_directory = '%s/%s' % (config['logdir'], time.strftime("%Y%m%d%H%M"))
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

    script = str()
    with open(config['script']) as f:
        script = '\n'.join(oneline.rstrip() for oneline in f)

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

    env.parallel = True
    env.warn_only = True
    env.disable_known_hosts = True

    env.timeout = 30
    env.command_timeout = 60

    env.pool_size = config['proc']
    env.user = config['user']
    env.password = config['password']
    env.key_filename = config['private']
    env.port = config['port']

    with show('everything'):

        fruit = execute(super_remote_runner,
                        script=script,
                        envs=template_data,
                        hosts=hosts)