from twisted.application.service import Application
from twisted.application.internet import TimerService, TCPServer
from twisted.web import server
from twisted.python import log

from scrapy.utils.misc import load_object

from .interfaces import ISpiderQueue, IPoller, IEnvironment
from .spiderqueue import RedisSpiderQueue
from .poller import QueuePoller
from .environ import Environment
from .config import Config

def application(config):
	app = Application("Scraperd")
	poll_interval = config.getfloat('poll_interval', 5)

	spiderqueue = RedisSpiderQueue(config)
	poller = QueuePoller(spiderqueue)
	environment = Environment(config)

	app.setComponent(ISpiderQueue, spiderqueue)
	app.setComponent(IPoller, poller)
	app.setComponent(IEnvironment, environment)

	laupath = config.get('launcher', 'scraperd.launcher.Launcher')
	laucls = load_object(laupath)
	launcher = laucls(config, app)

	timer = TimerService(poll_interval, poller.poll)

	launcher.setServiceParent(app)
	timer.setServiceParent(app)

	return app
