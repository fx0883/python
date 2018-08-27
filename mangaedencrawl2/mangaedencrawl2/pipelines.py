# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import uuid
import settings

class Mangaedencrawl2Pipeline(object):
    def process_item(self, item, spider):
        client = MongoClient(settings.MangadbConfig["url"])
        # 连接数据库
        db = client.mangaeden

        chapterlist = db[item['mangaedenid']]

        chapterlist.insert(item)
        client.close()

        return item
