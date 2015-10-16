import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from . import RedisMixin
from scraper.spidermiddlewares.pagination import pagination_rule

from readability.readability import Document

class WDZJSpider(RedisMixin, CrawlSpider):
	name = 'wdzj'
	allowed_domains = ['wangdaizhijia.com']
	start_urls = ['http://www.wangdaizhijia.com/news/hangye/']

	rules = (
		Rule(LinkExtractor(allow=('/news/hangye/\d+\.html',), restrict_css=('div.specialBox',)),
			callback='parse_question'),
		pagination_rule(Rule(LinkExtractor(restrict_xpaths=('//div[@class="pageList"]/a[last()-1]',)))),
	)

	def parse_question(self, response):
		print response.url
		print Document(response.body).short_title()