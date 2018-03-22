# -*- coding: utf-8 -*-

BOT_NAME = 'taobao'

SPIDER_MODULES = ['taobao.spiders']
NEWSPIDER_MODULE = 'taobao.spiders'
DEFAULT_ITEM_CLASS = 'taobao.items.TaobaoItem'

DOWNLOADER_MIDDLEWARES = {
    # Engine side
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    # Downloader side
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
SPLASH_URL = 'http://127.0.0.1:8050/'
# SPLASH_URL = 'http://192.168.59.103:8050/'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
DOWNLOAD_DELAY = 10
