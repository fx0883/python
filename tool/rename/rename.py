import hashlib
import os
import sqlite3


conn = sqlite3.connect('db/babyDietFood.DB')
root = "repice2"
c = conn.cursor()
for dirpath, dirnames, filenames in os.walk(root):
    for filepath in filenames:
        print("fileName="+filepath)
        md5_name = hashlib.md5(os.path.splitext(filepath)[0].encode("utf8")).hexdigest()+'.png'
        print("md5Name = "+md5_name)
        # 'my name is {1} ,age {0}'.format(10, 'hoho')

        update_sql = "update childrenfood set picture = '{}' where picture = '{}'".format(md5_name, filepath)
        c.execute(update_sql)
        conn.commit()

        os.rename('./repice2/' + filepath, 'repice2/' + md5_name)

conn.close()
print("finish=====>")