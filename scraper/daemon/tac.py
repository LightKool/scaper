# -*- coding: utf-8 -*-

from scrapy.utils.misc import load_object

from scraper.daemon import get_scraper_settings


def get_application():
    settings = get_scraper_settings()
    apppath = settings.get('DAEMON_APPLICATION', 'scraper.daemon.app.application')
    appfunc = load_object(apppath)
    return appfunc(settings)


application = get_application()
