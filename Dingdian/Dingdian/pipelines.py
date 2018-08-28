# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 因为爬取整个网站时间较长，这里为了实现断点续传，我们把每个小说下载完成的
# 章节地址存入数据库一个单独的集合里，记录已完成抓取的小说章节

from pymongo import MongoClient
from urllib import request
from bs4 import BeautifulSoup
import re
import uuid
import spiders.downloader
import hashlib
import time
import datetime
import operator as op


# 在pipeline中我们将实现下载每个小说，存入MongoDB数据库

class DingdianxiaoshuoPipeline(object):
    def process_item(self, item, spider):
        try:
            # print("马衍硕")
            # 如果获取章节链接进行如下操作
            if "novel_section_urls" in item:
                # 获取Mongodb链接
                client = MongoClient("mongodb://127.0.0.1:27017")
                # 连接数据库
                db = client.dingdian

                # 获取booklist集合
                novel_list = db["book_list"]
                # 获取小说名称
                novel_name = item['novel_name']
                # 根据小说名字，使用集合，没有则创建

                novel_author = item['novel_author']
                # if novel_author == "":
                #     novel_author = str(uuid.uuid1())
                imgurl = item['novel_imgurl']
                chapterList = []
                cur_md5 = self.getMd5NovelNameAndAuthor(novel_name, novel_author)
                # novel=db[novel_name]
                cur_novel = novel_list.find_one({"novel_md5": cur_md5})

                cur_novel_id = ""
                chapterlistId = ""
                if cur_novel != None:
                    chapterList = cur_novel["chapterlist"]
                    cur_novel_id = cur_novel["_id"]
                    chapterlistId = cur_novel["chapterlistId"]
                else:
                    cur_novel_id = str(uuid.uuid1())
                    chapterlistId = str(uuid.uuid1())

                    novel_list.insert(
                        {"_id": cur_novel_id, "novel_name": item['novel_name'], "novel_family": item['novel_family'],
                         "novel_author": item['novel_author'], "novel_status": item['novel_status'],
                         "novel_imgurl": imgurl, "novel_description": item['novel_description'],
                         "chapterlist": chapterList, "chapterlistId": chapterlistId, "novel_md5": cur_md5,"novel_section_urls": len(item['novel_section_urls'])
                         ,"novel_url":item["novel_url"]})

                    ret_novel_idStr = str(cur_novel_id)
                    spiders.downloader.download_image(imgurl, "./bookimg", ret_novel_idStr)

                novel = db[chapterlistId]
                # novel_id = novel_name+"_"+novel_author

                # 获取小说类型
                novel_family = item['novel_family']
                # novel_familydb = db[novel_family]
                novel_category_collection = db.novel_category
                if not novel_category_collection.find_one({"category": novel_family}):
                    novel_category_collection.insert({"_id": str(uuid.uuid1()), "category": novel_family})
                # 使用记录已抓取网页的集合，没有则创建
                section_url_downloaded_collection = db.section_url_collection
                # index=1

                if section_url_downloaded_collection.find_one({"url": item["novel_url"]}) != None:
                    print(item["novel_name"] + "========>已经下载过了......")
                    client.close()
                    return item
                index2 = 1
                print("正在下载：" + item["novel_name"])

                # 根据小说每个章节的地址，下载小说各个章节
                for section_url in item['novel_section_urls']:

                    # 根据对应关系，找出章节名称
                    section_name = item["section_url_And_section_name"][section_url]
                    # 如果将要下载的小说章节没有在section_url_collection集合中，也就是从未下载过，执行下载
                    # 否则跳过
                    if not section_url_downloaded_collection.find_one({"url": section_url}):
                        # 使用urllib库获取网页HTML
                        response = request.Request(url=section_url)
                        download_response = request.urlopen(response)
                        download_html = download_response.read().decode('utf-8')
                        # 利用BeautifulSoup对HTML进行处理，截取小说内容
                        soup_texts = BeautifulSoup(download_html, 'lxml')
                        content = soup_texts.find("dd", attrs={"id": "contents"}).getText()

                        index2 = index2 + 1
                        index = self.getinttime()
                        section_id = str(uuid.uuid1())
                        # 向Mongodb数据库插入下载完的小说章节内容
                        novel.insert(
                            {"_id": section_id, "novel_name": item['novel_name'], "novel_family": item['novel_family'],
                             "novel_author": item['novel_author'], "novel_status": item['novel_status'],
                             "section_name": section_name, "order_number": index,
                             "content": content})
                        print(index)

                        # 下载完成，则将章节地址存入section_url_downloaded_collection集合
                        section_url_downloaded_collection.insert({"url": section_url})
                        chapterList.append({"section_id": section_id, "section_name": section_name})
                        print("======> " + section_name)
                        novel_list.update({"_id": cur_novel_id}, {"$set": {"chapterlist": chapterList}})
                        if index2 > 3:
                            break

                # print("当前状态=========》" + item["novel_status"])
                # if str('完本') in str(item["novel_status"]):
                #     print("当前状态=========》" + item["novel_status"])
                #     section_url_downloaded_collection.insert({"url": item["novel_url"]})
                # else:
                #     print("当前状态不是完本=========》" + item["novel_status"])


                print("下载完成：" + item['novel_name'])
                client.close()
                return item
        except Exception as e:
            print(e)


    def getinttime(self):
        t = time.time()
        return int(round(t * 1000))

    def getMd5NovelNameAndAuthor(self, novelName, author):
        retStr = str(novelName + author)
        md5 = hashlib.md5(retStr.encode("utf-8")).hexdigest()
        return str(md5)
