# -*- coding: utf-8 -*-

import re, urllib, time

from bs4 import BeautifulSoup

from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from scraper.spiders import RedisMixin
from scraper.items.qyxy import CompCreditItem
from scraper.utils import current_milli_time

class BeijingSpider(RedisMixin, Spider):
	name = 'qyxy_beijing'
	allowed_domains = ['qyxy.baic.gov.cn']
	start_urls = ['http://qyxy.baic.gov.cn/yzwfqymd/yzwfqymdAction!ccxxquery.dhtml?clear=true']
	custom_settings = {
		'ROBOTSTXT_OBEY': False,
		'COOKIES_ENABLED': True,
		'COOKIES_DEBUG': True,
		'ITEM_PIPELINES': {
			'scraper.pipelines.mongo.MongoDBPipeline': 100,
		},
		'DOWNLOAD_DELAY': 10, # safe delay
	}

	def __init__(self, *args, **kwargs):
		super(BeijingSpider, self).__init__(*args, **kwargs)

	def start_requests(self):
		url = self.start_urls[0]
		for page in xrange(1, 2):
			yield FormRequest(url=url, formdata={'pageNos': str(page), 'pageSize': '10'},
				callback=self.parse_list, dont_filter=True)

	def parse_list(self, response):
		for entry in response.css('table.ccjcList a::attr(onclick)').extract():
			m = re.search("openEntInfo\((.+?)\)", entry)
			if m:
				info = m.group(1).split(',')
				ent_id = info[1].strip()[1:-1]
				reg_no = info[2].strip()[1:-1]
				credit_ticket = info[3].strip()[1:-1]
				# crawl the basic information page
				url = self._build_url(response.urljoin('/gjjbj/gjjQueryCreditAction!openEntInfo.dhtml'),
					entId=ent_id, entNo=reg_no, credit_ticket=credit_ticket)
				yield Request(url=url, callback=self.parse_detail, meta={'reg_no': reg_no})

	def parse_detail(self, response):
		table = BeautifulSoup(response.body, 'lxml').select('#jbxx')[0].find('table')
		sel = Selector(text=str(table))
		item = CompCreditItem('test')
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

	def _build_url(self, base, **params):
		# params['timeStamp'] = current_milli_time()
		return base + '?' + urllib.urlencode(params)