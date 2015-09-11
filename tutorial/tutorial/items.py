# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SOQuestionItem(scrapy.Item):
	question_id = scrapy.Field()
	question_title = scrapy.Field()
	issue_time = scrapy.Field()