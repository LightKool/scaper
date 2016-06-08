# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.http.request import Request

from . import RedisSpider


class SimpleSpider(RedisSpider):
    name = 'simple'

    def __init__(self, *args, **kwargs):
        super(SimpleSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        link_extractor = self._create_link_extractor(response.meta)
        for link in link_extractor.extract_links(response):
            yield Request(link.url)

    def _create_link_extractor(self, meta):
        return LinkExtractor(
            allow=meta['allow'],
            deny=meta['deny'],
            allow_domains=meta['allow_domains'],
            deny_domains=meta['deny_domains'],
            restrict_xpaths=meta['restrict_xpaths'],
            restrict_css=meta['restrict_css'])
