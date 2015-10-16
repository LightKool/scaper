# -*- coding: utf-8 -*-

# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy import signals
from scrapy.spiders import Spider
from scrapy.exceptions import DontCloseSpider


class RedisMixin(object):
	def setup(self):
		self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

	def make_requests_from_url(self, url):
		'''
		Override the make_requests_from_url method to set the default crawlid.
		Useful for hard code spider implementations.
		'''
		request = super(RedisMixin, self).make_requests_from_url(url)
		if 'crawlid' not in request.meta:
			request.meta['crawlid'] = 'default'
		return request

	def spider_idle(self):
		# The spider won't be stopped after idle
		raise DontCloseSpider

class RedisSpider(RedisMixin, Spider):
	'''
	Base spider to process distributed crawls backed by Redis from
	which all spiders in this project should subclass.
	'''
	def _set_crawler(self, crawler):
		super(RedisSpider, self)._set_crawler(crawler)
		self.setup()
