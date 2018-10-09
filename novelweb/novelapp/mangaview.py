# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from django.core.handlers.wsgi import WSGIRequest
import json
import simplejson
from pymongo import DESCENDING

# import bson.objectid




# @csrf_exempt
# def test_api(request):
#     return JsonResponse({"result": 0, "msg": "执行成功"})
MangadbConfig = {
    "url": "mongodb://127.0.0.1:27017"
}

@csrf_exempt
def getMangaList(request):

    pageIndex = 0
    pageSize = 20
    sortField = None
    categoryNames = None
    if request.method == 'POST':
        received_json_data = simplejson.loads(request.body)
        print(received_json_data)
        pageIndex = received_json_data["pageIndex"]
        pageSize = received_json_data["pageSize"]
        if "sortField" in received_json_data.keys():
            sortField = received_json_data["sortField"]
        if "categoryNames" in received_json_data.keys():
            categoryNames = received_json_data["categoryNames"]
    else:
        return JsonResponse({"result": -1, "mangalist":[]})
    client = MongoClient(MangadbConfig["url"])
    # 连接数据库
    db = client.mangaeden
    manga_list = db["mangalist"]
    index = int(pageIndex) * pageSize
    searchRes = None
    if categoryNames != None:
        searchdic = {"$or":[]}
        for categoryName in categoryNames:
            searchdic["$or"].append({"categoriesstr": {'$regex': ".*" + categoryName + ".*"}})
        if sortField == None:
            searchRes = manga_list.find(searchdic).skip(index).limit(pageSize)
        else:
            searchRes = manga_list.find(searchdic).sort([{sortField, -1}]).skip(index).limit(pageSize)
    else:
        if sortField == None:
            searchRes = manga_list.find().skip(index).limit(pageSize)
        else:
            searchRes = manga_list.find().sort([{sortField, -1}]).skip(index).limit(pageSize)
    total = searchRes.count()
    rets = []
    for item in searchRes:
        # item['_id'] = str(item['_id'])
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0,"total":total, "mangalist": rets})

@csrf_exempt
def getMangaByMangaId(request):
    if request.method == 'POST':
        received_json_data = simplejson.loads(request.body)
        print(received_json_data)
    else:
        return JsonResponse({"result": -1, "mangalist":[]})
    client = MongoClient(MangadbConfig["url"])
    # 连接数据库
    db = client.mangaeden
    manga_list = db["mangalist"]

    searchdic = {"mangaedenid":{ "$in":received_json_data["mangaedenid"]}}

    searchRes = manga_list.find(searchdic)

    rets = []
    for item in searchRes:
        # item['_id'] = str(item['_id'])
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0, "mangalist": rets})

@csrf_exempt
def searchMangalList(request):
    pageIndex = 0
    pageSize = 20
    sortField = None
    categoryNames = None
    keyword = None
    if request.method == 'POST':
        received_json_data = simplejson.loads(request.body)
        print(received_json_data)
        pageIndex = received_json_data["pageIndex"]
        pageSize = received_json_data["pageSize"]
        keyword = received_json_data["keyword"]
        if "sortField" in received_json_data.keys():
            sortField = received_json_data["sortField"]
        if "categoryNames" in received_json_data.keys():
            categoryNames = received_json_data["categoryNames"]
    else:
        return JsonResponse({"result": -1, "mangalist":[]})
    client = MongoClient(MangadbConfig["url"])
    # 连接数据库
    db = client.mangaeden
    manga_list = db["mangalist"]

    searchdic1 = {"$or":[
        {"title": {'$regex': ".*"+keyword+".*"}},
        {"author": {'$regex': ".*"+keyword+".*"}}
    ]}
    searchdic2 = None
    searchdic = None
    if categoryNames != None:
        searchdic2 = {"$or":[]}
        for categoryName in categoryNames:
            searchdic2["$or"].append({"categoriesstr": {'$regex': ".*" + categoryName + ".*"}})
    if searchdic2!=None:
        searchdic = {"$and":[searchdic1,searchdic2]}
    else:
        searchdic = searchdic1
    # pageIndex = 0
    index = int(pageIndex) * pageSize
    searchRes = None
    if sortField == None:
        searchRes = manga_list.find(searchdic).skip(index).limit(pageSize)
    else:
        searchRes = manga_list.find(searchdic).sort([{sortField, -1}]).skip(index).limit(pageSize)
    total = searchRes.count()
    rets = []
    for item in searchRes:
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0,"total":total, "mangalist": rets})

@csrf_exempt
def searchMangalListByAuthor(request,author,pageIndex,pageSize):
    client = MongoClient(MangadbConfig["url"])
    # 连接数据库
    db = client.mangaeden
    manga_list = db["mangalist"]

    searchdic = {"author": author}
    # pageIndex = 0
    index = int(pageIndex) * pageSize
    searchRes = manga_list.find(searchdic).sort([{"hits",-1},{"create",-1}]).skip(index).limit(pageSize)
    total = searchRes.count()
    rets = []
    for item in searchRes:
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0, "total":total,"mangalist": rets})

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
    total = searchRes.count()
    # pageIndex = 0
    rets = []
    for item in searchRes:
        rets.append(item)
        print(item)
    client.close()
    return JsonResponse({"result": 0,"total":total, "novellist": rets})


@csrf_exempt
def getCategoryNames(request):
    client = MongoClient(MangadbConfig["url"])
    # 连接数据库
    db = client.mangaeden
    # 获取booklist集合
    categoryList = db["mangacategory"]

    retCategory = categoryList.find()
    total = retCategory.count()
    retAllNovelCategory = []
    for itemCategory in retCategory:
        categoryName = itemCategory['category']
        retAllNovelCategory.append(categoryName)

    client.close()
    return JsonResponse({"result": 0,"total":total, "categoryNames": retAllNovelCategory})


