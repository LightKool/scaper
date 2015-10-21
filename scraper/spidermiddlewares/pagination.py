# -*- coding: utf-8 -*-

# Utilities to handle pagination links following combined with scrapy.spiders.CrawlSpider.

from scrapy.http import Request

class FollowPaginationMiddleware(object):
	"""
	This spider middleware is used to control the follow behavior of pagination
	links. It could be combined with scrapy.spiders.CrawlSpider to automatically
	follow pagination links.
	"""
	def __init__(self, maxpages):
		self.maxpages = maxpages

	@classmethod
	def from_crawler(cls, crawler):
		settings = crawler.settings
		maxpages = settings.getint('PAGINATION_MAX_PAGES')
		return cls(maxpages)

	def process_spider_output(self, response, result, spider):
		def _filter(request):
			if isinstance(request, Request) and response.meta.get('pagination_link', False):
				page_count = response.meta.get('page_count', 1) + 1
				request.meta['page_count'] = page_count
				if self.maxpages and page_count > self.maxpages:
					return False
				elif response.meta.get('depth', 0) > 0:
					# disallow depth limitation when following pagination links
					response.meta['depth'] = response.meta['depth'] - 1
			return True

		return (r for r in result or () if _filter(r))

def PaginationRule(rule):
	"""
	Wrap the scrapy.spiders.Rule to make it automatically follow pagination links.
	"""
	pr = rule.process_request
	def _pr(request):
		request.meta['pagination_link'] = True
		return pr(request)
	rule.process_request = _pr
	return rule