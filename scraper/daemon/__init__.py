# -*- coding: utf-8 -*-

import os

from scrapy.utils.project import ENVVAR, get_project_settings
from scrapy.utils.python import stringify_dict, unicode_to_str

SCRAPY_PROJECT = 'scraper'
SCRAPY_SETTINGS_MODULE = 'scraper.settings'


def get_scraper_settings():
    if ENVVAR not in os.environ:
        os.environ[ENVVAR] = SCRAPY_SETTINGS_MODULE
    return get_project_settings()


def get_crawl_args(message):
    """
    Return the command-line arguments to use for the scrapy crawl process
    that will be started for this message
    """
    msg = message.copy()
    args = [unicode_to_str(msg['_spider'])]
    del msg['_project'], msg['_spider']
    settings = msg.pop('settings', {})
    for k, v in stringify_dict(msg, keys_only=False).items():
        args += ['-a']
        args += ['%s=%s' % (k, v)]
    for k, v in stringify_dict(settings, keys_only=False).items():
        args += ['-s']
        args += ['%s=%s' % (k, v)]
    return args
