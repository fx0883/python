# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from urllib import request
from bs4 import BeautifulSoup
import re
import uuid



class MangaedencrawlPipeline(object):
    def process_item(self, item, spider):
        if len(item['chapters']) > 0:
            client = MongoClient("mongodb://127.0.0.1:27017")
            # 连接数据库
            db = client.mangaeden

            mangalist = db['mangalist']

            mangalist.insert(item);
            client.close()
            print(item)
        return item
