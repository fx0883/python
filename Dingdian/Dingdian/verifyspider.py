from pymongo import MongoClient
import json
import datetime
def createFileJson():
    date=datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    path=date+'.json'
    return path

# 获取Mongodb链接
client = MongoClient("mongodb://127.0.0.1:27017")
#连接数据库
db =client.dingdian
#获取booklist集合
novel_list = db["book_list"]
rets = novel_list.find()

errornovellist = []
for item in rets:
    print(item)
    chapterCount = len(item['novel_section_urls'])
    chapterid = item['chapterlistId']
    chapter_list = db[chapterid]
    chapter_listCount = chapter_list.find().count()
    if chapterCount != chapter_listCount:
        errornovellist.append({"novel_name": item['novel_name'], "novel_url": item["novel_url"]})
client.close()


jsonfileName = createFileJson()
with open("verifyresult/"+jsonfileName, "wb") as f:
    f.write((json.dumps(errornovellist).encode('iso-8859-1').decode('unicode_escape').encode('utf-8')))  # 强制以utf-8转一下byte数据再以普通形式写入 。
    f.close()
  # json.dump({"list":errornovellist},f)
  # print("加载入文件完成...")


# with open('test.json','wb')
# data1 = {'name':'john',"age":12}
# data2 = {'name':'merry',"age":13}
# data = [data1,data2]
# print(data)
# json.dump(data,file,ensure_ascii=False)
# file.close()
# file = open('t
#
# with open("verifyresult/result.json", 'wb') as json_file:json.dump(errornovellist), json_file)

print("finish")