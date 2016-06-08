# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

from . import MongoItem


class CorpInfo(MongoItem):
    stock_id = Field()
    name = Field()
    eng_name = Field()
    address = Field()
    brief_name = Field()
    legal_rep = Field()
    reg_capital = Field()
    busi_type = Field()
    postcode = Field()
    tel = Field()
    fax = Field()
    homepage = Field()

    staff = Field()
    shareholders = Field()

    def do_process(self, db):
        db[self._col_name].update_one(
            {'stock_id': self['stock_id']},
            {'$set': dict(self)},
            upsert=True
        )


class Staff(Item):
    name = Field()
    title = Field()
    gender = Field()


class Shareholder(Item):
    name = Field()
    ratio = Field()
