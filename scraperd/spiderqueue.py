from zope.interface import implements

from scraperd.interfaces import ISpiderQueue
from scraper.redis_scrapy.queues import RedisPriorityQueue

import redis

class RedisSpiderQueue(object):

	implements(ISpiderQueue)

	def __init__(self, config):
		redis_host = config.get('redis_host')
		redis_port = config.getint('redis_port', 6379)
		server = redis.StrictRedis(host=redis_host, port=redis_port)
		self.q = RedisPriorityQueue(server, 'scraperd:spider:queue')

	def add(self, name, **spider_args):
		d = spider_args.copy()
		d['name'] = name
		priority = float(d.pop('priority', 0))
		self.q.push(d, priority)

	def pop(self):
		return self.q.pop()

	def count(self):
		return len(self.q)
