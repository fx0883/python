# -*- coding: utf-8 -*-
import scrapy
import json
from pymongo import MongoClient
import uuid

class MangaedanSpider(scrapy.Spider):
    name = 'mangaedan'
    allowed_domains = ['mangaeden.com']
    server_link = 'https://www.mangaeden.com/api/list/0/?p='
    start_urls = []

    chapterlist_api = 'https://www.mangaeden.com/api/manga/'
    chapterinfo_api = 'https://www.mangaeden.com/api/chapter/'

    def __init__(self):
        for i in range(0, 40):
            page_url = self.server_link + str(i)
            print(page_url)
            self.start_urls.append(page_url)


    # def parse_start_url(self, response):
    #     print(response.body)
    #     mangalist = json.loads(response.body.decode("utf-8"))['manga']
    #     for item in mangalist:
    #         chapterlisturl = self.chapterlist_api+item['i']+"/"
    #         yield scrapy.Request(url=chapterlisturl, meta={'item': item}, callback=self.parse2, dont_filter=True)


    def parse(self, response):
        print(response.body)
        mangalist = json.loads(response.body.decode("utf-8"))['manga']

        client = MongoClient("mongodb://127.0.0.1:27017")
        # 连接数据库
        db = client.mangaeden

        mangalistdb = db['mangalist']

        for item in mangalist:
            chapterlisturl = self.chapterlist_api+item['i']+"/"
            mangalistRet = mangalistdb.find_one({"mangaedenid": item['i']})
            if mangalistRet != None:
                continue
            yield scrapy.Request(url=chapterlisturl, meta={'mangaedenid': item['i']}, callback=self.parse2, dont_filter=True)
        client.close()

    def parse2(self, response):
        print(response.url)
        mangaedenid = response.meta['mangaedenid']
        mangainfo = json.loads(response.body.decode("utf-8"))
        mangainfo["mangaedenid"] = mangaedenid
        mangainfo["_id"] = str(uuid.uuid1())
        # for chapterItem in mangainfo['chapters']:
        #     chapterinfourl = self.chapterinfo_api + item[3] + "/"
        #     yield scrapy.Request(url=chapterinfourl, meta={'chapterid': item[3]}, callback=self.parse3, dont_filter=True)
        return mangainfo

    def parse3(self, response):
        print(response.url)
        chapterid = response.meta['chapterid']
        chapterinfo = json.loads(response.body.decode("utf-8"))
        chapterinfo['chapterid'] = chapterid
        return chapterinfo