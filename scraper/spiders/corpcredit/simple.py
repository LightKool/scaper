# -*- coding: utf-8 -*-

from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest

from scraper.spiders import RedisSpider
from scraper.items.corpcredit import *
from scraper.utils import safe_strip

class SimpleShanghaiSpider(RedisSpider):
	name = 'shanghai'
	allowed_domains = ['www.sgs.gov.cn']
	custom_settings = {
		'ROBOTSTXT_OBEY': False,
		'ITEM_PIPELINES': {
			'scraper.pipelines.mongo.MongoDBPipeline': 100,
		},
	}

	def init(self):
		super(SimpleShanghaiSpider, self).init()
		self.col_name = self.settings.get('CORP_CREDIT_COL_NAME', 'corp_credit')

	def parse(self, response):
		table = response.xpath('//div[@rel="layout-01_01"][1]/table')[0]
		item = LimitedCorpCredit(self.col_name)
		item['reg_no'] = safe_strip(table.xpath('tr[2]/td[1]/text()').extract_first())
		item['corp_name'] = safe_strip(table.xpath('tr[2]/td[2]/text()').extract_first())
		item['corp_type'] = safe_strip(table.xpath('tr[3]/td[1]/text()').extract_first())
		item['legal_rep'] = safe_strip(table.xpath('tr[3]/td[2]/text()').extract_first())
		item['reg_capital'] = safe_strip(table.xpath('tr[4]/td[1]/text()').extract_first())
		item['fund_date'] = safe_strip(table.xpath('tr[4]/td[2]/text()').extract_first())
		item['address'] = safe_strip(table.xpath('tr[5]/td/text()').extract_first())
		item['op_period_from'] = safe_strip(table.xpath('tr[6]/td[1]/text()').extract_first())
		item['op_period_to'] = safe_strip(table.xpath('tr[6]/td[2]/text()').extract_first())
		item['busi_scope'] = safe_strip(table.xpath('tr[7]/td/text()').extract_first())
		item['reg_office'] = safe_strip(table.xpath('tr[8]/td[1]/text()').extract_first())
		item['appr_date'] = safe_strip(table.xpath('tr[8]/td[2]/text()').extract_first())
		item['reg_status'] = safe_strip(table.xpath('tr[9]/td[1]/text()').extract_first())
		# sub items
		item['shareholders'] = self._parse_shareholders(response)
		item['main_staff'] = self._parse_staff(response)
		item['subsidiaries'] = self._parse_subsidiaries(response)
		yield item

	def _parse_shareholders(self, response):
		trs = response.xpath('//table[@id="investorTable"]/tr[@class="page-item"]')
		items = []
		for tr in trs:
			item = Shareholder()
			item['holder_type'] = safe_strip(tr.xpath('td[1]/text()').extract_first())
			item['name'] = safe_strip(tr.xpath('td[2]/text()').extract_first())
			item['license_type'] = safe_strip(tr.xpath('td[3]/text()').extract_first())
			items.append(item)
		return items

	def _parse_staff(self, response):
		trs = response.xpath('//table[@id="memberTable"]/tr[@class="page-item"]')
		items = []
		for tr in trs:
			item = Staff()
			item['name'] = safe_strip(tr.xpath('td[2]/text()').extract_first())
			item['title'] = safe_strip(tr.xpath('td[3]/text()').extract_first())
			items.append(item)
			name = safe_strip(tr.xpath('td[5]/text()').extract_first())
			if name != '':
				item = Staff()
				item['name'] = name
				item['title'] = safe_strip(tr.xpath('td[6]/text()').extract_first())
				items.append(item)
		return items

	def _parse_subsidiaries(self, response):
		trs = response.xpath('//table[@id="branchTable"]/tr[@class="page-item"]')
		items = []
		for tr in trs:
			item = Subsidiary()
			item['reg_no'] = safe_strip(tr.xpath('td[2]/text()').extract_first())
			item['name'] = safe_strip(tr.xpath('td[3]/text()').extract_first())
			item['reg_office'] = safe_strip(tr.xpath('td[4]/text()').extract_first())
			items.append(item)
		return items


class SimpleGuangdongSpider(RedisSpider):
	name = 'guangdong'
	allowed_domains = ['gsxt.gdgs.gov.cn']
	custom_settings = {
		'ROBOTSTXT_OBEY': False,
		'ITEM_PIPELINES': {
			'scraper.pipelines.mongo.MongoDBPipeline': 100,
		},
	}

	def init(self):
		super(SimpleGuangdongSpider, self).init()
		self.col_name = self.settings.get('CORP_CREDIT_COL_NAME', 'corp_credit')

	def parse(self, response):
		table = response.css('#jibenxinxi table')[0]
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