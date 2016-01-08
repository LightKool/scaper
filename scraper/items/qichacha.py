# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

from . import MongoItem

class CorpInfo(MongoItem):
	uid = Field()
	credit_code = Field()
	corp_name = Field()
	reg_no = Field()
	org_code = Field()
	status = Field()
	corp_type = Field()
	fund_date = Field()
	legal_rep = Field()
	reg_capital = Field()
	op_period = Field()
	reg_office = Field()
	appr_date = Field()
	corp_scale = Field()
	industry = Field()
	address = Field()
	busi_scope = Field()

	shareholders = Field()
	investments = Field()

	def do_process(self, db):
		db[self._col_name].update_one({'uid': self['uid']},
			{'$set': dict(self)}, upsert=True)

class Shareholder(Item):
	name = Field()
	corp_uid = Field()
	holder_type = Field()
	reg_amount = Field()
	paid_amount = Field()
	method = Field()

class Investment(Item):
	corp_uid = Field()
	corp_name = Field()