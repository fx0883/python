# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from django.views.decorators.cache import cache_page

import numpy as np
import json



@csrf_exempt
@cache_page(60 * 15)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def index(request):
    pageIndex = 0
    pageSize = 10
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian

    # 获取booklist集合
    novel_list = db["book_list"]
    categoryList = db["novel_category"]

    retCategory = categoryList.find()
    retAllNovelCategory = []
    for itemCategory in retCategory:
        categoryName = itemCategory['category']
        searchdic = {"novel_family": categoryName}
        # pageIndex = 0
        index = int(pageIndex) * pageSize
        searchRes = novel_list.find(searchdic).skip(index).limit(pageSize)
        # pageIndex = 0
        rets = []
        for item in searchRes:
            rets.append(item)
            # print(item)
        print(retCategory)

        retAllNovelCategory.append({"categoryName": categoryName, "recommend": rets[0], "novelList": rets})

    client.close()

    # 构建随机数
    selectCount = 0
    categoryCount = len(retAllNovelCategory)
    if (categoryCount <= 1):
        selectCount = 1
    selectCount = categoryCount / 2
    arr = getRandomArray(selectCount)
    retAllNovelCategoryRandom = []
    for itemindex in arr:
        retAllNovelCategoryRandom.append(retAllNovelCategory[int(itemindex)])

    print(retAllNovelCategory)
    return render(request, 'index.htm', {"retAllNovelCategory": retAllNovelCategoryRandom})

@csrf_exempt
# @cache_page(60 * 15)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def getNovelInfo(request, bookid):
    pageIndex = 0
    pageSize = 10
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian

    novel_list = db["book_list"]

    retRes = novel_list.find_one({"chapterlistId": bookid})

    client.close()
    # return render(request, 'article.htm', retRes)


    # retRes["recommend"] = retRes[]


    curresponse = render(request, 'article.htm', retRes)
    # curresponse.set_cookie("curBookinfo", retRes)



    # curresponse.delete_cookie('novelinfo')
    # curresponse.set_cookie('novelinfo', json_str)

# f
    return curresponse

@csrf_exempt
# @cache_page(60 * 15)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def getChapterInfo(request, bookid, chapterid):
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian

    # booklist = db["book_list"];
    #
    chapterlist = db[bookid]

    retRes = chapterlist.find_one({"_id": chapterid})

    # retRes["content"] = str(retRes["content"].replace("\r\n", "<br/>")
    #                         .replace("\xa0", "&nbsp").replace("\n", "<br/>").replace("\"", ""));

    # retRes["content"] = retRes["content"].replace("\r\n", "&lt;br&gt;")
    retRes["id"] = chapterid
    retRes["bookId"] = bookid

    client.close()

    return render(request, 'chapterinfo.htm', retRes)


@csrf_exempt
def search(request):
    keyword = request.POST['key']
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian
    # 获取booklist集合
    novel_list = db["book_list"]
    # pageIndex = request.GET.get('pageindex', 0)
    # keyword = request.GET.get('keyword', "")

    searchdic = {"$or": [
        {"novel_name": {'$regex': ".*" + keyword + ".*"}},
        {"novel_author": {'$regex': ".*" + keyword + ".*"}}
    ]}

    pageIndex = 0
    pageSize = 50
    index = int(pageIndex) * pageSize
    searchRes = novel_list.find(searchdic).skip(index).limit(pageSize)

    rets = []
    for item in searchRes:
        rets.append(item)
        print(item)
    client.close()
    # return JsonResponse({"result": 0, "booklist": rets})

    return render(request, "list.htm", {"keyword": keyword, "recommend": rets[0], "novelList": rets})


def getRandomArray(endindex):
    arr = np.random.permutation(int(endindex))
    return arr
