# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from multiprocessing import cpu_count

from twisted.internet import reactor, defer, protocol, error
from twisted.application.service import Service
from twisted.python import log

from scrapy.utils.python import stringify_dict
from scraper.daemon import get_crawl_args
from .interfaces import IPoller, IEnvironment

class Launcher(Service):

	def __init__(self, settings, app):
		self.processes = {}
		self.finished = []
		self.finished_to_keep = settings.getint('DAEMON_FINISHED_TO_KEEP', 100)
		self.max_proc = self._get_max_proc(settings)
		self.runner = settings.get('DAEMON_RUNNER', 'scraper.daemon.runner')
		self.app = app

	def startService(self):
		for slot in range(self.max_proc):
			self._wait_for_project(slot)
		log.msg(format='Scraperd started: max_proc=%(max_proc)r, runner=%(runner)r',
				max_proc=self.max_proc, runner=self.runner)

	def _wait_for_project(self, slot):
		poller = self.app.getComponent(IPoller)
		poller.next().addCallback(self._spawn_process, slot)

	def _spawn_process(self, message, slot):
		msg = stringify_dict(message, keys_only=False)
		args = [sys.executable, '-m', self.runner, 'crawl']
		args += get_crawl_args(msg)
		e = self.app.getComponent(IEnvironment)
		env = e.get_environment(msg, slot)
		env = stringify_dict(env, keys_only=False)
		pp = ScrapyProcessProtocol(slot, msg['_project'], msg['_spider'], msg['_job'], env)
		pp.deferred.addBoth(self._process_finished, slot)
		reactor.spawnProcess(pp, sys.executable, args=args, env=env)
		self.processes[slot] = pp

	def _process_finished(self, _, slot):
		process = self.processes.pop(slot)
		process.end_time = datetime.now()
		self.finished.append(process)
		del self.finished[:-self.finished_to_keep] # keep last 100 finished jobs
		self._wait_for_project(slot)

	def _get_max_proc(self, settings):
		max_proc = settings.getint('DAEMON_MAX_PROC', 0)
		if not max_proc:
			try:
				cpus = cpu_count()
			except NotImplementedError:
				cpus = 1
			max_proc = cpus * settings.getint('DAEMON_MAX_PROC_PER_CPU', 4)
		return max_proc

class ScrapyProcessProtocol(protocol.ProcessProtocol):

	def __init__(self, slot, project, spider, job, env):
		self.slot = slot
		self.pid = None
		self.project = project
		self.spider = spider
		self.job = job
		self.start_time = datetime.now()
		self.end_time = None
		self.env = env
		self.logfile = env.get('SCRAPY_LOG_FILE')
		self.deferred = defer.Deferred()

	def outReceived(self, data):
		log.msg(data.rstrip(), system="Launcher,%d/stdout" % self.pid)

	def errReceived(self, data):
		log.msg(data.rstrip(), system="Launcher,%d/stderr" % self.pid)

	def connectionMade(self):
		self.pid = self.transport.pid
		self.log("Process started: ")

	def processEnded(self, status):
		if isinstance(status.value, error.ProcessDone):
			self.log("Process finished: ")
		else:
			self.log("Process died: exitstatus=%r " % status.value.exitCode)
		self.deferred.callback(self)

	def log(self, action):
		fmt = '%(action)s project=%(project)r spider=%(spider)r job=%(job)r pid=%(pid)r log=%(log)r'
		log.msg(format=fmt, action=action, project=self.project, spider=self.spider,
				job=self.job, pid=self.pid, log=self.logfile)
