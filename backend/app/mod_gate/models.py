import datetime
from app import db


class Gate(db.DynamicDocument):
    name = db.StringField(default="")  # 闸机名
    number = db.StringField(default="", unique=True)  # 闸机编号
    category = db.StringField(default="")  # 闸机分类
    mc_id = db.StringField(default="", unique=True)  # 闸机 mc id
    hand_max = db.IntField(null=True, default=None)  # 手上限值
    hand_min = db.IntField(null=True, default=None)  # 手下限值
    foot_max = db.IntField(null=True, default=None)  # 脚上限值
    foot_min = db.IntField(null=True, default=None)  # 脚下限值
    is_on = db.BooleanField(default=True)  # 闸机开关状态
    is_online = db.BooleanField(default=True)  # 闸机在线状态
    ip = db.StringField(default="")  # IP地址
    port = db.IntField(null=True, default=None)  # 端口
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)

    hand_near_max = db.IntField(null=True, default=None)  # 手近失效上限值
    hand_near_min = db.IntField(null=True, default=None)  # 手近失效下限值
    foot_near_max = db.IntField(null=True, default=None)  # 脚近失效上限值
    foot_near_min = db.IntField(null=True, default=None)  # 脚近失效下限值

    def __str__(self):
        return self.to_json()


class Card(db.DynamicDocument):
    card_number = db.StringField(default="", unique=True)  # 卡号号码
    card_category = db.StringField(  # 卡片类别
        default="3",
        choices=(("0", "vip"), ("1", "只测手"), ("2", "只测脚"), ("3", "手脚都测")),
    )
    name = db.StringField(default="")  # 姓名
    job_number = db.StringField(default="", unique=True)  # 工号
    department = db.StringField(default="department")  # 部门
    gender = db.StringField(default="1", choices=(("0", "女"), ("1", "男")))  # 性别
    note = db.StringField(default="default")  # 其他说明
    belong_to_mc = db.StringField(default="all")
    # 进出标志 name1:1|name2:0|name3 0:可进可出, 1:禁止进入/可出, 2:禁止出去/可进,
    # 3:禁止进出  or all:所有闸机都可进可出
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)
    card_counter = db.SequenceField(
        collection_name="card_counter", unique=True
    )  # 卡号编号
    class_time = db.StringField(default="")  # 班别
    classes = db.ListField(default=[])  # 多班别
    hid_card_number = db.StringField(default="")  # HID 号码
    meta = {
        "indexes": [
            "card_number",
            "job_number",
            "card_counter",
            "hid_card_number",
            "department",
        ]
    }

    def __str__(self):
        return self.to_json()


class CardTest(db.DynamicDocument):
    log_id = db.StringField(default="")  # 记录流水号
    card_counter = db.StringField(default="")  # 卡片编号(内部, 1, 2, 3)
    card_number = db.StringField(default="")  # 卡片号码
    card_category = db.StringField(default="")  # 卡片类型(vip, 手脚都测...)
    in_out_symbol = db.StringField(default="")  # 进出标志: 闸机上是进还是出, 0表出, 1表进
    mc_id = db.StringField(default="")  # 闸机 mc id
    test_datetime = db.DateTimeField()  # 测试时间
    test_result = db.StringField(default="")  # 是否通过 1:通过 0:不通过
    is_tested = db.StringField(default="")  # 是否测试 1:测试 0:不测试
    hand = db.StringField(default="")  # 手腕检测值
    left_foot = db.StringField(default="")  # 左脚检测值
    right_foot = db.StringField(default="")  # 右脚检测值
    after_erg = db.StringField(default="")  # ERG后的值
    rsg = db.StringField(default="")  # RSG值
    created_time = db.DateTimeField(default=datetime.datetime.utcnow)
    is_copied_to_other_database = db.BooleanField(default=False)
    meta = {"indexes": ["card_number", "card_counter", "test_datetime"]}


class CardClassTime(db.DynamicDocument):
    name = db.StringField(default="", unique=True)
    working_time_from = db.StringField()
    working_time_to = db.StringField()

    def __str__(self):
        return self.to_json()
