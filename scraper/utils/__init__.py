# -*- coding: utf-8 -*-

import time
from scrapy.utils.python import stringify_dict

def current_milli_time():
	return int(round(time.time() * 1000))

def safe_strip(s, chars=None):
	return s.strip(chars) if s is not None and hasattr(s, 'strip') else ''

def safe_extract(sel, sep=None, extract_all=False):
	if extract_all:
		return sel.extract()
	elif sep is not None:
		return safe_strip(sep.join(sel.extract()))
	else:
		return safe_strip(sel.extract_first())

if __name__ == '__main__':
	print stringify_dict({'LOG_LEVEL': 'DEBUG'})