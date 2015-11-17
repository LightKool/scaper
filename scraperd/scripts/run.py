#!/usr/bin/env python

from twisted.scripts.twistd import run
from os.path import join, dirname
from sys import argv
import scraperd


def main():
    argv[1:1] = ['-n', '-y', join(dirname(scraperd.__file__), 'txapp.py')]
    run()
