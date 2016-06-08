# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch

from scraper.items.elastic import ElasticDocumentItem


class ElasticDocumentPipeline(object):
    def __init__(self, host, port):
        self.es = Elasticsearch([{'host': host, 'port': port}])

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        host = settings.get('ELASTICSEARCH_HOST')
        port = settings.get('ELASTICSEARCH_PORT')
        return cls(host, port)

    def process_item(self, item, spider):
        if isinstance(item, ElasticDocumentItem):
            self.es.index(index=item.index, doc_type=item.doc_type, id=item.id, body=dict(item))
        return item
