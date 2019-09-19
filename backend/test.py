# import os
# from pymongo import MongoClient
#
#
# MONGODB_DB = os.environ.get("MONGODB_DB", "quatek_web_app")
# MONGODB_HOST = os.environ.get("MONGODB_HOST", "10.1.6.211")
# MONGODB_PORT = os.environ.get("MONGODB_PORT", 27017)
#
#
# class DBServices:
#     def __init__(self, col):
#         client = MongoClient(MONGODB_HOST, MONGODB_PORT)
#         self.col = client[MONGODB_DB][col]
#
#     def save(self, data):
#         self.col.insert_one(data)
#
#     def get_log(self, data):
#         myquery = data
#         return [i for i in self.col.find(myquery)]
#
#     def update(self, query, value):
#         self.col.update_one(query, value)
#
#
#
# db= DBServices('logs')
# #
# # a = db.get_log({"name": '2'})
# # print(a)
# # if a:
# #     print("cunzai")
#
#
#
# db.save({'id':1, 'time':12324343})
#



# q = { "name": "1" }
# v = { "$set": { 'name': "6" } }
#
# db.update(q, v)


import time



a = time.time()
print(a, type(a))
>>>>>>> 尝试插入到 mysql 数据库里
