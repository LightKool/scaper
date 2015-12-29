# -*- coding: utf-8 -*-
#!/usr/bin/env python

from twisted.scripts.twistd import run
from os.path import join, dirname
from sys import argv
from scraper import daemon

def main():
    argv[1:1] = ['-y', join(dirname(daemon.__file__), 'tac.py')]
    run()
