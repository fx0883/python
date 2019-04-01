# -*- coding: utf-8 -*-
import scrapy
import re
import execjs
import json
import time

class Ting56appSpider(scrapy.Spider):
    name = 'ting56app'
    allowed_domains = ['ting56.com']
    start_urls = []
    ctx = None
    post_url = "http://www.ting56.com/player/tingchina.php"
    chapter_name_re = "2369-0-(.*?).html"


    def start_requests(self):
        for i in range(1107, 1108):
            url = 'http://www.ting56.com/video/2369-0-%s.html' % i
            self.start_urls.append(url)

        for itemurl in self.start_urls:
            time.sleep(1)
            yield scrapy.Request(url=itemurl,callback=self.parse)

    def parse(self, response):
        body = response.body.decode('gbk')
        # print(body)
        param = re.findall("FonHen_JieMa\('([^']*)'\)", body)
        if(len(param)<1):
            return
        print(param[0])
        paramRet= self.getParam(param[0])
        print(paramRet)
        # passre
        chapter_name = self.getChapterName(response.url)

        yield scrapy.FormRequest(
            url=self.post_url,
            meta={'chapter_name': chapter_name},
            formdata=paramRet,
            callback=self.parse_post
        )
    def parse_post(self, response):
        print(response.body)
        chapter_name = response.meta['chapter_name']
        decode_json = json.loads(response.body.decode('utf-8'))
        decode_json['chapter_name'] = chapter_name
        yield decode_json

    def getChapterName(self, strSource):
        retlist = re.findall(self.chapter_name_re, strSource)
        return retlist[0]

    # 执行本地的js

    def getjs(self):
        f = open("./js/main.js", 'r', encoding='UTF-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr

    def getParam(self,strSource):

        if self.ctx == None:
            jsstr = self.getjs()
            self.ctx = execjs.compile(jsstr)
        return self.ctx.call('getParam', strSource)