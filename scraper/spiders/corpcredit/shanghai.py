# -*- coding: utf-8 -*-

from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest

from scraper.spiders import RedisMixin
from scraper.items.corpcredit import CorpCredit, Shareholder, Subsidiary, Staff
from scraper.utils import safe_strip

class ShanghaiSpider(RedisMixin, Spider):
	name = 'corp_credit_shanghai'
	allowed_domains = ['www.sgs.gov.cn']
	start_urls = ['https://www.sgs.gov.cn/notice/search/ent_spot_check_list']
	custom_settings = {
		'ROBOTSTXT_OBEY': False,
		'ITEM_PIPELINES': {
			'scraper.pipelines.mongo.MongoDBPipeline': 100,
		},
		'DOWNLOAD_DELAY': 3, # safe delay
		# 'HTTPCACHE_ENABLED': True, # test purpose
	}

	def init(self):
		self.col_name = self.settings.get('CORP_CREDIT_COL_NAME', 'corp_credit')
		self.maxpage = self.settings.getint('CORP_CREDIT_MAX_PAGE', 50)
		# The maximum page number the URL
		# [https://www.sgs.gov.cn/notice/search/ent_spot_check_list]
		# supports is 50.
		self.maxpage = 50 if self.maxpage <= 0 else min(self.maxpage, 50)
		self.link_extractor = LinkExtractor(restrict_css=['table.list-table'])

	def parse(self, response):
		self.session_token = response.xpath('//input[@name="session.token"]/@value').extract_first()
		return self.parse_list(response)

	def parse_list(self, response):
		for link in self.link_extractor.extract_links(response):
			yield Request(url=link.url, callback=self.parse_info)

		page = response.meta.get('page', 1)
		if page < self.maxpage:
			page += 1
			formdata = {
				'condition.insType': '1',
				'condition.pageNo': str(page),
				'session.token': self.session_token,
			}
			yield FormRequest(url=self.start_urls[0], formdata=formdata,
				callback=self.parse_list, meta={'page': page})

	def parse_info(self, response):
		table = response.xpath('//div[@rel="layout-01_01"][1]/table')[0]
		item = CorpCredit(self.col_name)
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