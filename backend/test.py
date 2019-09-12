import config
from pymongo import MongoClient, UpdateOne, bulk

myclient = MongoClient('10.1.6.211', config.MONGODB_PORT)
mydb = myclient[config.MONGODB_DB]
mycol = mydb.gate

for x in mycol.find():
    print(x['mc_id'])



