#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .build_config import *


class FileUtil(object):

    try:
        config_file = open(CONFIG_FILE_PATH)
        config = json.loads(config_file.read())
        config_file.close()
    except Exception as e:
        raise ValueError(e)

    serverUrl = config['url']
    uploads = config['uploads']
    uploadsPath = config['url'] + config['uploadsPath']
    tmpPath = uploads + config['tmpUploadsPath']
