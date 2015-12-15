# -*- coding: utf-8 -*-

import pymongo

from scraper.items import MongoItem

class MongoDBPipeline(object):
	def __init__(self, host, port, db_name):
		self.host = host
		self.port = port
		self.db_name = db_name

	@classmethod
	def from_crawler(cls, crawler):
		settings = crawler.settings
		host = settings.get('MONGO_HOST', 'localhost')
		port = settings.get('MONGO_PORT', 27017)
		db_name = settings.get('MONGO_DB_NAME', 'test')
		return cls(host, port, db_name)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(host=self.host, port=self.port)
		self.db = self.client[self.db_name]

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		if isinstance(item, MongoItem):
			item.do_process(self.db)
		return item
