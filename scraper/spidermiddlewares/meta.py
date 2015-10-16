# -*- coding: utf-8 -*-

from scrapy.http import Request

class RequestMetaMiddleware(object):
	@classmethod
	def from_crawler(cls, crawler):
		return cls()

	def process_spider_output(self, response, result, spider):
		for request in result:
			if isinstance(request, Request):
				request.meta['crawlid'] = response.meta['crawlid']
				if 'maxdepth' in response.meta:
					request.meta['maxdepth'] = response.meta['maxdepth']
				# set the priority
				priority = response.meta['priority'] - 10
				request.priority = priority
				request.meta['priority'] = priority
				# set link extractor related values
				request.meta['allow'] = response.meta['allow']
				request.meta['deny'] = response.meta['deny']
				request.meta['allow_domains'] = response.meta['allow_domains']
				request.meta['deny_domains'] = response.meta['deny_domains']
				request.meta['restrict_xpaths'] = response.meta['restrict_xpaths']
				request.meta['restrict_css'] = response.meta['restrict_css']
			yield request
