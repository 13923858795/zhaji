import json, requests


# # data = '[{"_id": {"$oid": "5d9d4464182282e2aa486e8c"}, "card_number": "00053C47", "card_category": "2", "name": "\u6d4b\u8bd59", "job_number": "test09", "department": "IC", "gender": "1", "note": "default", "belong_to_mc": "all", "created_time": {"$date": 1570587748944}, "card_counter": 9, "class_time": "", "classes": ["\u665a\u73ed"], "hid_card_number": ""}, {"_id": {"$oid": "5d9d4464182282e2aa486e8b"}, "card_number": "00FED6D7", "card_category": "0", "name": "\u6d4b\u8bd58", "job_number": "test08", "department": "IC", "gender": "1", "note": "default", "belong_to_mc": "all", "created_time": {"$date": 1570587748935}, "card_counter": 8, "class_time": "", "classes": ["\u665a\u73ed"], "hid_card_number": ""}, {"_id": {"$oid": "5d9d4464182282e2aa486e8a"}, "card_number": "0008F467", "card_category": "1", "name": "\u6d4b\u8bd57", "job_number": "test07", "department": "IC", "gender": "1", "note": "default", "belong_to_mc": "all", "created_time": {"$date": 1570587748921}, "card_counter": 7, "class_time": "", "classes": ["\u665a\u73ed"], "hid_card_number": ""}, {"_id": {"$oid": "5d9d4464182282e2aa486e89"}, "card_number": "0083BF6D", "card_category": "1", "name": "\u6d4b\u8bd56", "job_number": "test06", "department": "HID", "gender": "1", "note": "default", "belong_to_mc": "all", "created_time": {"$date": 1570587748906}, "card_counter": 6, "class_time": "", "classes": ["\u65e9\u73ed"], "hid_card_number": "13149005"}, {"_id": {"$oid": "5d9d4464182282e2aa486e88"}, "card_number": "0083BF6A", "card_category": "0", "name": "\u6d4b\u8bd55", "job_number": "test05", "department": "HID", "gender": "1", "note": "default", "belong_to_mc": "all", "created_time": {"$date": 1570587748879}, "card_counter": 5, "class_time": "", "classes": ["\u65e9\u73ed"], "hid_card_number": "13149002"}, {"_id": {"$oid": "5d9d4464182282e2aa486e87"}, "card_number": "0083BF69", "card_category": "3", "name": "\u6d4b\u8bd54", "job_number": "test04", "department": "HID", "gender": "1", "note": "default", "belong_to_mc": "all", "created_time": {"$date": 1570587748857}, "card_counter": 4, "class_time": "", "classes": ["\u65e9\u73ed"], "hid_card_number": "13149001"}, {"_id": {"$oid": "5d9d4464182282e2aa486e86"}, "card_number": "005BCD15", "card_category": "2", "name": "\u6d4b\u8bd53", "job_number": "test03", "department": "ID", "gender": "1", "note": "default", "belong_to_mc": "all", "created_time": {"$date": 1570587748845}, "card_counter": 3, "class_time": "", "classes": ["\u65e9\u73ed"], "hid_card_number": ""}, {"_id": {"$oid": "5d9d4464182282e2aa486e85"}, "card_number": "00D03897", "card_category": "0", "name": "\u6d4b\u8bd52", "job_number": "test02", "department": "ID", "gender": "1", "note": "default", "belong_to_mc": "all", "created_time": {"$date": 1570587748826}, "card_counter": 2, "class_time": "", "classes": ["\u65e9\u73ed"], "hid_card_number": ""}, {"_id": {"$oid": "5d9d4464182282e2aa486e84"}, "card_number": "007A9C25", "card_category": "3", "name": "\u6d4b\u8bd51", "job_number": "test01", "department": "ID", "gender": "1", "note": "default", "belong_to_mc": "all", "created_time": {"$date": 1570587748587}, "card_counter": 1, "class_time": "", "classes": ["\u65e9\u73ed"], "hid_card_number": ""}]'
# # data = json.loads(data)
# #
# # for i in data:
# #   print(i['_id']['$oid'])
#
# # a = {'id': '5d9da70aa94e4ac68b6d2ca6', 'card_number': '000LS092', 'card_category': '2', 'name': '临时092', 'job_number': 'LS092', 'department': 'aaaa供应商 中航电子', 'gender': '0', 'note': '31', 'belong_to_mc': 'all', 'classes': '1', 'hid_number': ''}
#
#
# data = {
#      "EMPNO":"53C49",
#      "EMPNAME":"临时093",
#      "CARDFIXNO":"53C49",
#      "DPTNAME1":"供应商 中航电子",
#      "DPTNAME2":"ccc供应商 中航电子",
#      "DPTNAME3":"供应商 中航电子",
#      "DPTNAME4":"供应商 中航电子",
#      "EMPCARDTID": "31",
#      "UPD_DATE": "2019/9/29 9:02:49"
#     }
#
# url = 'http://10.1.6.219:5001/api/cards/update'
# resp = requests.post(url, data)

url_delete = 'http://10.1.6.219:5001/api/cards/delete/5dad7b6cb07e491c806b62a2'
resp = requests.delete(url_delete)

r = resp.content
print(r)
# a = 0.5 * 3600
# #
# # print(a)