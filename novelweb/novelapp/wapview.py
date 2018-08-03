# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from django.views.decorators.cache import cache_page

import numpy as np

# @cache_page(60 * 15) # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
# def index(request):
#     pageIndex = 0
#     pageSize = 10
#     categoryName = "网游竞技"
#     client = MongoClient("mongodb://127.0.0.1:27017")
#     # 连接数据库
#     db = client.dingdian
#     # 获取booklist集合
#     novel_list = db["book_list"]
#
#     searchdic = {"novel_family": categoryName}
#
#     # pageIndex = 0
#     index = int(pageIndex) * pageSize
#     searchRes = novel_list.find(searchdic).skip(index).limit(pageSize)
#
#     # pageIndex = 0
#     rets = []
#     for item in searchRes:
#         rets.append(item)
#         print(item)
#     client.close()
#
#
#
#     retdict = {"categoryName": "网游竞技","recommend":rets[0],"novelList": rets}
#
#
#     # 读取数据库等 并渲染到网页
#     return render(request, 'index.htm', retdict)

@cache_page(60 * 15) # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
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
            print(item)
        print(retCategory)

        retAllNovelCategory.append({"categoryName":categoryName,"recommend":rets[0],"novelList":rets})

    client.close()

    #构建随机数
    selectCount = 0
    categoryCount = len(retAllNovelCategory)
    if(categoryCount<=1):
        selectCount = 1
    selectCount = categoryCount/2
    arr = getRandomArray(selectCount)
    retAllNovelCategoryRandom = []
    for itemindex in arr:
        retAllNovelCategoryRandom.append(retAllNovelCategory[int(itemindex)])

    print(retAllNovelCategory)
    return render(request, 'index.htm', {"retAllNovelCategory":retAllNovelCategoryRandom})



@cache_page(60 * 15) # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def getNovelInfo(request,bookid):
    pageIndex = 0
    pageSize = 10
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian

    novel_list = db["book_list"]

    retRes = novel_list.find_one({"chapterlistId":bookid})

    return render(request, 'article.htm', retRes)

def getRandomArray(endindex):
    arr = np.random.permutation(int(endindex))
    return arr
