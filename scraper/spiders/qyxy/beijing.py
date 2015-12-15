# -*- coding: utf-8 -*-

import re, urllib

from bs4 import BeautifulSoup

from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from scraper.spiders import RedisMixin
from scraper.items.qyxy import QYXYItem

class BeijingSpider(RedisMixin, Spider):
	name = 'qyxy_beijing'
	allowed_domains = ['qyxy.baic.gov.cn']
	start_urls = ['http://qyxy.baic.gov.cn/yzwfqymd/yzwfqymdAction!ccxxquery.dhtml']
	custom_settings = {
		'ROBOTSTXT_OBEY': False,
		'COOKIES_ENABLED': True,
		'ITEM_PIPELINES': {
			'scraper.pipelines.mongo.MongoDBPipeline': 100,
		},
	}

	def __init__(self, *args, **kwargs):
		super(BeijingSpider, self).__init__(*args, **kwargs)

	# def parse(self, response):
	# 	for page in xrange(1):
	# 		yield FormRequest(url=response.request.url,
	# 			formdata={'pageNos': str(page+1), 'pageSize': '10'},
	# 			callback=self.parse_list,
	# 			dont_filter=True)

	def parse(self, response):
		for entry in response.css('table.ccjcList a::attr(onclick)').extract():
			m = re.search("openEntInfo\((.+?)\)", entry)
			if m:
				info = m.group(1).split(',')
				name = info[0][1:-1]
				ent_id = info[1][1:-1]
				ent_no = info[2][1:-1]
				credit_ticket = info[3].strip()[1:-1]
				params = urllib.urlencode({'entId': ent_id, 'entNo': ent_no, 'credit_ticket': credit_ticket})
				url = response.urljoin('/gjjbj/gjjQueryCreditAction!openEntInfo.dhtml') + '?' + params
				yield Request(url=url, callback=self.parse_detail)

	def parse_detail(self, response):
		table = BeautifulSoup(response.body, 'lxml').select('#jbxx')[0].find('table')
		sel = Selector(text=str(table))
		item = QYXYItem('test')
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

		yield item