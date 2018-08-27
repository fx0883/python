# -*- coding: utf-8 -*-
import scrapy
import json
from pymongo import MongoClient
import uuid
import settings



class Mangaedan2Spider(scrapy.Spider):
    name = 'mangaedan2'
    allowed_domains = ['mangaedan.com']
    start_urls = ['http://www.baidu.com']
    pageIndex = 0
    pageSize = 100
    chapter_url = "https://www.mangaeden.com/api/chapter/"




    def parse(self, response):
        client = MongoClient(settings.MangadbConfig["url"])
        # 连接数据库
        db = client.mangaeden
        # 获取booklist集合
        mangalist = db["mangalist"]
        # pageIndex = request.GET.get('pageindex', 0)
        # pageIndex = 0
        index = int(self.pageIndex) * self.pageSize
        searchRes = mangalist.find().skip(index).limit(self.pageSize)


        for item in searchRes:
            mangaedenid = item['mangaedenid']
            for itemchapter in item['chapters']:
                chapterinfo_url = self.chapter_url + itemchapter[3] + "/"
                yield scrapy.Request(url=chapterinfo_url, meta={'mangaedenid': mangaedenid, "chapterid": itemchapter[3]}, callback=self.parse2,
                             dont_filter=True)

        client.close()
        pass





    def parse2(self, response):
        print(response.url)
        mangaedenid = response.meta['mangaedenid']
        chapterid = response.meta['chapterid']
        chapterinfo = json.loads(response.body.decode("utf-8"))

        chapterinfo['mangaedenid'] = mangaedenid
        chapterinfo['chapterid'] = chapterid
        chapterinfo["_id"] = str(uuid.uuid1())
        # for chapterItem in mangainfo['chapters']:
        #     chapterinfourl = self.chapterinfo_api + item[3] + "/"
        #     yield scrapy.Request(url=chapterinfourl, meta={'chapterid': item[3]}, callback=self.parse3, dont_filter=True)
        # chapterinfo['_id'] == str(uuid.uuid1())


        return chapterinfo