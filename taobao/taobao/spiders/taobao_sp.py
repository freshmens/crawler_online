# -*- coding: utf-8 -*-
import re
import time

from scrapy import Spider
from scrapy import Request
from scrapy_splash import SplashRequest
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from taobao.items import TaobaoItem

class TBSpider(Spider):
    name='tb'
    allowed_domains=['taobao.com', 'tmall.com']
#    start_urls = ['https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20160913&stats_click=search_radio_all%3A1&js=1&imgfile=&q=swatch%E6%89%8B%E8%A1%A8&suggest=0_3&_input_charset=utf-8&wq=swatch&suggest_query=swatch&source=suggest&sort=sale-desc']
#    start_urls = ['https://s.taobao.com/search?q=%E4%B8%89%E6%98%9F%E6%99%BA%E8%83%BD%E9%94%81&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20161114&sort=sale-desc']
#    start_urls = ['https://s.taobao.com/search?q=%E6%99%BA%E8%83%BD%E9%94%81&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20161118&ie=utf8&sort=sale-desc&filter=reserve_price%5B400%2C20000%5D']
#    start_urls = ['https://s.taobao.com/search?q=%E7%AB%A5%E8%BD%A6+%E6%8E%A8%E8%BD%A6&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170221&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=0']
    start_urls = ['https://s.taobao.com/search?q=%E5%88%AE%E6%AF%9B%E5%88%80&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170705&sort=sale-desc']
#    start_urls = ['https://item.taobao.com/item.htm?id=22120775692&ns=1&abbucket=0#detail']

    url_pattern=[r'.*rank=sale&type=hot.*']
    url_extractor=LxmlLinkExtractor(allow=url_pattern)
    item_dict={}

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,callback=self.parse,args={
            #yield SplashRequest(url,callback=self.parse_item,args={
                'wait':9,'html':1,
            }
            )

    def parse(self,response):
	    link_list =re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')" ,response.body)
	    print("======================:")
	    for ttt in link_list:
	    	print(ttt)

	    urls = []
	    urls1 = []
	    for url in link_list:
	            if re.search("detail.tmall.com/\w+", url):
			if url not in urls:
				urls.append(url)
	            if re.search("item.taobao.com/\w+", url):
			if url not in urls:
				urls.append(url)
	    for url in urls:
		url1 = url.replace("&amp;", "&")
		if (url1.find("https") < 0):
			url2 = url1.replace("//", "https://")
		urls1.append(url2)

            print(len(urls1))

	    for url in urls1:
		print(url)
		yield SplashRequest(url,callback=self.parse_item,args={'wait':9,'html':1})


    def parse_item(self,response):
	print(response.url)
	print("=================================:")
	print(response.status)
	if re.search("detail.tmall.com", response.url):
		# tmall
		# title
		list_title = response.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[1]/h1/text()').extract()
		if (len(list_title) > 0):
			title = list_title[0].strip()
		else:
			title = "--"

		# count
		list_count = response.xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]/text()').extract()
		if (len(list_count) > 0):
			count = list_count[0].strip()
		else:
			count = "=="

		# price
		list_price1 = response.xpath('//*[@id="J_PromoPrice"]/dd/div/span/text()').extract()
		#list_price2 = response.xpath('//*[@id="J_StrPriceModBox"]/dd/span/text()').extract()
		if (len(list_price1) > 0):
			price = list_price1[0].strip()
		else:
			price = 0
		sell_out = count
	else:
		# taobao
		# title
		list_title = response.xpath('//*[@id="J_Title"]/h3/text()').extract()
		if (len(list_title) > 0):
			title = list_title[0].strip()
		else:
			title = "--"

		# count
		list_count = response.xpath('//*[@id="J_SellCounter"]/text()').extract()
		if (len(list_count) > 0):
			count = list_count[0].strip()
		else:
			count = "=="

		# price
		list_price1 = response.xpath('//*[@id="J_PromoPriceNum"]/text()').extract()
		#list_price2 = response.xpath('//*[@id="J_StrPrice"]/em[2]/text()').extract()
		if (len(list_price1) > 0):
			price = list_price1[0].strip()
		else:
			price = 0

		# sell_out
		sell_out = response.xpath('//*[@id="J_Counter"]/div/div[2]/a/@title').extract()
		if (len(sell_out) > 0):
			sell_out = sell_out[0].strip()
		else:
			sell_out = count

	print(title)
	print(price)
	print(count)
	print(sell_out)
	item = TaobaoItem()
	item['title'] = title
	item['price'] = price
	item['count'] = count
	item['url'] = response.url
	item['sell_out'] = sell_out
	yield item
