# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from django.core.handlers.wsgi import WSGIRequest





# @csrf_exempt
# def test_api(request):
#     return JsonResponse({"result": 0, "msg": "执行成功"})


@csrf_exempt
def getNovelList(request,pageIndex,pageSize):
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian
    # 获取booklist集合
    novel_list = db["book_list"]
    # pageIndex = request.GET.get('pageindex', 0)
    # pageIndex = 0
    index = int(pageIndex) * pageSize
    searchRes = novel_list.find().skip(index).limit(pageSize)

    rets = []
    for item in searchRes:
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0, "booklist": rets})

@csrf_exempt
def searchNovelList(request,keyword,pageIndex,pageSize):
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian
    # 获取booklist集合
    novel_list = db["book_list"]
    # pageIndex = request.GET.get('pageindex', 0)
    # keyword = request.GET.get('keyword', "")

    searchdic = {"$or":[
        {"novel_name": {'$regex' : ".*"+keyword+".*"}},
        {"novel_author": {'$regex' : ".*"+keyword+".*"}}
    ]}

    # pageIndex = 0
    index = int(pageIndex) * pageSize
    searchRes = novel_list.find(searchdic).skip(index).limit(pageSize)

    rets = []
    for item in searchRes:
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0, "booklist": rets})


@csrf_exempt
def getChapterById(request,bookid,chapterid):
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian

    # bookid = request.GET.get('bookid', "")
    # chapterid = request.GET.get('chapterid', "")

    # 获取booklist集合
    chapterlist = db[bookid]

    searchRes = chapterlist.find_one({"_id":chapterid})
    client.close()
    return JsonResponse({"result": 0, "chapter": searchRes})


@csrf_exempt
def getChapterList(request,bookid,chapterStartNumber,chapterEndNumber):
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian
   # // bookid = request.GET.get('bookid', "")
   #  chapterid = request.GET.get('chapterid', "")

    # 获取booklist集合
    chapterlist = db[bookid]

    searchRes = chapterlist.find({ "order_number" : { "$gte" : chapterStartNumber
, "$lte" : chapterEndNumber } })

    # pageIndex = 0
    rets = []
    for item in searchRes:
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0, "chapterlist": rets})

@csrf_exempt
def getCategoryNovelList(request,categoryName,pageIndex,pageSize):
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian
    # 获取booklist集合
    novel_list = db["book_list"]


    searchdic = {"novel_family":categoryName}

    # pageIndex = 0
    index = int(pageIndex) * pageSize
    searchRes = novel_list.find(searchdic).skip(index).limit(pageSize)

    # pageIndex = 0
    rets = []
    for item in searchRes:
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0, "novellist": rets})

