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



class book630Spider(scrapy.Spider):
    name = 'book603'
    allowed_domains = ['630book.la']
    mainurl = "http://www.630book.la/"
    start_urls = ['http://www.630book.la/list/1.html']



    def parse(self, response):
        # body = response.body.decode('utf-8')
        body = response.body.decode('gbk')
        # body = body_
        soup = BeautifulSoup(body, 'html.parser')
        titlelistTag = soup.find("ul",{"class":"titlelist"})


        for t1 in titlelistTag.find_all("li"):
            print(t1)
            bookItem = BookItem()
            bookItem["id"] = str(uuid.uuid1())


            titleTag = t1.find("div",{"class":"zp"}).find("a")
            bookItem['title'] = titleTag.text
            bookItem['url'] = titleTag["href"]

            authorTag = t1.find("div",{"class":"author"})
            bookItem['author'] = authorTag.text


            yield Request(url=bookItem['url'], meta={"bookitem": bookItem}, callback=self.parsebookdetail)
        #
        # # 查询是否有下一页
        # nextpagenode = soup.find("a", {"class": "next"})
        # if nextpagenode != None:
        #     yield Request(url=nextpagenode['href'], meta={}, callback=self.parse)

    def parsebookdetail(self,response):
        bookItem = response.meta["bookitem"]
        bookId = bookItem["id"]



        body = response.body.decode('gbk')
        soup = BeautifulSoup(body, 'html.parser')


        booktypeTag = soup.find("div",{"class":"nav-mbx"})
        booktypeTag.find("div",{"class":"fr"}).clear()
        booktypeTag = booktypeTag.find("a",{"target":"_blank"})
        bookItem["booktype"] = booktypeTag.text



        imgTag = soup.find("div",{"class":"img_in"})
        imgTag = imgTag.find("img")

        bookItem["imageurl"] =  imgTag["src"]

        descriptionTag = soup.find("div",{"id":"intro"})
        bookItem["description"] = dealrn(descriptionTag.text)


        readtimesTag = soup.find("div",{"class":"options"})
        readtimesStr = readtimesTag.find(text=re.compile("阅读数：.*"))

        readtimesStr = getOneStrUseRe("阅读数：(.*)",readtimesStr)

        bookItem["readtimes"] = convert2int(readtimesStr)

        chapterlistnode = soup.find("dl",{"class":"zjlist"})

        index = 1
        for item in chapterlistnode.find_all("dd"):
            itemTag = item.find("a")
            if itemTag == None:
                continue
            chapteritem = ChapterItem()

            chapteritem["id"] = str(uuid.uuid1())
            chapteritem["orderid"] = index
            chapteritem["bookid"] = bookId


            chapteritem["title"] = itemTag.text


            chapteritem["url"] = self.mainurl + itemTag["href"]
            index = index + 1
            yield Request(url=chapteritem["url"], meta={"chapteritem": chapteritem}, callback=self.parsebookchatperdetail)



        yield bookItem


    # def parsebookchatperlist(self, response):
    #     bookId = response.meta["bookId"]
    #     body = response.body.decode('utf-8')
    #     soup = BeautifulSoup(body, 'html.parser')
    #     chapterlistnode = soup.find("div",{"class":"read_list"})
    #
    #     index = 1
    #     for item in chapterlistnode.find_all("a"):
    #         chapteritem = ChapterItem()
    #         chapteritem["id"] = str(uuid.uuid1())
    #         chapteritem["orderid"] = index
    #         chapteritem["bookid"] = bookId
    #         chapteritem["title"] = item["title"]
    #         chapteritem["url"] = item["href"]
    #         index = index + 1
    #         yield Request(url=chapteritem["url"], meta={"chapteritem": chapteritem}, callback=self.parsebookchatperdetail)

    def parsebookchatperdetail(self, response):
        chapteritem = response.meta["chapteritem"]
        body = response.body.decode('gbk')
        soup = BeautifulSoup(body, 'html.parser')
        contentnode = soup.find("div",{"id":"content"})
        # contentnode.find("div",{"class":"view_page"}).clear()
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
    pattern = re.compile("[\s\S]*?恋上你看书网 WWW.630BOOK.LA.*")

    strSource = re.sub(pattern, '', strSource)
    strSource = strSource.replace("'", "")
    return strSource

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
def dealrn(s):
    s = s.replace('\r', '').replace('\n', '').replace('\t', '').replace("'","")
    move = dict.fromkeys((ord(c) for c in u"\xc2\xa0\xC2\xA0"))
    s = s.translate(move)
    s = trim(s)
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