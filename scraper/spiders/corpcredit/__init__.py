# -*- coding: utf-8 -*-

from zope.interface import Interface, implements

class IKeywordsGenerator(Interface):
	'''
	Keyword generator interface to feed keywords to all "企业信用" spiders.
	'''

	def generate():
		'''
		Return keywords. Must be a generator function.
		'''

class SimpleKeywordsGenerator(object):

	implements(IKeywordsGenerator)

	def __init__(self, keywords=[]):
		self.keywords = keywords

	def generate(self):
		for keyword in self.keywords:
			yield keyword
