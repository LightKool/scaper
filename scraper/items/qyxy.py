# -*- coding: utf-8 -*-

from scrapy.item import Field

from . import MongoItem

class QYXYItem(MongoItem):
	reg_no = Field() #注册号
	comp_name = Field() #公司名称
	comp_type = Field() #类型
	legal_rep = Field() #法定代表人
	reg_capital = Field() #注册资本
	fund_date = Field() #成立日期
	address = Field() #住所
	op_period_from = Field() #营业期限自
	op_period_to = Field() #营业期限至
	busi_scope = Field() #经营范围
	reg_office = Field() #登记机关
	appr_date = Field() #核准日期
	reg_status = Field() #登记状态

	def do_process(self, db):
		db[self._col_name].insert_one(dict(self))