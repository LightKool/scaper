# -*- coding: utf-8 -*-

import uuid

from zope.interface import implements
from twisted.internet.defer import DeferredQueue, inlineCallbacks, maybeDeferred, returnValue

from scraper.daemon import SCRAPY_PROJECT
from .interfaces import IPoller
from .spiderqueue import RedisSpiderQueue

class QueuePoller(object):

	implements(IPoller)

	def __init__(self, settings):
		self.q = RedisSpiderQueue(settings)
		self.dq = DeferredQueue(size=1)

	@inlineCallbacks
	def poll(self):
		if self.dq.pending:
			return
		c = yield maybeDeferred(self.q.count)
		if c:
			msg = yield maybeDeferred(self.q.pop)
			returnValue(self.dq.put(self._message(msg)))

	def next(self):
		return self.dq.get()

	def _message(self, queue_msg):
		d = queue_msg.copy()
		d['_project'] = SCRAPY_PROJECT
		d['_spider'] = d.pop('name')
		d['_job'] = d.pop('jobid', uuid.uuid1().hex)
		return d
