# -*- coding: utf-8 -*-

import json

from scrapy.spiders import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from scraper.spiders import RedisMixin
from scraper.items.corpcredit import *
from scraper.utils import safe_strip

class GuangdongSpider(RedisMixin, Spider):
	name = 'corp_credit_guangdong'
	allowed_domains = ['gsxt.gdgs.gov.cn']
	start_urls = ['http://gsxt.gdgs.gov.cn/aiccips/main/initInspInfoList.html']
	custom_settings = {
		'ROBOTSTXT_OBEY': False,
		'ITEM_PIPELINES': {
			'scraper.pipelines.mongo.MongoDBPipeline': 100,
		},
		'DOWNLOAD_DELAY': 3, # safe delay
	}

	def init(self):
		self.fetch_url = 'http://gsxt.gdgs.gov.cn/aiccips/main/inspInfoList.html'
		self.col_name = self.settings.get('CORP_CREDIT_COL_NAME', 'corp_credit')
		maxpage = self.settings.getint('CORP_CREDIT_MAX_PAGE', 1000)
		self.maxpage = 1000 if maxpage <= 0 else min(maxpage, 1000)

	def parse(self, response):
		# yield initial request
		yield FormRequest(url=self.fetch_url, formdata={'pageNo': '0'}, callback=self.parse_list)

	def parse_list(self, response):
		data = json.loads(response.body)
		for row in data['rows']:
			url = response.urljoin(Selector(text=row['entNameUrl']).xpath('//a/@href').extract_first())
			yield Request(url=url, callback=self.parse_info)

		page = response.meta.get('page', 0) # zero-based
		if page < self.maxpage - 1:
			page += 1
			yield FormRequest(url=self.fetch_url, formdata={'pageNo': str(page)},
				callback=self.parse_list, meta={'page': page})

	def parse_info(self, response):
		table = response.css('#baseinfo')[0]
		if len(table.xpath('tr')) == 9:
			item = IndividualCorpCredit(self.col_name)
			item['reg_no'] = safe_strip(table.xpath('tr[3]/td[1]/text()').extract_first())
			item['corp_name'] = safe_strip(table.xpath('tr[3]/td[2]/text()').extract_first())
			item['corp_type'] = safe_strip(table.xpath('tr[4]/td[1]/text()').extract_first())
			item['investor'] = safe_strip(table.xpath('tr[4]/td[2]/text()').extract_first())
			item['address'] = safe_strip(table.xpath('tr[5]/td/text()').extract_first())
			item['fund_date'] = safe_strip(table.xpath('tr[6]/td[2]/text()').extract_first())
			item['busi_scope'] = safe_strip(table.xpath('tr[7]/td/text()').extract_first())
			item['reg_office'] = safe_strip(table.xpath('tr[8]/td[1]/text()').extract_first())
			item['appr_date'] = safe_strip(table.xpath('tr[8]/td[2]/text()').extract_first())
			item['reg_status'] = safe_strip(table.xpath('tr[9]/td[1]/text()').extract_first())
		elif len(table.xpath('tr')) == 10:
			item = LimitedCorpCredit(self.col_name)
			item['reg_no'] = safe_strip(table.xpath('tr[3]/td[1]/text()').extract_first())
			item['corp_name'] = safe_strip(table.xpath('tr[3]/td[2]/text()').extract_first())
			item['corp_type'] = safe_strip(table.xpath('tr[4]/td[1]/text()').extract_first())
			item['legal_rep'] = safe_strip(table.xpath('tr[4]/td[2]/text()').extract_first())
			item['reg_capital'] = safe_strip(table.xpath('tr[5]/td[1]/text()').extract_first())
			item['fund_date'] = safe_strip(table.xpath('tr[5]/td[2]/text()').extract_first())
			item['address'] = safe_strip(table.xpath('tr[6]/td/text()').extract_first())
			item['op_period_from'] = safe_strip(table.xpath('tr[7]/td[1]/text()').extract_first())
			item['op_period_to'] = safe_strip(table.xpath('tr[7]/td[2]/text()').extract_first())
			item['busi_scope'] = safe_strip(table.xpath('tr[8]/td/text()').extract_first())
			item['reg_office'] = safe_strip(table.xpath('tr[9]/td[1]/text()').extract_first())
			item['appr_date'] = safe_strip(table.xpath('tr[9]/td[2]/text()').extract_first())
			item['reg_status'] = safe_strip(table.xpath('tr[10]/td[1]/text()').extract_first())
		yield item