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




        section_url_downloaded_collection = db.section_url_collection
        # index=1

        if section_url_downloaded_collection.find_one({"url": item["url"]}) != None:
            print(item["url"] + "========>已经下载过了......")
            client.close()
            return item
        else:
            section_url_downloaded_collection.insert({"url": item["url"]})
            chapterlist.insert(item)
        client.close()

        return item
