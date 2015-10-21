# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class ElasticDocumentItem(Item):
	'''
	Base class for all items wish to be indexed/stored by ElasticSearch.
	'''
	def __init__(self, index, doc_type, doc_id, *args, **kwargs):
		super(ElasticDocumentItem, self).__init__(self, *args, **kwargs)
		self._index = index
		self._doc_type = doc_type
		self._doc_id = doc_id

	@property
	def index(self):
		return self._index

	@property
	def doc_type(self):
		return self._doc_type

	@property
	def id(self):
		return self._doc_id