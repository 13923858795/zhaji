import datetime
import pathlib
import csv
from pymongo import MongoClient

# TODO: change to aggregate
#  logs.aggregate([{'$lookup': {'from': 'card', 'localField': 'card_number', 'foreignField': 'card_number', 'as': 'cards'}}])


def card_log_calculate(
    MONGODB_HOST,
    MONGODB_PORT,
    MONGODB_DB,
    hours_start,
    hours_end,
    card_class_time,
):
    """根据班别, 统计删选卡片和测试数据

    Arguments:
        MONGODB_HOST {[type]} -- [description]
        MONGODB_PORT {[type]} -- [description]
        MONGODB_DB {[type]} -- [description]
        hours_start {[type]} -- [description]
        hours_end {[type]} -- [description]
        card_class_time {str} -- 班别名称

    Returns:
        dict -- dict of list
    """

    # pymongo
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    db = client[MONGODB_DB]
    cards = db.card
    cardtests = db.card_test
    gate_collection = db.gate
    system_config = db.system_config

    # 初始化 excel dict
    wb = {}

    # 当前时区 和 时间
    config = system_config.find()[0]
    system_config_timezone = int(config["timezone"])
    local_tz = datetime.timezone(
        datetime.timedelta(hours=system_config_timezone)
    )

    # 设定 筛选时间段
    # a 如果上班时间 < 下班时间, 说明是白班
    work_hours_start = datetime.datetime.now().replace(
        hour=int(hours_start.split(":")[0]),
        minute=int(hours_start.split(":")[1]),
        second=0,
        microsecond=0,
        tzinfo=local_tz,
    )

    work_hours_end = work_hours_start.replace(
        hour=int(hours_end.split(":")[0]), minute=int(hours_end.split(":")[1])
    )

    # b 如果上班时间 > 下班时间, 说明是通宵班
    if hours_start.split(":")[0] > hours_end.split(":")[0]:
        work_hours_end = (
            work_hours_start + datetime.timedelta(days=1)
        ).replace(
            hour=int(hours_end.split(":")[0]),
            minute=int(hours_end.split(":")[1]),
        )

    # 当发送邮件时间 < 筛选时间段结尾, 筛选时间段往前移一天
    # if now < work_hours_end:
    #     work_hours_start = work_hours_start - datetime.timedelta(days=1)
    #     work_hours_end = work_hours_end - datetime.timedelta(days=1)

    # 筛选属于班别的卡片:
    card_classes_numbers = []
    # 如果传入了 班别名称 card_class_time
    if card_class_time:
        card_classes_numbers = [
            c
            for c in cards.find({"classes": card_class_time}).distinct(
                "card_number"
            )
        ]

    # 1. 该测试而未测试
    # 时间段中所有已测试卡片号码
    tested_card_number_list = cardtests.find(
        {"test_datetime": {"$gte": work_hours_start, "$lte": work_hours_end}}
    ).distinct("card_number")

    all_cards_should_test_but_not_tested = []
    # 如果传入了 班别名称
    if card_class_time:
        all_cards_should_test_but_not_tested = cards.find(
            {
                "card_number": {"$nin": tested_card_number_list},
                "classes": card_class_time,
            }
        )
    else:
        all_cards_should_test_but_not_tested = cards.find(
            {"card_number": {"$nin": tested_card_number_list}}
        )

    ws_should_test_but_not_tested = []

    ws_should_test_but_not_tested.append(
        ["卡号号码", "卡片类别", "姓名", "工号", "部门", "性别", "其他说明", "权限", "卡号编号"]
    )

    for card in all_cards_should_test_but_not_tested:
        card_category = ""
        if card.get("card_category", "") == "0":
            card_category = "VIP"
        elif card.get("card_category", "") == "1":
            card_category = "只测手"
        elif card.get("card_category", "") == "2":
            card_category = "只测脚"
        elif card.get("card_category", "") == "3":
            card_category = "手脚都测"
        gender = ""
        if card.get("gender", "") == "0":
            gender = "女"
        elif card.get("gender", "") == "1":
            gender = "男"
        ws_should_test_but_not_tested.append(
            [
                card.get("card_number", ""),
                card_category,
                card.get("name", ""),
                card.get("job_number", ""),
                card.get("department", ""),
                gender,
                card.get("note", ""),
                card.get("belong_to_mc", ""),
                card.get("card_counter", ""),
            ]
        )

    # 2. 已测试而未通过的 logs
    all_logs_tested_but_not_passed = []
    # 如果传入了班别名称:
    if card_class_time:
        all_logs_tested_but_not_passed = cardtests.find(
            {
                "test_result": "0",
                "test_datetime": {
                    "$gte": work_hours_start,
                    "$lte": work_hours_end,
                },
                "card_number": {"$in": card_classes_numbers},
            }
        )
    else:
        all_logs_tested_but_not_passed = cardtests.find(
            {
                "test_result": "0",
                "test_datetime": {
                    "$gte": work_hours_start,
                    "$lte": work_hours_end,
                },
            }
        )

    ws_tested_but_not_passed = []
    ws_tested_but_not_passed.append(
        [
            "记录流水号",
            "卡片编号",
            "卡片号码",
            "卡片类型",
            "进出标志",
            "闸机 mc id",
            "测试时间",
            "是否通过",
            "是否测试",
            "手腕检测值",
            "左脚检测值",
            "右脚检测值",
            "ERG后的值",
            "RSG值",
            "姓名",
            "工号",
            "部门"
        ]
    )

    for log in all_logs_tested_but_not_passed:
        card_category = ""
        if log.get("card_category", "") == "0":
            card_category = "VIP"
        elif log.get("card_category", "") == "1":
            card_category = "只测手"
        elif log.get("card_category", "") == "2":
            card_category = "只测脚"
        elif log.get("card_category", "") == "3":
            card_category = "手脚都测"
        else:
            card_category = card_category
        test_result = ""
        if log.get("test_result", "") == "0":
            test_result = "不通过"
        elif log.get("test_result", "") == "1":
            test_result = "通过"
        is_tested = ""
        if log.get("is_tested", "") == "0":
            is_tested = "不测试"
        elif log.get("is_tested", "") == "1":
            is_tested = "测试"
        name = ""
        job_number = ""
        department = ""
        try:
            card = cards.find_one({"card_number": log["card_number"]})
            name = card["name"]
            job_number = card["job_number"]
            department = card["department"]

        except:
            pass

        ws_tested_but_not_passed.append(
            [
                log.get("log_id", ""),
                log.get("card_counter", ""),
                log.get("card_number", ""),
                card_category,
                log.get("in_out_symbol", ""),
                log.get("mc_id", ""),
                log.get("test_datetime", "")
                .replace(tzinfo=datetime.timezone.utc)
                .astimezone(local_tz)
                .strftime("%Y-%m-%d %H:%M:%S"),
                test_result,
                is_tested,
                log.get("hand", ""),
                log.get("left_foot", ""),
                log.get("right_foot", ""),
                log.get("after_erg", ""),
                log.get("rsg", ""),
                name,
                job_number,
                department,
            ]
        )

    # 3. 测试已通过的 logs
    # 如果传入了班别名称:
    all_logs_tested_and_passed = []
    if card_class_time:
        all_logs_tested_and_passed = cardtests.find(
            {
                "test_result": "1",
                "test_datetime": {
                    "$gte": work_hours_start,
                    "$lte": work_hours_end,
                },
                "card_number": {"$in": card_classes_numbers},
            }
        )
    else:
        all_logs_tested_and_passed = cardtests.find(
            {
                "test_result": "1",
                "test_datetime": {
                    "$gte": work_hours_start,
                    "$lte": work_hours_end,
                },
            }
        )

    ws_tested_and_passed = []
    ws_tested_and_passed.append(
        [
            "记录流水号",
            "卡片编号",
            "卡片号码",
            "卡片类型",
            "进出标志",
            "闸机 mc id",
            "测试时间",
            "是否通过",
            "是否测试",
            "手腕检测值",
            "左脚检测值",
            "右脚检测值",
            "ERG后的值",
            "RSG值",
            "姓名",
            "工号",
            "部门",
        ]
    )

    for log in all_logs_tested_and_passed:
        card_category = ""
        if log.get("card_category", "") == "0":
            card_category = "VIP"
        elif log.get("card_category", "") == "1":
            card_category = "只测手"
        elif log.get("card_category", "") == "2":
            card_category = "只测脚"
        elif log.get("card_category", "") == "3":
            card_category = "手脚都测"
        else:
            card_category = card_category
        test_result = ""
        if log.get("test_result", "") == "0":
            test_result = "不通过"
        elif log.get("test_result", "") == "1":
            test_result = "通过"
        is_tested = ""
        if log.get("is_tested", "") == "0":
            is_tested = "不测试"
        elif log.get("is_tested", "") == "1":
            is_tested = "测试"

        name = ""
        job_number = ""
        department = ""
        try:
            card = cards.find_one({"card_number": log["card_number"]})
            name = card["name"]
            job_number = card["job_number"]
            department = card["department"]

        except:
            pass
        ws_tested_and_passed.append(
            [
                log.get("log_id", ""),
                log.get("card_counter", ""),
                log.get("card_number", ""),
                card_category,
                log.get("in_out_symbol", ""),
                log.get("mc_id", ""),
                log.get("test_datetime", "")
                .replace(tzinfo=datetime.timezone.utc)
                .astimezone(local_tz)
                .strftime("%Y-%m-%d %H:%M:%S"),
                test_result,
                is_tested,
                log.get("hand", ""),
                log.get("left_foot", ""),
                log.get("right_foot", ""),
                log.get("after_erg", ""),
                log.get("rsg", ""),
                name,
                job_number,
                department,
            ]
        )

    # 4. 近失效记录
    near_failure_logs = []
    all_gates = [x for x in gate_collection.find()]

    # 如果传入了班别名称:
    if card_class_time:
        for log in cardtests.find(
            {
                "test_datetime": {
                    "$gte": work_hours_start,
                    "$lte": work_hours_end,
                },
                "card_number": {"$in": card_classes_numbers},
            }
        ):
            gates = [g for g in all_gates if g["mc_id"] == log["mc_id"]]
            if gates:
                gate = gates[0]
                # 按照卡片的类型, 进行一一判断
                # vip卡:
                if log["card_category"] == "0":
                    pass

                # 只测手
                elif log["card_category"] == "1" and log["hand"] not in (
                    "NO",
                    "OVR",
                    "UND",
                    "UNR"
                ):
                    if (
                        gate["hand_max"]
                        < int(log["hand"])
                        < gate["hand_near_max"]
                        or gate["hand_near_min"]
                        < int(log["hand"])
                        < gate["hand_min"]
                    ):
                        near_failure_logs.append(log)

                # 只测脚
                elif (
                    log["card_category"] == "2"
                    and log["left_foot"] not in ("NO", "OVR", "UND", "UNR")
                    and log["right_foot"] not in ("NO", "OVR", "UND", "UNR")
                ):
                    if (
                        gate["foot_near_min"]
                        < int(log["left_foot"])
                        < gate["foot_min"]
                        or gate["foot_max"]
                        < int(log["left_foot"])
                        < gate["foot_near_max"]
                        or gate["foot_near_min"]
                        < int(log["right_foot"])
                        < gate["foot_min"]
                        or gate["foot_max"]
                        < int(log["right_foot"])
                        < gate["foot_near_max"]
                    ):
                        near_failure_logs.append(log)

                # 普通卡
                elif (
                    log["card_category"] == "3"
                    and log["hand"] not in ("NO", "OVR", "UND", "UNR")
                    and log["left_foot"] not in ("NO", "OVR", "UND", "UNR")
                    and log["right_foot"] not in ("NO", "OVR", "UND", "UNR")
                ):
                    if (
                        gate["hand_max"]
                        < int(log["hand"])
                        < gate["hand_near_max"]
                        or gate["hand_near_min"]
                        < int(log["hand"])
                        < gate["hand_min"]
                        or gate["foot_near_min"]
                        < int(log["left_foot"])
                        < gate["foot_min"]
                        or gate["foot_max"]
                        < int(log["left_foot"])
                        < gate["foot_near_max"]
                        or gate["foot_near_min"]
                        < int(log["right_foot"])
                        < gate["foot_min"]
                        or gate["foot_max"]
                        < int(log["right_foot"])
                        < gate["foot_near_max"]
                    ):
                        near_failure_logs.append(log)
    else:  # 没有传入了班别名称:
        for log in cardtests.find(
            {
                "test_datetime": {
                    "$gte": work_hours_start,
                    "$lte": work_hours_end,
                }
            }
        ):
            gates = [g for g in all_gates if g["mc_id"] == log["mc_id"]]
            if gates:
                gate = gates[0]
                # 按照卡片的类型, 进行一一判断
                # vip卡:
                if log["card_category"] == "0":
                    pass

                # 只测手
                elif log["card_category"] == "1" and log["hand"] not in (
                    "NO",
                    "OVR",
                    "UND",
                    "UNR",
                ):
                    if (
                        gate["hand_max"]
                        < int(log["hand"])
                        < gate["hand_near_max"]
                        or gate["hand_near_min"]
                        < int(log["hand"])
                        < gate["hand_min"]
                    ):
                        near_failure_logs.append(log)

                # 只测脚
                elif (
                    log["card_category"] == "2"
                    and log["left_foot"] not in ("NO", "OVR", "UND", "UNR")
                    and log["right_foot"] not in ("NO", "OVR", "UND", "UNR")
                ):
                    if (
                        gate["foot_near_min"]
                        < int(log["left_foot"])
                        < gate["foot_min"]
                        or gate["foot_max"]
                        < int(log["left_foot"])
                        < gate["foot_near_max"]
                        or gate["foot_near_min"]
                        < int(log["right_foot"])
                        < gate["foot_min"]
                        or gate["foot_max"]
                        < int(log["right_foot"])
                        < gate["foot_near_max"]
                    ):
                        near_failure_logs.append(log)

                # 普通卡
                elif (
                    log["card_category"] == "3"
                    and log["hand"] not in ("NO", "OVR", "UND", "UNR")
                    and log["left_foot"] not in ("NO", "OVR", "UND", "UNR")
                    and log["right_foot"] not in ("NO", "OVR", "UND", "UNR")
                ):
                    if (
                        gate["hand_max"]
                        < int(log["hand"])
                        < gate["hand_near_max"]
                        or gate["hand_near_min"]
                        < int(log["hand"])
                        < gate["hand_min"]
                        or gate["foot_near_min"]
                        < int(log["left_foot"])
                        < gate["foot_min"]
                        or gate["foot_max"]
                        < int(log["left_foot"])
                        < gate["foot_near_max"]
                        or gate["foot_near_min"]
                        < int(log["right_foot"])
                        < gate["foot_min"]
                        or gate["foot_max"]
                        < int(log["right_foot"])
                        < gate["foot_near_max"]
                    ):
                        near_failure_logs.append(log)

    ws_near_tests = []

    ws_near_tests.append(
        [
            "记录流水号",
            "卡片编号",
            "卡片号码",
            "卡片类型",
            "进出标志",
            "闸机 mc id",
            "测试时间",
            "是否通过",
            "是否测试",
            "手腕检测值",
            "左脚检测值",
            "右脚检测值",
            "ERG后的值",
            "RSG值",
            "姓名",
            "工号",
            "部门"
        ]
    )

    for log in near_failure_logs:
        card_category = ""
        if log.get("card_category", "") == "0":
            card_category = "VIP"
        elif log.get("card_category", "") == "1":
            card_category = "只测手"
        elif log.get("card_category", "") == "2":
            card_category = "只测脚"
        elif log.get("card_category", "") == "3":
            card_category = "手脚都测"
        else:
            card_category = card_category
        test_result = ""
        if log.get("test_result", "") == "0":
            test_result = "不通过"
        elif log.get("test_result", "") == "1":
            test_result = "通过"
        is_tested = ""
        if log.get("is_tested", "") == "0":
            is_tested = "不测试"
        elif log.get("is_tested", "") == "1":
            is_tested = "测试"

        name = ""
        job_number = ""
        department = ""
        try:
            card = cards.find_one({"card_number": log["card_number"]})
            name = card["name"]
            job_number = card["job_number"]
            department = card["department"]

        except:
            pass

        ws_near_tests.append(
            [
                log.get("log_id", ""),
                log.get("card_counter", ""),
                log.get("card_number", ""),
                card_category,
                log.get("in_out_symbol", ""),
                log.get("mc_id", ""),
                log.get("test_datetime", "")
                .replace(tzinfo=datetime.timezone.utc)
                .astimezone(local_tz)
                .strftime("%Y-%m-%d %H:%M:%S"),
                test_result,
                is_tested,
                log.get("hand", ""),
                log.get("left_foot", ""),
                log.get("right_foot", ""),
                log.get("after_erg", ""),
                log.get("rsg", ""),
                name,
                job_number,
                department,
            ]
        )

    wb["该测试而未测试"] = ws_should_test_but_not_tested
    wb["已测试而未通过"] = ws_tested_but_not_passed
    wb["测试已通过"] = ws_tested_and_passed
    wb["近失效"] = ws_near_tests

    # pprint(wb)

    return wb


