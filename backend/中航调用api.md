### 中航调用api 接口文档


####1： 获取所有员工的信息
    
    url: /api/cards/all
    请求方式：GET
    返回数据：以json 格式返回所有员工的信息
    返回示例：
    
    [ {
    _id: "5d83200e417f5ce52693276e",
    "card_number": "0008B2D7",
    "card_category": "0",
    name: "CEWC",
    "job_number": "12312",
    department: "D",
    gender: "1",
    note: "default",
    "belong_to_mc": "",
    "created_time": ISODate("2019-09-19T06:28:30.542Z"),
    "card_counter": NumberInt("1"),
    "class_time": "",
    classes: [
        "1"
    ],
    "hid_card_number": ""
    } ]        
    以 [员工信息，员工信息]的格式返回 json 格式
    
####2： 新增或更新 员工
    url: /api/cards/update
    请求方式：POST
    请求数据：以json 格式提交用户信息
    请求数据示例：
    {
     "EMPNO":"LS091",
     "EMPNAME":"临时091",
     "CARDFIXNO":"LS091",
     "DPTNAME1":"供应商 中航电子",
     "DPTNAME2":"供应商 中航电子",
     "DPTNAME3":"供应商 中航电子",
     "DPTNAME4":"供应商 中航电子",
     "EMPCARDTID":"31",
     "UPD_DATE": "2019/9/29 9:02:49"
    }
    
    返回数据：
    格式： json
    执行成功：{"statu":1, "erro":""}
    执行失败：{"statu":0, "erro":"报错信息"}
    
    
    
####3： 删除员工
    url: /api/cards/delete/[用户  _id]
    请求方式：DELETE
    请求示例：/api/cards/delete/5d83200e417f5ce52693276e
    
    返回数据：
    格式： json
    执行成功：{"statu":1, "erro":""}
    执行失败：{"statu":0, "erro":"报错信息"}