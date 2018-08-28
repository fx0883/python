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
from mongoconn import MongoConn
from mongoconn import MONGODB_CONFIG


class MangaedencrawlPipeline(object):
    def process_item(self, item, spider):
        try:
            if len(item['chapters']) > 0:
                mongoconn = MongoConn()
                # 连接数据库
                db = mongoconn.db

                categoriesstr = ','.join(item['categories'])
                item['categoriesstr'] = categoriesstr

                mangacategory = db['mangacategory']
                for categoryItem in item['categories']:
                    if not mangacategory.find_one({"category": categoryItem}):
                        mangacategory.insert({"_id": str(uuid.uuid1()), "category": categoryItem})

                mangalist = db['mangalist']
                if not mangalist.find_one({"mangaedenid": item["mangaedenid"]}):
                    mangalist.insert(item)
                mongoconn.close()
                print(item)
            return item
        except Exception as e:
            print(e)