def normalize_card_number(card_number):
    """如果 card_number 大于8位, 则将10进制的卡号, 转化为16进制, 并取其后六位, 最后用0补
    全为8位大写16进制. 否则将其转换为8位大写16进制

    Arguments:
        card_number {int|string} -- 卡号

    Returns:
        str -- 处理后的卡号
    """
    card_number = str(card_number).strip()

    if len(card_number) > 8:
        card_number = hex(int(card_number))[-6:]

    return card_number.upper().rjust(8, "0")


def hid_to_normal(hid_card_number):
    """首先两位00
    hid卡号前三位转16进制 得到的数取后两位，不足两位补0
    后5位转16进制，取后四位 不足四位补0
    
    Arguments:
        hid_card_number {int|str} -- HID 卡号
    """

    hid_card_number = str(hid_card_number)
    part_1 = "{:0>2X}".format(int(hid_card_number[0:3]))
    part_2 = "{:0>4}".format("{:X}".format(int(hid_card_number[-5:]))[-4:])
    final_number = "00{}{}".format(part_1, part_2)

    return final_number


def import_data_to_mongodb(file_path, database_name, collection_name):
    """将 csv 文件 插入到 mongodb 中
    
    Arguments:
        file_path {str} -- 文件路径
        database_name {str} -- 数据库名
        collection_name {str} -- collection 名
    
    Returns:
        insert_many_results -- insert_many_results
    """
    data = []
    csv_f = pathlib.Path(file_path)
    with csv_f.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            del row["_id"]

            if "test_datetime" in row:
                row["test_datetime"] = datetime.datetime.strptime(
                    row["test_datetime"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(
                    tzinfo=datetime.timezone.utc
                )  # 2019-01-21T06:56:37.000Z

            data.append(row)

    mongo_client = MongoClient()
    database = mongo_client[database_name]
    insert_many_results = database[collection_name].insert_many(data)

    return insert_many_results


def import_data_to_mongodb_one_by_one(file_path, database_name, collection_name):
    """将 csv 文件 插入到 mongodb 中
    
    Arguments:
        file_path {str} -- 文件路径
        database_name {str} -- 数据库名
        collection_name {str} -- collection 名
    
    Returns:
        insert_many_results -- insert_many_results
    """
    mongo_client = MongoClient()
    database = mongo_client[database_name]
    csv_f = pathlib.Path(file_path)
    with csv_f.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            del row["_id"]

            if "test_datetime" in row:
                row["test_datetime"] = datetime.datetime.strptime(
                    row["test_datetime"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(
                    tzinfo=datetime.timezone.utc
                )  # 2019-01-21T06:56:37.000Z

            database[collection_name].insert_one(row)


def filter_in_out_cardtest_data(cardtest_list):
    """从 cardtest_list 中, 筛选出匹配的进出记录, 0表出, 1表进

    Arguments:
        cardtest_list {list} -- 相同卡号的进出记录数据
    
    Returns:
        list -- 匹配好后的进出记录
    """
    # len 为 0, 说明没有匹配,
    # len 为 1, 说明只有一条数据
    # len 为 2+
    results_mid = []
    results_final = []
    a = None

    # cardtest_list 中只有一条数据
    if len(cardtest_list) == 1:
        pass

    else:
        for i, b in enumerate(cardtest_list):
            if (
                a is None
                and b["in_out_symbol"] == "1"
                and len(results_mid) == 0
            ):
                results_mid.append(b)
            elif (
                a is not None
                and a["in_out_symbol"] == "0"
                and b["in_out_symbol"] == "1"
                and len(results_mid) == 0
            ):
                results_mid.append(b)
            elif (
                a is not None
                and a["in_out_symbol"] == "0"
                and b["in_out_symbol"] == "1"
                and len(results_mid) != 0
            ):
                results_mid.append(a)
                results_mid.append(b)
            elif i == len(cardtest_list) - 1 and b["in_out_symbol"] == "0":
                results_mid.append(b)

            a = b

    if len(results_mid) > 1:
        if len(results_mid) % 2 == 1:
            del results_mid[-1]
        for i in range(0, len(results_mid) - 1, 2):
            results_mid[i]["out_test_datetime"] = results_mid[i + 1]["test_datetime"]
            results_mid[i]["out_mc_id"] = results_mid[i + 1]["mc_id"]
            results_final.append(results_mid[i])

    return results_final
