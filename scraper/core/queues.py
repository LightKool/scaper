# -*- coding: utf-8 -*-
import json


class Base(object):
	'''
	Base class for redis backed queue/stack
	'''
	def __init__(self, server, key):
		self.server = server
		self.key = key

	def _encode_item(self, item):
		return json.dumps(item)

	def _decode_item(self, item):
		return json.loads(item)

	def __len__(self):
		raise NotImplementedError

	def push(self):
		raise NotImplementedError

	def pop(self, timeout=0):
		raise NotImplementedError

	def clear(self):
		self.server.delete(self.key)


class RedisPriorityQueue(Base):
	'''
	Priority queue backed by Redis sorted set
	'''
	def __len__(self):
		return self.server.zcard(self.key)

	def push(self, item, priority):
		data = self._encode_item(item)
		pairs = {data: -priority}
		self.server.zadd(self.key, **pairs)

	def pop(self, timeout=0):
		pipe = self.server.pipeline()
		pipe.multi()
		pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
		results, count = pipe.execute()
		if results:
			return self._decode_item(results[0])


__all__ = ['RedisPriorityQueue']
