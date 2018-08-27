# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from django.core.handlers.wsgi import WSGIRequest

# import bson.objectid



# @csrf_exempt
# def test_api(request):
#     return JsonResponse({"result": 0, "msg": "执行成功"})
MangadbConfig = {
    "url": "mongodb://127.0.0.1:27017"
}

@csrf_exempt
def getMangaList(request,pageIndex,pageSize):
    client = MongoClient(MangadbConfig["url"])
    # 连接数据库
    db = client.mangaeden
    manga_list = db["mangalist"]
    # pageIndex = request.GET.get('pageindex', 0)
    # pageIndex = 0
    index = int(pageIndex) * pageSize
    searchRes = manga_list.find().skip(index).limit(pageSize)

    rets = []
    for item in searchRes:
        # item['_id'] = str(item['_id'])
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0, "mangalist": rets})

@csrf_exempt
def searchMangalList(request,keyword,pageIndex,pageSize):
    client = MongoClient(MangadbConfig["url"])
    # 连接数据库
    db = client.mangaeden
    manga_list = db["mangalist"]

    searchdic = {"$or":[
        {"title": {'$regex': ".*"+keyword+".*"}},
        {"author": {'$regex': ".*"+keyword+".*"}}
    ]}

    # pageIndex = 0
    index = int(pageIndex) * pageSize
    searchRes = manga_list.find(searchdic).skip(index).limit(pageSize)

    rets = []
    for item in searchRes:
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0, "mangalist": rets})


@csrf_exempt
def getMangaChapterById(request,mangaid,chapterid):
    client = MongoClient(MangadbConfig["url"])
    # 连接数据库
    db = client.mangaeden

    chapterlist = db[mangaid]

    searchRes = chapterlist.find_one({"chapterid":chapterid})
    client.close()
    return JsonResponse({"result": 0, "chapter": searchRes})



@csrf_exempt
def getCategoryMangaList(request,categoryName,pageIndex,pageSize):
    client = MongoClient(MangadbConfig["url"])
    # 连接数据库
    db = client.mangaeden
    # 获取booklist集合
    manga_list = db["mangalist"]


    searchdic = {"categoriesstr": {'$regex': ".*"+categoryName+".*"}}

    # pageIndex = 0
    index = int(pageIndex) * pageSize
    searchRes = manga_list.find(searchdic).skip(index).limit(pageSize)

    # pageIndex = 0
    rets = []
    for item in searchRes:
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0, "novellist": rets})



