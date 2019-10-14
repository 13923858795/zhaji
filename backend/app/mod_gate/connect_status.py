import os, time
from pymongo import MongoClient

MONGODB_DB = os.environ.get("MONGODB_DB", "quatek_web_app")
MONGODB_HOST = os.environ.get("MONGODB_HOST", "127.0.0.1")
MONGODB_PORT = os.environ.get("MONGODB_PORT", 27017)
client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DB]


def connect_status():

    # db_every = [i for i in db.log_every.find()]
    # if db_every:
    #     log_every = db_every[0]['value']
    # else:
    #     log_every = 60*2

    log_every = 0.5 * 3600

    """ 获取所有的 设备通讯时间戳 """
    log_data = {}
    for i in db.logs.find():
        log_data[int(i["mc_client_id"])] = i["connect_time"]

    """获取所有的 设备id"""
    resp = []
    for i in db.gate.find():
        dev_id = int(i['mc_id'])
        log_time = log_data.get(dev_id, False)
        if log_time and time.time() - log_time < log_every:
            resp.append(dev_id)

    print(resp)
    return resp
