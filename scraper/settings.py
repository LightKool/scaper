# -*- coding: utf-8 -*-

# Scrapy settings for scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Scheduler setting
SCHEDULER = 'scraper.redis_scrapy.scheduler.RedisScheduler'

# Be polite
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'zh-cn,en;q=0.5',
}

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    'scraper.spidermiddlewares.pagination.FollowPaginationMiddleware': 501,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': None,
    'scraper.spidermiddlewares.depth.DepthMiddleware': 900,
    'scraper.spidermiddlewares.meta.RequestMetaMiddleware': 1000,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   'scraper.downloadermiddlewares.useragent.RandomUserAgentMiddleware': 400,
}

# Configure item pipelines
#ITEM_PIPELINES = {
#    'scraper.pipelines.MongoPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

LOG_LEVEL = 'INFO'
PAGINATION_MAX_PAGES = 2

# Redis settings
REDIS_HOST = '120.132.51.176'
REDIS_PORT = 6379

# ElasticSearch settings
ELASTICSEARCH_HOST = '120.132.51.176'
ELASTICSEARCH_PORT = 9200