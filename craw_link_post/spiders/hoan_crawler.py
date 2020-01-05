# !/usr/bin/env python
# _*_ coding: utf-8 _*_


import scrapy
import configparser
from scrapy.conf import settings
from craw_link_post.common.database import Database

class HoanCrawler(scrapy.Spider):
	name ="hoan"
	
	def __init__(self):
		pass
	
	def get_config(self, link=''):
		parse_link = configparser.ConfigParser()
		parse_link.read(settings.get('CONFIG_XPATH'), encoding="utf8")
		domain = link.split("://")[-1].split('/')[0].split('?')[0]
		out = dict()
		out['path'] = parse_link.get(domain, 'path')
		out['domain'] = link.split("://")[0] + "://" + domain
		return out
	
	def start_requests(self):
		urls = [
			"https://news.zing.vn/ti%E1%BB%81n-%E1%BA%A3o-tin-tuc.html",
			"https://dantri.com.vn/tien-ao.tag",
			"https://coin68.com/",
			"https://www.tapchibitcoin.vn/",
			"https://cafebitcoin.info/",
			"https://trungvanhoang.com/",
			"https://bitcoinnews24h.net/",
			"https://vietnamfinance.vn/tong-hop-tin-tuc-tien-dien-tu-hom-nay-267-20180504224210526.htm",
			"https://tuvantienao.com/",
			"https://baomoi.com/tag/Ti%E1%BB%81n-%E1%BA%A3o.epi",
			"http://tintuctienao.com/",
			"https://www.xaluan.com/modules.php?name=News&new_topic=106",
			"http://bitmainvietnam.com/",
			"https://sieuthibitcoin.com/",
			"https://www.cachmuabitcoin.com/bai-viet/tin-tuc-bitcoin/",
			"https://giaoducthoidai.vn/tags/IHRp4buBbiDhuqNv/tien-ao.html",
			"https://vnexpress.net/tag/tien-dien-tu-421384",
			"https://blog.kiemtienso.io/",
			"https://tienkythuatso.com/",
			"https://ecoinfogreen.com/",
			"https://vndc.io/posts",
			"https://vnbit.net/",
			"https://vn.nami.today/cryptocurrency/tong-quan-thi-truong-tien-dien-tu-ngay-1292018-tin-tuc-tieu-cuc-phu-bong-thi-truong-4724.html",
			"https://vnreview.vn/digital-society",
			"https://vbc.group/category/tin-tuc/",
			"https://bitcoin-news.vn/tin-coins/",
			"https://trumdaotien.com/",
			"https://cryptoinsidervn.wordpress.com/",
			"https://nld.com.vn/tien-ao.html",
			"https://trithucvn.net/blog/tien-ao.html",
			"https://daututaichinh24h.com/",
			"https://tygiacoin.com/tin-tuc.html"
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
	
	def parse(self, response):
		xpath = self.get_config(response.url)
		links = response.selector.xpath(xpath["path"]).extract()
		for link in links:
			if link and (xpath["domain"] not in link):
				if '/' in link:
					link = xpath["domain"] + link
				else:
					link = xpath["domain"] + '/' + link
			item = {}
			item['url'] = link
			item['domain'] = xpath["domain"]
			Database()._insert_post(item)
			print(link, "url")