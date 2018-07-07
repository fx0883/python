# -*- coding: utf-8 -*-
import scrapy

from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request

from bs4 import BeautifulSoup

#from txtcrawler.items import BookItem

from items import BookItem,ChapterItem

import re
import uuid

class TxtnovelSpider(scrapy.Spider):
    name = 'txtnovel'
    allowed_domains = ['jjxsw.cc']
    start_urls = ['http://www.jjxsw.cc/txt/list5-1.html']



    def parse(self, response):
        body = response.body.decode('utf-8')
        soup = BeautifulSoup(body, 'html.parser')
        for t1 in soup.find_all("div",{"class":"listbg"}):
            print(t1)
            bookItem = BookItem()
            bookItem["id"] = str(uuid.uuid1())
            typeTag = t1.find("span",{"class":"classname"})


            bookItem['type'] = getOneStrUseRe("\[([^\]]*)",typeTag.text)

            titleTag = t1.find("a")
            bookItem['title'] = titleTag.text
            bookItem['url'] = titleTag["href"]


            t2 = t1.find_all("div",{"style":"padding:0 20px"})

            for t2Item in t2:
                if len(list(t2Item.children)) > 1:
                    # bookItem.author = t2Item.contents[0]
                    curTagText = t2Item.text
                    bookItem['author'] = getOneStrUseRe("小说作者：(.*?)文件大小",curTagText)

                    readtimesStr = getOneStrUseRe("下载次数：(.*?)次",curTagText)
                    bookItem['readtimes'] = convert2int(readtimesStr)
                    bookItem['author'] = trim(bookItem['author'])
                else:
                    bookItem['description'] = t2Item.text

            # bookItem["imageurl"] = "123123"
            #
            # yield bookItem
            yield Request(url=bookItem['url'], meta={"bookitem": bookItem}, callback=self.parsebookdetail)

        # 查询是否有下一页
        nextpagenode = soup.find("a", {"class": "next"})
        if nextpagenode != None:
            yield Request(url=nextpagenode['href'], meta={}, callback=self.parse)

    def parsebookdetail(self,response):
        bookItem = response.meta["bookitem"]
        bookId = bookItem["id"]



        body = response.body.decode('utf-8')
        soup = BeautifulSoup(body, 'html.parser')
        readnode = soup.find(text="点击在线全文阅读^_^")
        # text11 = readnode.parent.text
        chapterlisturl = readnode.parent.parent["href"]

        imageNode = soup.find("span",{"class":"img"})
        bookItem["imageurl"] = imageNode.find("img")["src"]

        yield bookItem
        yield Request(url=chapterlisturl, meta={"bookId": bookId}, callback=self.parsebookchatperlist)

    def parsebookchatperlist(self, response):
        bookId = response.meta["bookId"]
        body = response.body.decode('utf-8')
        soup = BeautifulSoup(body, 'html.parser')
        chapterlistnode = soup.find("div",{"class":"read_list"})

        index = 1
        for item in chapterlistnode.find_all("a"):
            chapteritem = ChapterItem()
            chapteritem["id"] = str(uuid.uuid1())
            chapteritem["orderid"] = index
            chapteritem["bookid"] = bookId
            chapteritem["title"] = item["title"]
            chapteritem["url"] = item["href"]
            index = index + 1
            yield Request(url=chapteritem["url"], meta={"chapteritem": chapteritem}, callback=self.parsebookchatperdetail)

    def parsebookchatperdetail(self, response):
        chapteritem = response.meta["chapteritem"]
        body = response.body.decode('utf-8')
        soup = BeautifulSoup(body, 'html.parser')
        contentnode = soup.find("div",{"id":"view_content_txt"})
        contentnode.find("div",{"class":"view_page"}).clear()
        contentText = contentnode.text
        # contentText = contentText.replace("<br>", "")
        chapteritem["content"] = dealcontent(contentText)
        # print(chapteritem["content"])
        print("==============>")
        print(chapteritem["orderid"])
        print(chapteritem["title"])
        yield chapteritem


def dealcontent(strSource):
    strSource = strSource.replace("<br>", "")
    strSource = strSource.replace('"', "")
    pattern = re.compile("[\s\S]*?[-]?用户上传之内容开始[-]*")
    return re.sub(pattern, '', strSource)



def getOneStrUseRe(strRe,strSource):
    # re.match(strRe,)
    retlist = re.findall(strRe,strSource)

    if len(retlist)>0:
        return retlist[0]
    return ''

# -*- coding: utf-8 -*-
def trim(s):
    if len(s)==0:
        return ''
    if s[:1]==' ':
        return trim(s[1:])
    elif s[-1:]=='':
        return trim(s[:-1])
    else:
        return s

def convert2int(strValue):
    retlist = re.findall("(^[0-9]*)", strValue)
    retStr = strValue
    if len(retlist)>0:
        retStr = retlist[0]

    ret = 0
    try:
        ret = int(retStr)
    except Exception as err:
        print(err)
        pass
    matchw = re.match(r".*?w.*?",strValue,re.I)
    if matchw!=None:
        ret = ret*10000
    return ret