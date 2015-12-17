# -*- coding: utf-8 -*-

from scraper.spiders import RedisMixin

class RequestMetaMiddleware(object):
	"""Downloader middleware to set some mandatory metadata."""

	@classmethod
	def from_crawler(cls, crawler):
		return cls()

	def process_request(self, request, spider):
		# set default crawlid for redis backed spiders
		if isinstance(spider, RedisMixin) and 'crawlid' not in request.meta:
			request.meta['crawlid'] = 'default'
