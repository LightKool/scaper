# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

from . import MongoItem

class CorpCredit(MongoItem):
	reg_no = Field() #注册号
	corp_name = Field() #公司名称
	corp_type = Field() #类型
	fund_date = Field() #成立日期
	address = Field() #住所
	busi_scope = Field() #经营范围
	reg_office = Field() #登记机关
	appr_date = Field() #核准日期
	reg_status = Field() #登记状态

	# sub items
	shareholders = Field() #股东
	main_staff = Field() #主要人员
	subsidiaries = Field() #分支机构

	def do_process(self, db):
		db[self._col_name].update_one({'reg_no': self['reg_no']},
			{'$set': dict(self)}, upsert=True)

class LimitedCorpCredit(CorpCredit):
	legal_rep = Field() #法定代表人
	reg_capital = Field() #注册资本
	op_period_from = Field() #营业期限自
	op_period_to = Field() #营业期限至

class LimitedSubCorpCredit(CorpCredit):
	person_in_charge = Field() #负责人
	op_period_from = Field() #营业期限自
	op_period_to = Field() #营业期限至

class IndividualCorpCredit(CorpCredit):
	investor = Field() #投资人

class PartnerCorpCredit(CorpCredit):
	exec_partner = Field() #执行事务合伙人
	partner_period_from = Field() #合伙期限自
	partner_period_to = Field() #合伙期限至

class Shareholder(Item):
	holder_type = Field() #股东类型
	name = Field() #名称
	license_type = Field() #证照/证件类型

class Staff(Item):
	name = Field() #姓名
	title = Field() #职务

class Subsidiary(Item):
	reg_no = Field() #注册号
	name = Field() #名称
	reg_office = Field() #登记机关