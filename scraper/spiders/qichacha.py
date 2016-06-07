# -*- coding: utf-8 -*-

from string import whitespace
import re

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

from scraper.spiders import RedisMixin
from scraper.items.qichacha import *
from scraper.utils import safe_strip, safe_extract
from scraper.spidermiddlewares.depth import HoldDepthRequest

class QichachaSpider(RedisMixin, Spider):
    name = 'qichacha'
    allowed_domains = ['qichacha.com']
    start_urls = ['http://qichacha.com/firm_CN_2fde0a8c9a5f08b6b03988d58dbf7473']
    custom_settings = {
        'COOKIES_ENABLED': True,
        'ITEM_PIPELINES': {
            'scraper.pipelines.mongo.MongoDBPipeline': 100,
        },
        'DOWNLOAD_DELAY': 3,  # safe delay
        'DEPTH_LIMIT': 3,
    }
    pspt = '%7B%22id%22%3A%22537259%22%2C%22pswd%22%3A%22107cdca7b23241f732d24bbcb8e068aa%22%2C%22_code%22%3A%2229954fedf40e4373e1c984fb8f88c9fa%22%7D'

    # link extractors
    investment_link_extractor = LinkExtractor(restrict_css='#company-nav>p', allow='.*touzi.*')

    def init(self):
        super(QichachaSpider, self).init()
        self.label_to_field = {
            u'统一社会信用代码': 'credit_code',
            u'注册号': 'reg_no',
            u'组织机构代码': 'org_code',
            u'经营状态': 'status',
            u'公司类型': 'corp_type',
            u'成立日期': 'fund_date',
            u'法定代表': 'legal_rep',
            u'注册资本': 'reg_capital',
            u'营业期限': 'op_period',
            u'登记机关': 'reg_office',
            u'发照日期': 'appr_date',
            u'公司规模': 'corp_scale',
            u'行业': 'industry',
            u'住所': 'address',
            u'经营范围': 'busi_scope',
        }
        self.label_strip_chars = whitespace+u':：'
        self.uid_pattern = re.compile('firm_(.+)_(.+)')

    def make_requests_from_url(self, url):
        return Request(url=url, dont_filter=True, callback=self.parse_info, cookies={'pspt': self.pspt})

    def parse_info(self, response):
        uid = self._extract_uid(response.url)
        for link in self.investment_link_extractor.extract_links(response):
            yield HoldDepthRequest(url=link.url, callback=self.parse_investment, meta={'uid': uid})

        item = CorpInfo('corp_info')
        item['uid'] = uid
        item['corp_name'] = safe_extract(response.xpath('//*[@id="companyheader"]/h3/span/text()'))
        corp_info = response.css('.company-info')[0]
        for li in corp_info.xpath('li'):
            label = safe_strip(li.xpath('label/text()').extract_first(), chars=self.label_strip_chars)
            field = self.label_to_field[label]
            if field is 'legal_rep':
                item[field] = safe_extract(li.xpath('a/text()'), sep='')
            else:
                item[field] = safe_extract(li.xpath('text()'), sep='')

        # parse shareholders and related pages
        shareholders = []
        for a in response.css('tr.white>td>div>a[href*=firm]'):
            # yield request
            url = response.urljoin(a.xpath('@href').extract_first())
            yield Request(url=url, callback=self.parse_info)

            shareholder = Shareholder()
            shareholder['name'] = safe_extract(a.xpath('span/text()'))
            shareholder['corp_uid'] = self._extract_uid(url)
            tr = a.xpath('../../..')
            shareholder['holder_type'] = safe_extract(tr.xpath('td[2]/text()'))
            shareholder['reg_amount'] = safe_extract(tr.xpath('td[3]/p/text()'), sep='/')
            shareholder['paid_amount'] = safe_extract(tr.xpath('td[4]/p/text()'), sep='/')
            shareholder['method'] = safe_extract(tr.xpath('td[5]/text()'))
            shareholders.append(shareholder)
        for a in response.css('tr.white>td>div>a[href*=search]'):
            shareholder = Shareholder()
            shareholder['name'] = safe_extract(a.xpath('text()'))
            tr = a.xpath('../../../..')
            shareholder['holder_type'] = safe_extract(tr.xpath('td[2]/text()'))
            shareholder['reg_amount'] = safe_extract(tr.xpath('td[3]/p/text()'), sep='/')
            shareholder['paid_amount'] = safe_extract(tr.xpath('td[4]/p/text()'), sep='/')
            shareholder['method'] = safe_extract(tr.xpath('td[5]/text()'))
            shareholders.append(shareholder)
        item['shareholders'] = shareholders

        # parse subsidiaries
        subsidiaries = []
        for a in response.css('tr.white>td>a'):
            # yield request
            url = response.urljoin(a.xpath('@href').extract_first())
            yield Request(url=url, callback=self.parse_info)

            subsidiary = Subsidiary()
            subsidiary['corp_uid'] = self._extract_uid(url)
            subsidiary['corp_name'] = safe_strip(a.xpath('text()').extract_first())
            subsidiaries.append(subsidiary)
        item['subsidiaries'] = subsidiaries

        yield item

    def parse_investment(self, response):
        item = CorpInfo('corp_info')
        item['uid'] = response.meta['uid']
        investments = []
        for a in response.css('.site-list-title>a[href*=firm]'):
            url = response.urljoin(a.xpath('@href').extract_first())
            yield Request(url=url, callback=self.parse_info)

            investment = Investment()
            investment['corp_uid'] = self._extract_uid(url)
            investment['corp_name'] = safe_strip(a.xpath('text()').extract_first())
            investments.append(investment)

        item['investments'] = investments
        yield item

    def _extract_uid(self, url):
        m = self.uid_pattern.search(url)
        if m:
            return m.group(2)
