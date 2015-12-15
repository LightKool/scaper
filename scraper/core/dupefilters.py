# -*- coding: utf-8 -*-

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

class RedisRFPDupefilter(BaseDupeFilter):
	def __init__(self, server, key, timeout):
		self.server = server
		self.key = key
		self.timeout = timeout

	def request_seen(self, request):
		fp = request_fingerprint(request)
		crawlid = request.meta['crawlid']
		key = self.key + ':' + crawlid

		added = self.server.sadd(key, fp)
		self.server.expire(key, self.timeout)
		return not added

	def close(self):
		self.clear()

	def clear(self):
		# eaglerly delete all related keys of the duplication filter
		for key in self.server.scan_iter(match=self.key + ':*'):
			self.server.delete(key)

# TODO: duplication filter based on bloom filter to
# reduced the memory consumption
class RedisBFDupefilter(BaseDupeFilter):
	pass

__all__ = ['RedisRFPDupefilter']
