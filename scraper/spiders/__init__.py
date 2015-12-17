# -*- coding: utf-8 -*-

# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy import signals
from scrapy.spiders import Spider
from scrapy.exceptions import DontCloseSpider

class RedisMixin(object):
	'''
	Base spider to process distributed crawls backed by Redis from
	which all long-run spiders in this project should subclass.
	'''
	def _set_crawler(self, crawler):
		super(RedisMixin, self)._set_crawler(crawler)
		self.init()

	def init(self):
		pass

class RedisSpider(RedisMixin, Spider):
	def init(self):
		self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

	def spider_idle(self):
		# The spider won't be stopped after idle
		raise DontCloseSpider
