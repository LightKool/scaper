# -*- coding: utf-8 -*-

import redis
from zope.interface import implements

from scraper.core.queues import RedisPriorityQueue
from .interfaces import ISpiderQueue

class RedisSpiderQueue(object):

	implements(ISpiderQueue)

	def __init__(self, settings):
		redis_host = settings.get('REDIS_HOST')
		redis_port = settings.getint('REDIS_PORT', 6379)
		server = redis.StrictRedis(host=redis_host, port=redis_port)
		self.queue = RedisPriorityQueue(server, 'scraperd:spider:queue')

	def add(self, name, **spider_args):
		d = spider_args.copy()
		d['name'] = name
		priority = float(d.pop('priority', 0))
		self.queue.push(d, priority)

	def pop(self):
		return self.queue.pop()

	def count(self):
		return len(self.queue)
