from django.test import TestCase

# Create your tests here.
from pymongo import MongoClient
import hashlib

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
#     # return JsonResponse({"result": 0, "novellist": rets})
#
# getCategoryBookList("网游竞技",1,20)

# md5=hashlib.md5('网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技网游竞技'.encode('utf-8')).hexdigest()
# print(md5)

client = MongoClient("mongodb://127.0.0.1:27017")
    # 连接数据库
db = client.dingdian

tttt= db["123123"]
tttt.find({})