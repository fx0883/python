from django.test import TestCase

# Create your tests here.
from pymongo import MongoClient
import hashlib
import json

# client = MongoClient("mongodb://127.0.0.1:27017")
# # 连接数据库
# db = client.dingdian
# # 获取booklist集合
# novel_list = db["book_list"]
# searchRes = novel_list.find({"$or":[{"novel_name": {'$regex' : ".*网游.*"}},{"novel_author": {'$regex' : ".*网游.*"}}]})
# # searchRes = novel_list.find()
# #
# for item in searchRes:
#     print(item)
#
#
# print(searchRes)


# client = MongoClient("mongodb://127.0.0.1:27017")
# # 连接数据库
# db = client.dingdian
#
# bookid = "一只哥斯拉的时空之旅_旅行的土拨鼠"
# chapterid = "67d1e398-8eef-11e8-bd8a-6003088a50b6"
#
# # 获取booklist集合
# chapterlist = db[bookid]
#
# searchRes = chapterlist.find_one({"_id":chapterid})
#
# # pageIndex = 0
#
#
# # rets = []
# # for item in searchRes:
# #     rets.append(item)
# #     print(item)
#
# print(searchRes)
# client.close()
# # return JsonResponse({"result": 0, "chapterlist": rets})


# def getChapterList(bookid,chapterStartNumber,chapterEndNumber):
#     client = MongoClient("mongodb://127.0.0.1:27017")
#     # 连接数据库
#     db = client.dingdian
#
#    # // bookid = request.GET.get('bookid', "")
#    #  chapterid = request.GET.get('chapterid', "")
#
#     # 获取booklist集合
#     chapterlist = db[bookid]
#
#     searchRes = chapterlist.find({"order_number" : { "$gte" : chapterStartNumber
# , "$lte" : chapterEndNumber}})
#
#     # pageIndex = 0
#     rets = []
#     for item in searchRes:
#         rets.append(item)
#         print(item)
#     client.close()
#
# getChapterList("仙武召唤系统_我真是老王啊",1,20)


# import urllib.parse
# def percentEncode(str):
#     res = urllib.parse.quote(str, '')
#     res = res.replace('+', '%20')
#     res = res.replace('*', '%2A')
#     res = res.replace('%7E', '~')
#     return res
#
# print(percentEncode("http://127.0.0.1:8000/api/bookid/仙武召唤系统_我真是老王啊/chapterStartNumber/1/chapterEndNumber/20"))



# def getCategoryBookList(categoryName,pageIndex,pageSize):
#     client = MongoClient("mongodb://127.0.0.1:27017")
#     # 连接数据库
#     db = client.dingdian
#     # 获取booklist集合
#     novel_list = db["book_list"]
#
#
#     searchdic = {"novel_family":categoryName}
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
#     retdict = {"categoryName":"网游竞技","nobelList":rets}
#
#     j = json.dumps(retdict)
#     print(j)
#     # return JsonResponse({"result": 0, "novellist": rets})
#     decode_json = json.loads(j)
#     print(decode_json)
# getCategoryBookList("网游竞技",1,20)

# md5=hashlib.md5('网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技'.encode('utf-8')).hexdigest()
# print(md5)

# client = MongoClient("mongodb://127.0.0.1:27017")
#     # 连接数据库
# db = client.dingdian
#
# tttt= db["123123"]
# tttt.find({})



# def getCategoryBookList(categoryName,pageIndex,pageSize):
#     client = MongoClient("mongodb://127.0.0.1:27017")
#     # 连接数据库
#     db = client.dingdian
#
#     # 获取booklist集合
#     novel_list = db["book_list"]
#     categoryList = db["novel_category"]
#
#     retCategory = categoryList.find()
#     retAllNovelCategory = []
#     for itemCategory in retCategory:
#         categoryName = itemCategory['category']
#         searchdic = {"novel_family": categoryName}
#         # pageIndex = 0
#         index = int(pageIndex) * pageSize
#         searchRes = novel_list.find(searchdic).skip(index).limit(pageSize)
#         # pageIndex = 0
#         rets = []
#         for item in searchRes:
#             rets.append(item)
#             print(item)
#         print(retCategory)
#
#         retAllNovelCategory.append({"categoryName":categoryName,"nobelList":rets})
#
#     client.close()
#
#     print(retAllNovelCategory)
# getCategoryBookList("网游竞技",0,10)

# def getChapterById(bookid):
#     client = MongoClient("mongodb://127.0.0.1:27017")
#     # 连接数据库
#     db = client.dingdian
#
#     # bookid = request.GET.get('bookid', "")
#     # chapterid = request.GET.get('chapterid', "")
#
#     # 获取booklist集合
#     novel_list = db["book_list"]
#
#     searchRes = novel_list.find_one({"_id":bookid})
#     client.close()
#     print(searchRes)
#
# getChapterById("00b791de-9638-11e8-b4c4-68f728a3bccf")


def getChapterInfo(bookid,chapterid):
    client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
    db = client.dingdian

    # booklist = db["book_list"];
    #
    chapterlist = db[bookid]

    retRes = chapterlist.find_one({"_id": chapterid})

    retRes["content"] = retRes["content"].replace("\r\n", "<br/>").replace("\0x", "&nbsp");

    print(retRes)

    client.close()

getChapterInfo("6572e96e-9c71-11e8-9b63-6003088a50b6","668cc248-9c71-11e8-b1bf-6003088a50b6")