# -*- coding: utf-8 -*-

import redis
import time, random

from dupefilters import RedisRFPDupefilter
from queues import RedisPriorityQueue

from scrapy.http import Request
from scrapy.utils.reqser import request_to_dict, request_from_dict

class RedisScheduler(object):
	def __init__(self, server, persist, timeout, retries):
		self.server = server
		self.persist = persist
		self.df_timeout = timeout
		self.item_retries = retries

	@classmethod
	def from_settings(cls, settings):
		server = redis.StrictRedis(host=settings.get('REDIS_HOST'), port=settings.get('REDIS_PORT'))
		persist = settings.get('SCHEDULER_PERSIST', False)
		timeout = settings.get('DUPEFILTER_TIMEOUT', 600)
		retries = settings.get('SCHEDULER_ITEM_RETRIES', 3)
		return cls(server, persist, timeout, retries)

	@classmethod
	def from_crawler(cls, crawler):
		return cls.from_settings(crawler.settings)

	def open(self, spider):
		'''
		Open the scheduler for the spider and initializing the queue and
		duplication filter.
		'''
		self.spider = spider
		self.queue = RedisPriorityQueue(self.server, self.spider.name + ':queue')
		self.dupefilter = RedisRFPDupefilter(self.server, self.spider.name + ':dupefilter', self.df_timeout)

	def close(self, reason):
		if not self.persist:
			self.dupefilter.clear()
			self.queue.clear()

	def has_pending_requests(self):
		return len(self.queue) > 0

	def enqueue_request(self, request):
		if not request.dont_filter and self.dupefilter.request_seen(request):
			return False
		req_dict = request_to_dict(request, self.spider)
		self.queue.push(req_dict, request.priority)
		return True

	def next_request(self):
		item = self._retrieve_from_queue()
		if item:
			try:
				request = request_from_dict(item, self.spider)
			except KeyError:
				request = self._request_from_dict(item)
			return self._populate_request(request, item)
		else:
			return None

	def _retrieve_from_queue(self):
		count = 0
		while count <= self.item_retries:
			item = self.queue.pop()
			if item:
				return item
			count = count + 1
		return None

	def _request_from_dict(self, item):
		request = Request(item['url'])
		request.meta['crawlid'] = item['crawlid']
		request.meta['maxdepth'] = item.get('maxdepth', 0)
		request.priority = item.get('priority', 0)
		request.meta['priority'] = request.priority
		return request

	def _populate_request(self, request, item):
		if 'extra' in item:
			extra = item['extra']
		else:
			extra = request.meta.copy()

		extra.setdefault('priority', request.priority)
		# link extractor related values
		extra.setdefault('allow', ())
		extra.setdefault('deny', ())
		extra.setdefault('allow_domains', ())
		extra.setdefault('deny_domains', ())
		extra.setdefault('restrict_xpaths', ())
		extra.setdefault('restrict_css', ())

		request.meta.update(extra)
		return request