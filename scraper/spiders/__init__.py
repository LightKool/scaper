# -*- coding: utf-8 -*-

# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy import signals
from scrapy.spiders import Spider
from scrapy.exceptions import DontCloseSpider


class RedisSpider(Spider):
	'''
	Base spider to process distributed crawls backed by Redis from
	which all spiders in this project should subclass.
	'''
	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(RedisSpider, cls).from_crawler(crawler, *args, **kwargs)
		spider.on_crawler_set()

	def set_crawler(self, crawler):
		super(RedisSpider, self).set_crawler(crawler)
		self.on_crawler_set()

	def on_crawler_set(self):
		self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

	def spider_idle(self):
		# The spider won't be stopped after idle
		raise DontCloseSpider

	def make_requests_from_url(self, url):
		'''
		Override the make_requests_from_url method to set the default crawlid.
		Useful for hard code spider implementations.
		'''
		request = super(RedisSpider, self).make_requests_from_url(url)
		if 'crawlid' not in request.meta:
			request.meta['crawlid'] = 'default'
		return request