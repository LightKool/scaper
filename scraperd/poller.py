from zope.interface import implements
from twisted.internet.defer import DeferredQueue, inlineCallbacks, maybeDeferred, returnValue

from .interfaces import IPoller

class QueuePoller(object):

	implements(IPoller)

	def __init__(self, q):
		self.q = q
		self.dq = DeferredQueue(size=1)

	@inlineCallbacks
	def poll(self):
		if self.dq.pending:
			return
		c = yield maybeDeferred(self.q.count)
		if c:
			msg = yield maybeDeferred(self.q.pop)
			returnValue(self.dq.put(self._message(msg, p)))

	def next(self):
		return self.dq.get()

	def _message(self, queue_msg):
		d = queue_msg.copy()
		d['_spider'] = d.pop('name')
		return d
