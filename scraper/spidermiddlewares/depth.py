# -*- coding: utf-8 -*-

from scrapy.http import Request

class DepthMiddleware(object):
	'''
	Reimplementation of scrapy.spidermiddlewares.depth.DepthMiddleware
	which allow the max depth setting be overrided per crawl request.
	'''
	def __init__(self, maxdepth):
		self.maxdepth = maxdepth

	@classmethod
	def from_crawler(cls, crawler):
		settings = crawler.settings
		maxdepth = settings.getint('DEPTH_LIMIT')
		return cls(maxdepth)

	def process_spider_output(self, response, result, spider):
		def _filter(request):
			if isinstance(request, Request):
				depth = response.meta['depth'] + 1
				# get the actual maxdepth which could be overrided
				maxdepth = self.maxdepth
				if 'maxdepth' in response.meta:
					maxdepth = response.meta['maxdepth']
					request.meta['maxdepth'] = maxdepth
				if maxdepth and depth > maxdepth:
					return False

				request.meta['depth'] = depth
			return True

		# base case (depth=0)
		if 'depth' not in response.meta:
			response.meta['depth'] = 0

		return (r for r in result or () if _filter(r))
