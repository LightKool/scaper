# -*- coding: utf-8 -*-

import re

from scrapy.spiders import Spider
from scrapy.http import Request

from scraper.spiders import RedisMixin
from scraper.items.cninfo import *
from scraper.utils import safe_strip

class CninfoSpider(RedisMixin, Spider):
    name = 'cninfo'
    allowed_domains = ['www.cninfo.com.cn']
    start_urls = [
        'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',  # 深市主板
        'http://www.cninfo.com.cn/information/sh/mb/shmblclist.html',  # 上市主板
        'http://www.cninfo.com.cn/information/sz/sme/szsmelclist.html',  # 中小企业板
        'http://www.cninfo.com.cn/information/sz/cn/szcnlclist.html',  # 创业板
    ]
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {
            'scraper.pipelines.mongo.MongoDBPipeline': 100,
        },
    }

    brief_url = 'http://www.cninfo.com.cn/information/brief/%s%s.html'
    staff_url = 'http://www.cninfo.com.cn/information/management/%s%s.html'
    shareholders_url = 'http://www.cninfo.com.cn/information/shareholders/%s.html'

    def parse(self, response):
        for value in response.xpath('//table//a/@onclick').extract():
            m = re.match(r"setLmCode\('.+\?(\D+)(\d+)'\);", value)
            if m:
                stock_prefix = m.group(1)
                stock_id = m.group(2)
                meta = {'stock_id': stock_id}
                # brief request
                brief_url = self.brief_url % (stock_prefix, stock_id)
                yield Request(url=brief_url, callback=self.parse_brief, meta=meta)
                # staff request
                staff_url = self.staff_url % (stock_prefix, stock_id)
                yield Request(url=staff_url, callback=self.parse_staff, meta=meta)
                # shareholders request
                shareholders_url = self.shareholders_url % (stock_id,)
                yield Request(url=shareholders_url, callback=self.parse_shareholders, meta=meta)

    def parse_brief(self, response):
        item = CorpInfo('corp_info')
        item['stock_id'] = response.meta['stock_id']
        table = response.css('div.zx_left table')[0]
        item['name'] = safe_strip(table.xpath('tr[1]/td[2]/text()').extract_first())
        item['eng_name'] = safe_strip(table.xpath('tr[2]/td[2]/text()').extract_first())
        item['address'] = safe_strip(table.xpath('tr[3]/td[2]/text()').extract_first())
        item['brief_name'] = safe_strip(table.xpath('tr[4]/td[2]/text()').extract_first())
        item['legal_rep'] = safe_strip(table.xpath('tr[5]/td[2]/text()').extract_first())
        item['reg_capital'] = safe_strip(table.xpath('tr[7]/td[2]/text()').extract_first())
        item['busi_type'] = safe_strip(table.xpath('tr[8]/td[2]/text()').extract_first())
        item['postcode'] = safe_strip(table.xpath('tr[9]/td[2]/text()').extract_first())
        item['tel'] = safe_strip(table.xpath('tr[10]/td[2]/text()').extract_first())
        item['fax'] = safe_strip(table.xpath('tr[11]/td[2]/text()').extract_first())
        item['homepage'] = safe_strip(table.xpath('tr[12]/td[2]/text()').extract_first())
        yield item

    def parse_staff(self, response):
        item = CorpInfo('corp_info')
        item['stock_id'] = response.meta['stock_id']
        staff = []
        for tr in response.xpath('//div[@class="zx_left"]//table/tr[position() > 1]'):
            s = Staff()
            s['name'] = safe_strip(tr.xpath('td[1]/text()').extract_first())
            s['title'] = safe_strip(tr.xpath('td[2]/text()').extract_first())
            s['gender'] = safe_strip(tr.xpath('td[4]/text()').extract_first())
            staff.append(s)
        item['staff'] = staff
        yield item

    def parse_shareholders(self, response):
        item = CorpInfo('corp_info')
        item['stock_id'] = response.meta['stock_id']
        shareholders = []
        table = response.css('div.zx_left table')[0]
        rowspan = int(table.xpath('tr[2]/td/@rowspan').extract_first())
        chars = '1234567890.'
        for i in xrange(2, 2 + rowspan):
            s = Shareholder()
            if i == 2:
                s['name'] = safe_strip(table.xpath('tr[%d]/td[2]/text()' % i).extract_first(), chars)
                s['ratio'] = float(safe_strip(table.xpath('tr[%d]/td[4]/text()' % i).extract_first()))
            else:
                s['name'] = safe_strip(table.xpath('tr[%d]/td[1]/text()' % i).extract_first(), chars)
                s['ratio'] = float(safe_strip(table.xpath('tr[%d]/td[3]/text()' % i).extract_first()))
            shareholders.append(s)
        item['shareholders'] = shareholders
        yield item
