import hashlib
import os
import sqlite3


conn = sqlite3.connect('db/babydietfood2.db')
root = "repice3"
c = conn.cursor()


sql = "select * from food_table where type = '营养进补' and prompt is not NULL"

# 执行语句
results = c.execute(sql)

# 遍历打印输出
allrepices = results.fetchall()
conn.commit()
for repice in allrepices:
    repiceName = repice[1]
    repicefile = "./repice3/"+repiceName+".png"
    if os.path.exists(repicefile):

        print(repice[1])
        md5_name = hashlib.md5(repiceName.encode("utf8")).hexdigest() + '.png'
        update_sql = "update childrenfood set picture = '{}' where name = '{}'".format(md5_name, repiceName)
        c.execute(update_sql)
        conn.commit()
        os.rename(repicefile, 'repice5/' + md5_name)



# for dirpath, dirnames, filenames in os.walk(root):
#     for filepath in filenames:
#         print("fileName="+filepath)
#         md5_name = hashlib.md5(os.path.splitext(filepath)[0].encode("utf8")).hexdigest()+'.png'
#         print("md5Name = "+md5_name)
#         # 'my name is {1} ,age {0}'.format(10, 'hoho')
#
#         update_sql = "update childrenfood set picture = '{}' where picture = '{}'".format(md5_name, filepath)
#         c.execute(update_sql)
#         conn.commit()
#
#         os.rename('./repice3/' + filepath, 'repice5/' + md5_name)
#
# conn.close()
# print("finish=====>")