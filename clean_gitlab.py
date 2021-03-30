#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#    multichecking,
#
#         socket或ping并发测试脚本
#
#
#    Created by Ruoyan Wong on 2021/03/30.

import json
import requests

try:
    from loguru import logger
except ImportError:

    import logging
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y%m%d%H%M',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

GITLAB_DOMAIN = ''
GITLAB_ID = 0
GITLAB_USERNAME = ''
GITLAB_TOKEN = ''


def pprint(data):
    logger.info(json.dumps(data, indent=4, sort_keys=True))


def main():

    URL = 'http://%s/api/v4/users/%d/projects?private_token=%s' % (
        GITLAB_DOMAIN, GITLAB_ID, GITLAB_TOKEN)

    data = requests.get(URL).json()
    for item in data:
        if item.get('owner', {}).get('username') == GITLAB_USERNAME:
            logger.info('%s(%d) is owner, try delete' %
                        (item['path_with_namespace'], item['id']))

            URL = 'http://%s/api/v4/projects/%d?private_token=%s' % (
                GITLAB_DOMAIN, item['id'], GITLAB_TOKEN)
            data = requests.delete(URL).json()
            if data.get('message', '') == '202 Accepted':
                logger.info('%s(%d) is owner, delete success' %
                            (item['path_with_namespace'], item['id']))
                continue

        logger.warn('%s(%d) is unknown type' %
                    (item['path_with_namespace'], item['id']))


if __name__ == '__main__':
    main()