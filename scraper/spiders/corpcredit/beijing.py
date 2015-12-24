# -*- coding: utf-8 -*-

import re, urllib, time

from bs4 import BeautifulSoup

from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from scraper.spiders import RedisMixin
from scraper.items.corpcredit import LimitedCorpCredit
from scraper.utils import current_milli_time

class BeijingSpider(RedisMixin, Spider):
	name = 'corp_credit_beijing'
	allowed_domains = ['qyxy.baic.gov.cn']
	start_urls = ['http://qyxy.baic.gov.cn/beijing']
	custom_settings = {
		'ROBOTSTXT_OBEY': False,
		'COOKIES_ENABLED': True,
		'COOKIES_DEBUG': True,
		'ITEM_PIPELINES': {
			'scraper.pipelines.mongo.MongoDBPipeline': 100,
		},
		# 'DOWNLOADER_MIDDLEWARES': {
		# 	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
		# 	'scraper.downloadermiddlewares.useragent.RandomUserAgentMiddleware': None,
		# },
		'DOWNLOAD_DELAY': 10, # safe delay
	}

	def __init__(self, *args, **kwargs):
		super(BeijingSpider, self).__init__(*args, **kwargs)

	def parse_info(self, response):
		table = BeautifulSoup(response.body, 'lxml').select('#jbxx')[0].find('table')
		sel = Selector(text=str(table))
		item = LimitedCorpCredit('test')
		item['reg_no'] = sel.xpath('//tr[2]/td[1]/text()').extract_first()
		item['comp_name'] = sel.xpath('//tr[2]/td[2]/text()').extract_first()
		item['comp_type'] = sel.xpath('//tr[3]/td[1]/text()').extract_first()
		item['legal_rep'] = sel.xpath('//tr[3]/td[2]/text()').extract_first()
		item['reg_capital'] = sel.xpath('//tr[4]/td[1]/text()').extract_first().strip()
		item['fund_date'] = sel.xpath('//tr[4]/td[2]/text()').extract_first()
		item['address'] = sel.xpath('//tr[5]/td/text()').extract_first()
		item['op_period_from'] = sel.xpath('//tr[6]/td[1]/text()').extract_first()
		item['op_period_to'] = sel.xpath('//tr[6]/td[2]/text()').extract_first()
		item['busi_scope'] = sel.xpath('//tr[7]/td/text()').extract_first()
		item['reg_office'] = sel.xpath('//tr[8]/td[1]/text()').extract_first()
		item['appr_date'] = sel.xpath('//tr[8]/td[2]/text()').extract_first()
		item['reg_status'] = sel.xpath('//tr[9]/td[1]/text()').extract_first()
		print item

	def _build_url(self, base, **params):
		# params['timeStamp'] = current_milli_time()
		return base + '?' + urllib.urlencode(params)