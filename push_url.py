# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, json
import redis

from scrapy.spiderloader import SpiderLoader

from scraper.daemon import get_scraper_settings

class UrlPusher(object):

	def __init__(self):
		settings = get_scraper_settings()
		loader = SpiderLoader.from_settings(settings)
		self.spider_names = loader.list()
		self.server = redis.StrictRedis(host=settings.get('REDIS_HOST'), port=settings.get('REDIS_PORT'))

	def has_spider(self, spider_name):
		return spider_name in self.spider_names

	def push(self, spider_name, *urls):
		key = spider_name + ':queue'
		for url in urls:
			data = json.dumps({'url': url})
			self.server.zadd(key, **{data: 0})

if __name__ == '__main__':
	argv = sys.argv[1:]

	if len(argv) < 2:
		print 'Usage: python push_url.py [spider_name] "[urls]"...'
		print ''
		print 'Example:'
		print '    python push_url.py spider "www.google.com" "www.facebook.com"'
		sys.exit(0)
	else:
		spider_name = argv[0]
		pusher = UrlPusher()
		if pusher.has_spider(spider_name):
			pusher.push(spider_name, *argv[1:])
			sys.exit(0)
		else:
			print "Spider: [%s] doesn't exist!" % spider_name
			sys.exit(1)