import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from . import RedisMixin
from scraper.spidermiddlewares.pagination import PaginationRule
from scraper.items.wdzj import WDZJNewsItem

from readability.readability import Document
import html2text

class WDZJNewsSpider(RedisMixin, CrawlSpider):
	name = 'wdzj_news'
	allowed_domains = ['wangdaizhijia.com']
	start_urls = ['http://www.wangdaizhijia.com/news']
	custom_settings = {
		'ITEM_PIPELINES': {
			'scraper.pipelines.elastic.ElasticDocumentPipeline': 100,
		},
	}

	rules = (
		Rule(LinkExtractor(allow=('/news/[^/]+/\d+\.html',), restrict_css=('div.specialBox',)),
			callback='parse_news_content'),
		PaginationRule(Rule(LinkExtractor(allow=('/news/[^/]+/p\d+\.html'),
			# tricky point: the :nth-last-of-type is 0-based instead of the
			# standard 1-based, could be the bug of python cssselect library
			# so use with cautions
			restrict_css=('div.pageList>a:nth-last-of-type(1)',)))),
	)

	full_article_link_extractor = LinkExtractor(allow=('/news/[^/]+/\d+-all.html'),
		restrict_css=('div.pageList>a:last-child',))

	def parse_start_url(self, response):
		frontpage_link_extractor = LinkExtractor(restrict_css=('div.news_box>div.nbs_1 li.nbs_li',))
		for link in frontpage_link_extractor.extract_links(response):
			print link.url
			yield Request(url=link.url)

	def parse_news_content(self, response):
		for link in self.full_article_link_extractor.extract_links(response):
			request = response.request.replace(url=link.url)
			yield request
		
		item = self._create_item(response)
		if item is not None:
			doc = Document(response.body)
			item['title'] = doc.short_title()
			item['content'] = html2text.html2text(doc.summary())
			yield item

	def _create_item(self, response):
		m = re.search('/news/(?P<doc_type>[^/]+)/(?P<doc_id>\d+)', response.url)
		if m:
			return WDZJNewsItem(self.name, m.group('doc_type'), m.group('doc_id'))
		else:
			return None
