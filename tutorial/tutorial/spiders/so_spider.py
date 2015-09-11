import re

import scrapy

from tutorial.items import SOQuestionItem

class SOSpider(scrapy.Spider):
	name = 'StackOverflow'
	allowed_domains = ['stackoverflow.com']
	start_urls = ['http://stackoverflow.com/questions/tagged/python']

	def parse(self, response):
		for url in ['http://stackoverflow.com/questions/tagged/python?page=%d' % page for page in range(1,3)]:
			yield scrapy.Request(url, callback=self.parse_list)

	def parse_list(self, response):
		for href in response.xpath('.//div[@id="questions"]//h3/a/@href').extract():
			url = response.urljoin(href)
			yield scrapy.Request(url, callback=self.parse_question)

	def parse_question(self, response):
		item = SOQuestionItem()
		m = re.search('/questions/(\d+)/.+', response.url)
		if m:
			item['question_id'] = m.group(1)
		item['question_title'] = response.xpath('.//h1/a/text()').extract_first()
		item['issue_time'] = response.css('span.relativetime').xpath('@title').extract_first()
		yield item