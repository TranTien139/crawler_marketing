# !/usr/bin/env python
# _*_ coding: utf-8 _*_


import MySQLdb
from scrapy.conf import settings

__author__ = 'TranTien'

class Database:
	def __init__(self):
		print("connect database")
		self.conn = MySQLdb.connect(host=settings['MYSQL_HOST'],
		                            port=int(settings['MYSQL_PORT']),
		                            user=settings['MYSQL_USER'],
		                            passwd=settings['MYSQL_PASSWORD'],
		                            db=settings['MYSQL_DB'],
		                            charset="utf8",
		                            use_unicode=True)
		self.cursor = self.conn.cursor()
	
	def _insert_post(self, item):
		try:
			check = self.cursor.execute("""SELECT * FROM articles WHERE url=%s""", [item['url']])
			if not check:
				self.cursor.execute("""INSERT INTO articles
                (domain, url)
                VALUES (%s, %s)""", (item["domain"], item["url"]))
				self.conn.commit()
				print('Luu du lieu thanh cong')
			else:
				print("Du lieu nay da ton tai")
			return item
		except Exception as e:
			print('Co loi xay ra khi luu post', e)
			return item
