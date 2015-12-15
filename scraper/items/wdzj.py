# -*- coding: utf-8 -*-

from scrapy.item import Field

from . import ElasticDocumentItem

class WDZJNewsItem(ElasticDocumentItem):
	title = Field()
	content = Field()