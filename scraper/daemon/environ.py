# -*- coding: utf-8 -*-

import datetime
import os

from w3lib.url import path_to_file_uri
from zope.interface import implements

from scraper.daemon import SCRAPY_SETTINGS_MODULE
from .interfaces import IEnvironment

class Environment(object):

	implements(IEnvironment)

	def __init__(self, settings, initenv=os.environ):
		self.logs_dir = settings.get('DAEMON_LOGS_DIR', 'logs')
		self.logs_filename = settings.get('LOG_FILE', '')
		self.jobs_to_keep = settings.getint('DAEMON_JOBS_TO_KEEP', 5)
		self.initenv = initenv

	def get_environment(self, message, slot):
		env = self.initenv.copy()
		env['SCRAPY_SLOT'] = str(slot)
		env['SCRAPY_PROJECT'] = message['_project']
		env['SCRAPY_SPIDER'] = message['_spider']
		env['SCRAPY_JOB'] = message['_job']
		env['SCRAPY_SETTINGS_MODULE'] = SCRAPY_SETTINGS_MODULE
		if self.logs_dir:
			env['SCRAPY_LOG_FILE'] = self._get_log_file(message)
		return env

	def _get_log_file(self, message):
		"""Combine the logs_dir and logs_filename config items, and substitute
		any variables in logs_filename to get the full filename of the log file
		"""
		if not self.logs_filename:
			# if no filename specified, fall back on the default.
			return self._get_file(message, self.logs_dir, 'log')

		now = datetime.datetime.now()
		format_args = {}
		format_args['project'] = message['_project']
		format_args['spider'] = message['_spider']
		format_args['Y'] = now.year
		format_args['m'] = now.month
		format_args['d'] = now.day
		format_args['H'] = now.hour
		format_args['M'] = now.minute
		format_args['S'] = now.second
		filename = self.logs_filename.format(**format_args)

		full_filename = os.path.join(self.logs_dir, filename)

		log_dir = os.path.dirname(full_filename)
		if not os.path.exists(log_dir):
			os.makedirs(log_dir)

		return full_filename

	def _get_file(self, message, dir, ext):
		logsdir = os.path.join(dir, message['_project'], message['_spider'])
		if not os.path.exists(logsdir):
			os.makedirs(logsdir)
		to_delete = sorted((os.path.join(logsdir, x) for x in \
			os.listdir(logsdir)), key=os.path.getmtime)[:-self.jobs_to_keep]
		for x in to_delete:
			os.remove(x)
		return os.path.join(logsdir, "%s.%s" % (message['_job'], ext))
