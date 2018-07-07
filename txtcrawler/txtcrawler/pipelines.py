# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html





import json
import spiders.downloader
import uuid
import pymysql
import spiders.pconfig
from items import BookItem,ChapterItem
from redisopera import RedisOpera




class TxtcrawlerPipeline(object):
    #连接登陆mysql，新建数据表
    def __init__(self):
        print("TxtcrawlerPipeline==>init")
        self.initDB()
        #初始化redis
        self.Redis = RedisOpera('insert')


    def initDB(self):
        try:
            self.conn = pymysql.connect(user=spiders.pconfig.mysqldb["user"],
                                        passwd=spiders.pconfig.mysqldb["password"],
                                        host=spiders.pconfig.mysqldb["host"],
                                        db=spiders.pconfig.mysqldb["db"],
                                        charset=spiders.pconfig.mysqldb["charset"])
        except Exception as err:
            print(err)
            exit(0)

    #mysql写入
    def process_item(self, item, spider):

        if isinstance(item, BookItem):
            try:
                self.insertbookitem(item)
                self.Redis.write(item['url'])
            except Exception as err:
                print(err)
                pass
        elif isinstance(item, ChapterItem):
            try:
                self.insertchapteritem(item)
                self.Redis.write(item['url'])
            except Exception as err:
                print(err)
                pass


    #关闭连接
    def close_spider(self):
        self.conn.close()


    def insertbookitem(self,item):
        id = item["id"]
        title = item["title"]
        author = item["author"]
        booktype = item["type"]
        description = item["description"]
        url = item["url"]
        imageurl = item["imageurl"]
        readtimes = item["readtimes"]
        cur = self.conn.cursor()

        sql = """insert into bookmysqldb.bookitem
(id,title,author,description,booktype,url,imageurl,readtimes) values
        ('%s','%s','%s','%s','%s','%s','%s','%d')""" % (id,title, author,description,booktype,url,imageurl,readtimes)

        cur.execute(sql.encode('utf-8'))

        spiders.downloader.download_image(imageurl,"./bookimg",id,)
        self.conn.commit()

    def insertchapteritem(self, item):
        id = item["id"]
        orderid = item["orderid"]
        bookid = item["bookid"]
        title = item["title"]

        url = item["url"]
        content = item["content"]

        # subplace("\xc2\xa0", " ")
        # content = content.replace("\\xc2\\xa0", " ");
        # content = content.replace("\\xC2\\xA0", " ");

        # content = "".join(content.split())


        move = dict.fromkeys((ord(c) for c in u"\xc2\xa0\xC2\xA0"))
        content = content.translate(move)

        cur = self.conn.cursor()
        sql = """insert into bookmysqldb.chapteritem 
(id,orderid,bookid,title,url,content) values 
        ('%s','%d','%s','%s','%s','%s')""" % (id, orderid, bookid, title, url, content)

        cur.execute(sql.encode('utf-8'))

        self.conn.commit()