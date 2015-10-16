# -*- coding: utf-8 -*-

import scrapy

class SOQuestionItem(scrapy.Item):
	question_id = scrapy.Field()
	question_title = scrapy.Field()
	issue_time = scrapy.Field()