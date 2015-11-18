# -*- coding: utf-8 -*-

from twisted.application.service import Application
from twisted.application.internet import TimerService

from scrapy.utils.misc import load_object

from .interfaces import IPoller, IEnvironment
from .poller import QueuePoller
from .environ import Environment

def application(settings):
	app = Application("Scraperd")

	poller = QueuePoller(settings)
	environment = Environment(settings)

	app.setComponent(IPoller, poller)
	app.setComponent(IEnvironment, environment)

	laupath = settings.get('DAEMON_LAUNCHER', 'scraper.daemon.launcher.Launcher')
	laucls = load_object(laupath)
	launcher = laucls(settings, app)

	poll_interval = settings.getfloat('DAEMON_POLL_INTERVAL', 5)
	timer = TimerService(poll_interval, poller.poll)

	launcher.setServiceParent(app)
	timer.setServiceParent(app)

	return app
