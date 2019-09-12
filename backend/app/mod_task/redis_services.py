import redis, os
import config
from pymongo import MongoClient, UpdateOne, bulk

class Redis:
    def __init__(self, REDIS_HOST, REDIS_PORT):
        self.log_every = 'log_every'
        self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

    def set(self, k, v, time=False):
        if time:
            self.redis.set(k, v, time)
        else:
            self.redis.set(k, v)
        return True

    def set_log_every(self, k):
        self.set(self.log_every, k)

    def get_dev_status(self):
        """获取所有闸机的状态，  原理是 挨个去查设备的redis 是否存在"""

        myclient = MongoClient(config.MONGODB_HOST, config.MONGODB_PORT)
        mydb = myclient[config.MONGODB_DB]
        mycol = mydb.gate
        
        data = []
        for x in mycol.find():
            dev = x['mc_id']
            if self.get(dev):
                data.append(dev)
        
        return data



    def save_log_status(self, key_id):
        log_every = self.get(self.log_every)
        if not log_every:
            log_every = 1
        self.set('dev'+str(key_id), log_every)

    def get(self, k):
        return self.redis.get(k)


Redis = Redis(config.REDIS_URL, 6379)