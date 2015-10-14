# -*- coding: utf-8 -*-

from scrapy.http import Request

class RequestMetaMiddleware(object):
	@classmethod
	def from_crawler(cls, crawler):
		return cls()

	def process_spider_output(self, response, result, spider):
		for request in result:
			if isinstance(request, Request) and 'crawlid' in response.meta:
				request.meta['crawlid'] = response.meta['crawlid']
			yield request
