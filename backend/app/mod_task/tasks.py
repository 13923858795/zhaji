import eventlet

eventlet.monkey_patch()
import socket
import copy
import datetime
import io
import logging
import os
import re
import smtplib
import socketserver
import sys
import threading
import time
from email.message import EmailMessage
from logging import handlers
import pyexcel
from celery import Celery
from flask_socketio import SocketIO
from pymongo import MongoClient, UpdateOne, bulk
from sqlalchemy import create_engine, inspect, Table, MetaData
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from mongoengine import connect

from app.mod_gate.schema import Base, Log
from app.mod_gate.models import Card
from app.mod_gate.utils import card_log_calculate, normalize_card_number
from app.mod_system_config.models import SystemConfig


# load configs
MONGODB_DB = os.environ.get("MONGODB_DB", "quatek_web_app")
MONGODB_HOST = os.environ.get("MONGODB_HOST", "127.0.0.1")
MONGODB_PORT = os.environ.get("MONGODB_PORT", 27017)
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1")
SOCKET_HOST = os.environ.get("SOCKET_HOST", "0.0.0.0")
SOCKET_PORT = os.environ.get("SOCKET_PORT", 5858)



# logging
logger = logging.getLogger(
    os.path.splitext(os.path.split((os.path.abspath(__file__)))[1])[0]
)
logger.setLevel(logging.INFO)
logFormatter = logging.Formatter("%(asctime)s - %(message)s")
fileHandler = handlers.RotatingFileHandler(
    "{}{}".format(os.path.splitext(os.path.abspath(__file__))[0], ".log"),
    maxBytes=1024 * 1024 * 10,  # 10MB
    backupCount=10,
)
fileHandler.setFormatter(logFormatter)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
# logger.addHandler(consoleHandler)


# celery
app = Celery("quatek-task", broker=REDIS_URL, backend=REDIS_URL)
app.conf.update(
    {
        "CELERY_MONGODB_SCHEDULER_DB": MONGODB_DB,
        "CELERY_MONGODB_SCHEDULER_COLLECTION": "schedules",
        "CELERY_MONGODB_SCHEDULER_URL": f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}",
        "enable_utc": True,
    }
)


class UploadAllCardsHandler(socketserver.BaseRequestHandler):
    """ send: b'\rSET CARD;0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        recv: b'\rCARD 0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
    """

    def handle(self):
        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        cards = db.card
        gates = db.gate

        self.request.settimeout(5)
        mc_client = {}

        # get mc from database
        try:
            self.request.sendall(b"GET MCID\r\n")
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            mc_client_id = (
                data.replace("\r", "").replace("\n", "").split(" ")[1]
            )
            mc_client = gates.find({"mc_id": mc_client_id})[0]
            gates.update_one(
                {"mc_id": "mc_client.mc_id"},
                {
                    "$set": {
                        "ip": self.client_address[0],
                        "port": self.client_address[1],
                    }
                },
            )

            if "MCID" not in data:
                raise Exception("get mc error")
        except:
            logger.exception(f"error in UploadAllCardsHandler")

        logger.info(
            f'start UploadAllCardsHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
        )

        # set datetime for mc
        try:
            dt = datetime.datetime.utcnow()
            self.request.sendall(
                "SET DATE {}\r\n".format(dt.strftime("%Y-%m-%d")).encode()
            )
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            if "DATE" not in data:
                raise Exception("set date error")

            self.request.sendall(
                "SET TIME {}\r\n".format(dt.strftime("%H:%M:%S")).encode()
            )
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            if "TIME" not in data:
                raise Exception("set time error")

        except:
            logger.exception(
                f'error in UploadAllCardsHandler <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
            )

        # add cards to mc
        try:
            commands = []
            for card in cards.find():
                belong_to_mc = "all"
                if "belong_to_mc" in card:
                    belong_to_mc = card["belong_to_mc"]

                # add to all mc
                if belong_to_mc == "all" or not belong_to_mc:
                    # command = 'SET CARD {card_counter},{card_number},{job_number},{name},{department},{gender},{card_category},0,{note}\r\n'.format(
                    #     **card).encode()
                    for key in card.keys():
                        if not card[key]:
                            card[key] = "default"
                    commands.append(
                        f'SET CARD {card["card_counter"]},{card["card_number"]},{card["job_number"]},{card["name"]},{card["department"]},{card["gender"]},{card["card_category"]},0,{card["note"]}\r\n'
                    )

                # add to configed mc
                else:
                    # [{'mc1': '0'}, {'mc2': 1}]
                    belong_to_mc = [
                        {item.split(":")[0]: item.split(":")[1]}
                        for item in belong_to_mc.split("|")
                    ]

                    belong_to_mc_dict = {}  # {'mc1': '0', 'mc2': 1}

                    for item in belong_to_mc:
                        belong_to_mc_dict.update(item)

                    if mc_client["name"] in belong_to_mc_dict:

                        for key in card.keys():
                            if not card[key]:
                                card[key] = "default"

                        commands.append(
                            f'SET CARD {card["card_counter"]},{card["card_number"]},{card["job_number"]},{card["name"]},{card["department"]},{card["gender"]},{card["card_category"]},{belong_to_mc_dict[mc_client["name"]]},{card["note"]}\r\n'
                        )

            for command in commands:
                logger.info(command)
                self.request.sendall(command.encode())
                logger.info(self.request.recv(1000).decode())

            # commands = ''.join(commands).encode()
            # self.request.sendall(commands)
            # logger.info(f'send commands to <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>: {commands}')
            # logger.info(
            #     f'recv from <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>: {self.request.recv(100000)}')
        except:
            logger.exception(
                f'error in UploadAllCardsHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
            )

        time.sleep(self.server.p_data["server_last_time"])
        logger.info(
            f'stop UploadAllCardsHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
        )


class UpdateACardHandler(socketserver.BaseRequestHandler):
    """ send: b'\rSET CARD;0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        recv: b'\rCARD 0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        param: card
    """

    def handle(self):
        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        gates = db.gate
        self.request.settimeout(5)

        mc_client = {}
        card = self.server.p_data["card"]

        # get mc from database
        try:
            self.request.sendall(b"GET MCID\r\n")
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            mc_client_id = (
                data.replace("\r", "").replace("\n", "").split(" ")[1]
            )
            mc_client = gates.find({"mc_id": mc_client_id})[0]

            if "MCID" not in data:
                raise Exception(
                    "get mc error, from {}".format(self.client_address)
                )
        except:
            logger.exception("error in UpdateACardHandler")

        logger.info(
            f'start UpdateACardHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
        )

        # set datetime for mc
        try:
            dt = datetime.datetime.utcnow()
            self.request.sendall(
                "SET DATE {}\r\n".format(dt.strftime("%Y-%m-%d")).encode()
            )
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            if "DATE" not in data:
                raise Exception(
                    "set date error for  {}".format(self.client_address)
                )

            self.request.sendall(
                "SET TIME {}\r\n".format(dt.strftime("%H:%M:%S")).encode()
            )
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            if "TIME" not in data:
                raise Exception(
                    "set time error for {}".format(self.client_address)
                )

        except:
            logger.exception("error in UpdateACardHandler")

        try:
            belong_to_mc = "all"
            if "belong_to_mc" in card:
                belong_to_mc = card["belong_to_mc"]

            # add to all mc
            if belong_to_mc == "all" or not belong_to_mc:
                command = "SET CARD {card_counter},{card_number},{job_number},{name},{department},{gender},{card_category},0,{note}\r\n".format(
                    **card
                ).encode()
                logger.info(command.decode())
                self.request.sendall(command)

                data = re.sub(
                    r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
                )
                if "CARD" not in data:
                    raise Exception(
                        "upload the card to all mc error, card: {} from{}".format(
                            card, self.client_address
                        )
                    )

            # add to configed mc
            else:
                # [{'mc1': '0'}, {'mc2': 1}]
                belong_to_mc = [
                    {item.split(":")[0]: item.split(":")[1]}
                    for item in belong_to_mc.split("|")
                ]

                belong_to_mc_dict = {}  # {'mc1': '0', 'mc2': 1}
                for item in belong_to_mc:
                    belong_to_mc_dict.update(item)

                if mc_client["name"] in belong_to_mc_dict:
                    self.request.sendall(
                        "SET CARD {card_counter},{card_number},{job_number},{name},{department},{gender},{card_category},{0},{note}\r\n".format(
                            belong_to_mc_dict[mc_client["name"]], **card
                        ).encode()
                    )
                    data = re.sub(
                        r"CSN.*\r\n|\r|LOG ",
                        "",
                        self.request.recv(1024).decode(),
                    )
                    if "CARD" not in data:
                        raise Exception(
                            "upload the card to 1 mc error, card: {}, from {}".format(
                                card, self.client_address
                            )
                        )
                else:
                    self.request.sendall(
                        "CLR CARD {}\r\n".format(card["card_counter"]).encode()
                    )
                    data = re.sub(
                        r"CSN.*\r\n|\r|LOG ",
                        "",
                        self.request.recv(1024).decode(),
                    )
                    if "CARD" not in data:
                        raise Exception(
                            "update with delete a card to mc error, card: {}, from {}".format(
                                card, self.client_address
                            )
                        )
        except:
            logger.exception("error in UpdateACardHandler")

        time.sleep(self.server.p_data["server_last_time"])
        logger.info(
            "stop the UpdateACardHandler for mc {} {}".format(
                mc_client, self.client_address
            )
        )


class DeleteACardHandler(socketserver.BaseRequestHandler):
    """ send: b'CLR CARD;0\r\n'
        recv: b'CARD 0;; ; ; ;0;0; ; \r\n'
    """

    def handle(self):
        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        gates = db.gate
        mc_client = {}

        self.request.settimeout(5)
        logger.info(
            "start an DeleteACardHandler for {}".format(self.client_address)
        )
        card = self.server.p_data["card"]

        # get mc from database
        try:
            self.request.sendall(b"GET MCID\r\n")
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            mc_client_id = (
                data.replace("\r", "").replace("\n", "").split(" ")[1]
            )
            mc_client = gates.find({"mc_id": mc_client_id})[0]

            if "MCID" not in data:
                raise Exception(
                    "get mc error, mc: {} {}".format(
                        mc_client, self.client_address
                    )
                )
        except:
            logger.exception("error in GetCardTestLogHandler")

        # set datetime for mc
        try:
            dt = datetime.datetime.utcnow()
            self.request.sendall(
                "SET DATE {}\r\n".format(dt.strftime("%Y-%m-%d")).encode()
            )
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            if "DATE" not in data:
                raise Exception(
                    "set date error for  {}".format(self.client_address)
                )

            self.request.sendall(
                "SET TIME {}\r\n".format(dt.strftime("%H:%M:%S")).encode()
            )
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            if "TIME" not in data:
                raise Exception(
                    "set time error for {}".format(self.client_address)
                )

        except:
            logger.exception("error in DeleteACardHandler")

        # delete card from mc
        try:
            self.request.sendall(
                "CLR CARD {}\r\n".format(card["card_counter"]).encode()
            )
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            if "CARD" not in data:
                raise Exception(
                    "delete a card from mc error, card: {}, from {}".format(
                        card, self.client_address
                    )
                )
        except:
            logger.exception("error in DeleteACardHandler")

        time.sleep(self.server.p_data["server_last_time"])
        logger.info(
            "stop DeleteACardHandler for {}".format(self.client_address)
        )


class GetCardTestLogHandler(socketserver.BaseRequestHandler):
    """ send: b'GET LOG\r\n'
        recv：b'LOG 1536388814,1,00BC5C01,1,1,0,0,0,NO,NO,NO,NO,NO\r\n'
    """

    def handle(self):
        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        gates = db.gate
        card_collection = db.card
        cardtests = db.card_test

        self.request.settimeout(5)
        all_data = []
        mc_client = {}
        all_cardtests = []

        # get mc from database
        try:
            self.request.sendall(b"GET MCID\r\n")
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            mc_client_id = (
                data.replace("\r", "").replace("\n", "").split(" ")[1]
            )
            mc_clients = gates.find({"mc_id": mc_client_id})
            if mc_clients.count() == 0:
                raise Exception(f"数据库中无法找到 mc: {mc_client_id}")

            mc_client = gates.find({"mc_id": mc_client_id})[0]

            """ 插入数据到 logs里 """
            db_log = db.logs
            if [i for i in db_log.find({'mc_client_id': mc_client_id})]:
                db_log.update_one({'mc_client_id': mc_client_id}, {"$set": {'connect_time': time.time()}})
            else:
                db_log.insert_one({'mc_client_id': mc_client_id, 'connect_time': time.time()})

            if "MCID" not in data:
                raise Exception(
                    "get mc error, mc: {} {}".format(
                        mc_client, self.client_address
                    )
                )
        except:
            logger.exception("error in GetCardTestLogHandler")

        logger.info(
            f'start GetCardTestLogHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
        )

        # set datetime for mc
        try:
            dt = datetime.datetime.utcnow()
            self.request.sendall(
                "SET DATE {}\r\n".format(dt.strftime("%Y-%m-%d")).encode()
            )
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            if "DATE" not in data:
                raise Exception(
                    "set date error for {}".format(self.client_address)
                )

            self.request.sendall(
                "SET TIME {}\r\n".format(dt.strftime("%H:%M:%S")).encode()
            )
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            if "TIME" not in data:
                raise Exception(
                    "set time error for {}".format(self.client_address)
                )

        except:
            logger.exception("error in GetCardTestLogHandler")

        #  read all logs from mc

        while True:
            try:
                self.request.sendall(b"GET LOG\r\n")
                data = re.sub(
                    r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
                )

                if "0,0,00000000,0,0,0,0,0,,,,," in data:
                    logger.info(
                        f'break, no logs in <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
                    )
                    break

                if not data:
                    logger.info(
                        f'break, no data from <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
                    )
                    break

                all_data.append(data)
                self.request.sendall(
                    "CLR LOG {}\r\n".format(
                        data.split(",")[0].replace("LOG ", "")
                    ).encode()
                )
                self.request.recv(1024)

            except TimeoutError:
                logger.exception(
                    "except break, timeout from {} {}".format(
                        mc_client, self.client_address
                    )
                )
                break
            except:
                logger.exception(
                    "except break, timeout from {} {}".format(
                        mc_client, self.client_address
                    )
                )
                break

        # process data and save to database
        if all_data:
            try:
                all_data = "".join(all_data)
                all_data = re.sub(r"CSN.*\r\n|\r|LOG ", "", all_data).split(
                    "\n"
                )
                all_data = [x for x in all_data if len(x) > 2]  # 修复 有0时数据错误:
                #  '1547164299,268,0015E7AD,2,1,2,1,1,NO,NO,3369,6105,OK', '547164299', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1547164307,1301,001592AD,2,1,2,1,1,NO,NO,7879,5189,OK', '1547164327,1348,001591F0,2,1,2,1,1,NO,NO,2347,2235,OK', '1547164332,942,001592B8,2,1,2,0,0,NO,NO,NO,NO,NO',

                if not all_data[-1]:
                    all_data.pop()
                logger.info(
                    "format: LOG 流水号;卡片编号;卡片号码;卡片类型;进出标志;进出机号;是否通过;是否测试;RSG;手腕带检测;左脚检测;右脚检测;ERG\n"
                )
                logger.info(f"raw data:\n")
                for x in all_data:
                    logger.info(x + "\n")

                # 卡片号码 set, 用于之后查找卡片信息用
                card_number_set = set()
                for data in all_data:
                    data = data.split(",")

                    temp_dict = {
                        "log_id": data[0],
                        "card_counter": data[1],
                        "card_number": data[2],
                        "card_category": data[3],
                        "in_out_symbol": data[4],
                        "mc_id": data[5],
                        "test_result": data[6],
                        "is_tested": data[7],
                        "RSG": data[8],
                        "hand": data[9],
                        "left_foot": data[10],
                        "right_foot": data[11],
                        "after_erg": data[12],
                        "test_datetime": datetime.datetime.fromtimestamp(
                            int(data[0]), tz=datetime.timezone.utc
                        ),
                        "is_copied_to_other_database": False,
                    }

                    all_cardtests.append(temp_dict)
                    card_number_set.add(temp_dict["card_number"])

                # save all logs to database
                cardtests.insert_many(all_cardtests)

                # prepare the all cards info
                all_cards = [
                    x
                    for x in card_collection.find(
                        {"card_number": {"$in": list(card_number_set)}}
                    )
                ]
                all_logs_needed_to_send_to_frontend = copy.deepcopy(
                    all_cardtests
                )
                for log in all_logs_needed_to_send_to_frontend:
                    log["_id"] = str(log["_id"])
                    if log["card_category"] == "0":
                        log["card_category"] = "VIP"
                    if log["card_category"] == "1":
                        log["card_category"] = "只测手"
                    if log["card_category"] == "2":
                        log["card_category"] = "只测脚"
                    if log["card_category"] == "3":
                        log["card_category"] = "手脚都测"

                    if log["in_out_symbol"] == "0":
                        log["in_out_symbol"] = "出"
                    if log["in_out_symbol"] == "1":
                        log["in_out_symbol"] = "进"

                    log["test_datetime"] = (
                        log["test_datetime"].timestamp() * 1000
                    )

                    if log["test_result"] == "0":
                        log["test_result"] = "不通过"
                    if log["test_result"] == "1":
                        log["test_result"] = "通过"

                    if log["is_tested"] == "0":
                        log["is_tested"] = "不测试"
                    if log["is_tested"] == "1":
                        log["is_tested"] = "测试"

                    log["name"] = ""
                    log["job_number"] = ""
                    try:
                        r = filter(
                            lambda x: x["card_number"] == log["card_number"],
                            all_cards,
                        )
                        card = next(r)
                        del r
                        log["name"] = card["name"]
                        log["job_number"] = card["job_number"]

                    except:
                        logger.exception("cannot find card")
                        pass

                # send all logs to frontend using socketio
                # try:
                logger.info("got config REDIS_URL: " + str(REDIS_URL))
                logger.info(
                    "got all_logs_needed_to_send_to_frontend: "
                    + str(all_logs_needed_to_send_to_frontend)
                )
                socket_io = SocketIO(
                    message_queue=REDIS_URL, async_mode="threading"
                )
                socket_io.emit(
                    "send_all_cards_data_to_frontend_from_tasks",
                    all_logs_needed_to_send_to_frontend,
                    broadcast=True,
                )
                # except:
                #     pass

                # for test use
                # s = SocketIO(message_queue='redis://127.0.0.1')
                # s.emit('send_all_cards_data_to_frontend_from_tasks', [{'log_id': '1', 'name': 'name1'}, {'log_id': '2', 'name': 'name2'}])

            except:
                logger.exception(
                    "error from: {} {}".format(mc_client, self.client_address)
                )

        time.sleep(self.server.p_data["server_last_time"])
        logger.info(
            f'stop the GetCardTestLogHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
        )


class DeleteAllCardsFromMcHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(5)
        mc_client = {}

        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        cards = db.card
        gates = db.gate

        # get mc from database
        try:
            self.request.sendall(b"GET MCID\r\n")
            data = re.sub(
                r"CSN.*\r\n|\r|LOG ", "", self.request.recv(1024).decode()
            )
            mc_client_id = (
                data.replace("\r", "").replace("\n", "").split(" ")[1]
            )
            mc_client = gates.find({"mc_id": mc_client_id})[0]
            gates.update_one(
                {"mc_id": "mc_client.mc_id"},
                {
                    "$set": {
                        "ip": self.client_address[0],
                        "port": self.client_address[1],
                    }
                },
            )

            if "MCID" not in data:
                raise Exception(
                    "get mc error, mc: {} {}".format(
                        mc_client, self.client_address
                    )
                )
        except:
            logger.exception("error in DeleteAllCardsFromMcHandler")

        logger.info(
            f'start DeleteAllCardsFromMcHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
        )

        # delete all cards from mc
        commands = []
        try:
            for i in range(6000):
                # command = f'CLR CARD {i}\r\n'.encode()
                commands.append(f"CLR CARD {i}\r\n")
                # self.request.sendall(command)
                # logger.info(f'send command {command} to <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

            for card in cards.find():
                # command = f'CLR CARD {card["card_counter"]}\r\n'.encode()
                commands.append(f'CLR CARD {card["card_counter"]}\r\n')
                # self.request.sendall(command)
                # logger.info(f'send command {command} to <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

            self.request.sendall("".join(commands).encode())
            logger.info(
                f'send commands to <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>: {commands}'
            )

            logger.info(
                f'receive from <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>: {self.request.recv(100000)}'
            )

        except:
            logger.exception(
                f'DeleteAllCardsFromMcHandler error from <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
            )

        time.sleep(self.server.p_data["server_last_time"])
        logger.info(
            f'stop DeleteAllCardsFromMcHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
        )

def delete_all_cards():

    s = socket.socket()  # 创建 socket 对象
    host = SOCKET_HOST  # 获取本地主机名
    port = SOCKET_PORT  # 设置端口

    # pymongo
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    db = client[MONGODB_DB]
    cards = db.card
    gates = db.gate

    s.listen(5)  # 等待客户端连接

    def connect_socket():
        while True:
            try:
                print("尝试连接 socket")
                s.bind((host, port))  # 绑定端口
                break
            except BaseException as e:
                print("连接 socket 失败")
                time.sleep(5)

        return s.accept()


    try:
        c, client_address = connect_socket()  # 建立客户端连接
        c.sendall(b"GET MCID\r\n")
        data = re.sub(
            r"CSN.*\r\n|\r|LOG ", "", c.recv(1024).decode()
        )
        mc_client_id = (
            data.replace("\r", "").replace("\n", "").split(" ")[1]
        )
        mc_client = gates.find({"mc_id": mc_client_id})[0]
        gates.update_one(
            {"mc_id": "mc_client.mc_id"},
            {
                "$set": {
                    "ip": client_address[0],
                    "port": client_address[1],
                }
            },
        )

        if "MCID" not in data:
            raise Exception(
                "get mc error, mc: {} {}".format(
                    mc_client, client_address
                )
            )

        c.close()
    except:
        logger.exception("error in DeleteAllCardsFromMcHandler")

    logger.info(
        f'start DeleteAllCardsFromMcHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>'
    )

    commands = []

    for i in range(6000):
        # command = f'CLR CARD {i}\r\n'.encode()
        commands.append(f"CLR CARD {i}\r\n")
        # self.request.sendall(command)
        # logger.info(f'send command {command} to <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

    for card in cards.find():
        # command = f'CLR CARD {card["card_counter"]}\r\n'.encode()
        commands.append(f'CLR CARD {card["card_counter"]}\r\n')
        # self.request.sendall(command)
        # logger.info(f'send command {command} to <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

    for cmd in commands:

        c, addr = connect_socket()  # 建立客户端连接
        c.send(cmd.encode())
        c.close()

        logger.info(
         f'receive from <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>: {c.recv(100000)}'
        )




    #
    #
    # now_time = time.time()
    # ids = [i for i in range(0, 100)]
    # comment = []
    # for i in ids:
    #     _c = f'CLR CARD {i}\r\n'.encode()
    #     # comment.append(f'GET CARD {i}\r\n')
    #
    #     c, addr = s.accept()  # 建立客户端连接
    #     print(_c)
    #     c.send(_c)
    #
    #     a = c.recv(1024)
    #     print(a)
    #
    #     c.close()



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(
        self,
        server_address,
        RequestHandlerClass,
        bind_and_activate=True,
        p_data=None,
    ):

        super().__init__(
            server_address, RequestHandlerClass, bind_and_activate=True
        )
        self.p_data = p_data

    timeout = 30
    allow_reuse_address = True


@app.task()
def update_all_cards_to_mc_task(
    host=SOCKET_HOST, port=SOCKET_PORT, server_last_time=3
):
    server = ThreadedTCPServer(
        (host, port),
        UploadAllCardsHandler,
        p_data={"server_last_time": server_last_time},
    )
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start an update_all_cards task")
    time.sleep(server_last_time)
    server.shutdown()
    server.server_close()
    logger.info("stop the update_all_cards task")


@app.task()
def update_a_card_to_all_mc_task(card_dict, server_last_time=3):
    server = ThreadedTCPServer(
        (SOCKET_HOST, SOCKET_PORT),
        UpdateACardHandler,
        p_data={"card": card_dict, "server_last_time": server_last_time},
    )
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start an update_a_card task")
    time.sleep(server_last_time)
    server.shutdown()
    server.server_close()
    logger.info("stop the update_a_card task")


@app.task()
def delete_a_card_from_mc_task(card_dict, server_last_time=3):
    server = ThreadedTCPServer(
        (SOCKET_HOST, SOCKET_PORT),
        DeleteACardHandler,
        p_data={"card": card_dict, "server_last_time": server_last_time},
    )
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start a delete_a_card task")
    time.sleep(server_last_time)
    server.shutdown()
    server.server_close()
    logger.info("stop the delete_a_card task")


@app.task()
def get_logs_from_mc_task(server_last_time=3):
    server = ThreadedTCPServer(
        (SOCKET_HOST, SOCKET_PORT),
        GetCardTestLogHandler,
        p_data={"server_last_time": server_last_time},
    )
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start a get_logs_from_mc task")
    time.sleep(server_last_time)
    server.shutdown()
    server.server_close()
    logger.info("stop the get_logs_from_mc task")


@app.task()
def delete_all_cards_task(server_last_time=3):
    server = ThreadedTCPServer(
        (SOCKET_HOST, SOCKET_PORT),
        DeleteAllCardsFromMcHandler,
        p_data={"server_last_time": server_last_time},
    )

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start a delete_all_cards_task")
    time.sleep(server_last_time)
    server.shutdown()
    server.server_close()
    logger.info("stop the delete_all_cards_task")

    # server_thread = threading.Thread(target=delete_all_cards)
    # server_thread.daemon = True
    # server_thread.start()
    # logger.info("start a delete_all_cards_task")
    # server_thread.join()
    # logger.info("stop the delete_all_cards_task")


@app.task()
def send_email_of_logs(card_class_time=""):
    # pymongo
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    db = client[MONGODB_DB]
    system_config = db.system_config
    card_class_time_collection = db.card_class_time

    logger.info("start send_email_of_logs task")
    config = system_config.find()[0]
    logger.info(f"config: {config}")

    card_class = {}
    if card_class_time:
        card_class = card_class_time_collection.find_one(
            {"name": card_class_time}
        )

    else:
        card_class = {
            "name": "all",
            "working_time_from": config["work_hours"].split("-")[0],
            "working_time_to": config["work_hours"].split("-")[1],
        }

    # process data
    wb = card_log_calculate(
        MONGODB_HOST,
        MONGODB_PORT,
        MONGODB_DB,
        hours_start=card_class["working_time_from"],
        hours_end=card_class["working_time_to"],
        card_class_time=card_class_time,
    )

    # sending email

    # 获得系统时区
    system_config_timezone = int(config["timezone"])
    local_tz = datetime.timezone(
        datetime.timedelta(hours=system_config_timezone)
    )

    file_name_utf = f"report_generated_at_{datetime.datetime.now().replace(tzinfo=local_tz)}_for_{card_class['name']}_{card_class['working_time_from']}_{card_class['working_time_to']}"
    file_name = f"report_generated_at_{datetime.datetime.now().replace(tzinfo=local_tz)}"
    msg = EmailMessage()
    msg["Subject"] = file_name
    msg["From"] = config["smtp_username"]
    msg["To"] = ", ".join(config["emails"].split(","))
    msg.add_alternative(file_name_utf + "\n")
    # msg.preamble = file_name
    excel_data = io.BytesIO()
    pyexcel.get_book(bookdict=wb).save_to_memory("xlsx", stream=excel_data)
    excel_data.seek(0)

    msg.add_attachment(
        excel_data.read(),
        maintype="application",
        subtype="vnd.ms-excel",
        filename=f"{file_name_utf}.xlsx",
    )

    if config["smtp_use_ssl"]:
        with smtplib.SMTP_SSL(config["smtp_host"], config["smtp_port"]) as s:
            if config["smtp_use_tls"]:
                s.starttls()
            if config["smtp_need_auth"]:
                s.login(config["smtp_username"], config["smtp_password"])
            s.send_message(msg)
    else:
        with smtplib.SMTP(config["smtp_host"], config["smtp_port"]) as s:
            if config["smtp_use_tls"]:
                s.starttls()
            if config["smtp_need_auth"]:
                s.login(config["smtp_username"], config["smtp_password"])
            s.send_message(msg)

    logger.info("stop send_email_of_logs task")


@app.task()
def save_to_other_database():
    logger.info("start save_to_other_database task")

    try:
        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        cards = db.card
        cardtests = db.card_test
        system_config = db.system_config
        config = system_config.find()[0]

        os.environ["NLS_LANG"] = "AMERICAN_AMERICA.UTF8"
        # sqlalchemy
        engine = create_engine(
            URL(
                drivername=config["db_type"],
                host=config["db_host"],
                port=config["db_port"],
                database=config["db_name"],
                username=config["db_username"],
                password=config["db_password"],
            )
        )

        inspector = inspect(engine)

        if "logs" not in inspector.get_table_names():
            logger.info("create logs table")
            Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        logs = []
        uncopied_cardtests = list(
            cardtests.find({"is_copied_to_other_database": False})
        )

        all_cards = list(cards.find())
        for cardtest in uncopied_cardtests:
            users_list = [
                user
                for user in all_cards
                if user["card_number"] == cardtest["card_number"]
            ]
            if users_list:
                user = users_list[0]
            else:
                user = {}
            log = Log(
                id=str(cardtest.get("_id", "")),
                log_id=cardtest.get("log_id", ""),
                card_counter=cardtest.get("card_counter", ""),
                card_number=cardtest.get("card_number", ""),
                card_category=cardtest.get("card_category", ""),
                in_out_symbol=cardtest.get("in_out_symbol", ""),
                mc_id=cardtest.get("mc_id", ""),
                test_datetime=cardtest.get(
                    "test_datetime", datetime.datetime.utcnow()
                ),
                test_result=cardtest.get("test_result", ""),
                is_tested=cardtest.get("is_tested", ""),
                hand=cardtest.get("hand", ""),
                left_foot=cardtest.get("left_foot", ""),
                right_foot=cardtest.get("right_foot", ""),
                after_erg=cardtest.get("after_erg", ""),
                rsg=cardtest.get("rsg", ""),
                name=user.get("name", ""),
                job_number=user.get("job_number", ""),
                department=user.get("department", ""),
                gender=user.get("gender", ""),
                note=user.get("note", ""),
                belong_to_mc=user.get("belong_to_mc", ""),
            )

            if log.card_category == "0":
                log.card_category = "vip"
            if log.card_category == "1":
                log.card_category = "只测手"
            if log.card_category == "2":
                log.card_category = "只测脚"
            if log.card_category == "3":
                log.card_category = "手脚都测"
            if log.gender == "0":
                log.gender = "女"
            if log.gender == "1":
                log.gender = "男"
            if log.test_result == "0":
                log.test_result = "不通过"
            if log.test_result == "1":
                log.test_result = "通过"
            if log.is_tested == "0":
                log.is_tested = "不测试"
            if log.is_tested == "1":
                log.is_tested = "测试"

            logs.append(log)

        logger.info(str(logs))
        session.add_all(logs)
        session.commit()

        requests = []
        for cardtest in uncopied_cardtests:
            requests.append(
                UpdateOne(
                    {"_id": cardtest["_id"]},
                    {"$set": {"is_copied_to_other_database": True}},
                )
            )
        try:
            cardtests.bulk_write(requests)
        except bulk.InvalidOperation:
            logger.info(
                "pymongo bulk InvalidOperation: No operations to execute"
            )

        session.close()
        engine.dispose()
    except Exception as e:
        logger.exception(e)

    logger.info("stop save_to_other_database task")


@app.task()
def update_cards_from_other_database():
    logger.info("start update_cards_from_other_database")
    os.environ["NLS_LANG"] = "AMERICAN_AMERICA.UTF8"
    
    # pymongo
    connect(db=MONGODB_DB, host=MONGODB_HOST, port=MONGODB_PORT)
    config = None
    try:
        config = SystemConfig.objects.get()
    except SystemConfig.DoesNotExist:
        config = SystemConfig()
        config.save()

    # sqlalchemy
    engine = create_engine(
        URL(
            drivername=config["update_db_type"],
            host=config["update_db_host"],
            port=int(config["update_db_port"]),
            database=config["update_db_name"],
            username=config["update_db_username"],
            password=config["update_db_password"],
        ),
        exclude_tablespaces=[],
    )
    conn = engine.connect()

    inspector = inspect(engine)

    if config["update_db_table_name"] not in inspector.get_table_names():
        logger.info("can't find table {} in database!".format(config["update_db_table_name"]))
        return

    meta = MetaData()
    original_cards_table = Table(
        config["update_db_table_name"],
        meta,
        autoload=True,
        autoload_with=engine,
    )
    logger.info(
        "got table columns: {}".format(
            [c.name for c in original_cards_table.columns]
        )
    )

    s = original_cards_table.select()
    original_cards = conn.execute(s)
    original_card_list = []  # list of dict
    not_need_to_delete_cards = []
    cards_deleted = []
    error_cards = []

    for original_card in original_cards:
        original_card_list.append({
            'empno': original_card[0],
            'empname': original_card[1],
            'cardfixno': original_card[2],
            'dptname1': original_card[3],
            'dptname2': original_card[4],
            'dptname3': original_card[5],
            'dptname4': original_card[6],
            'empcardtid': original_card[7],
            'upd_date': original_card[8],
        })

    for original_card in original_card_list:
        # mongodb 中找得到工号的 卡片, 则更新
        not_need_to_delete_cards.append(original_card["empno"])
        try:
            card = Card.objects.get(job_number=original_card["empno"])
            card.name = original_card["empname"]
            card.card_number = normalize_card_number(original_card["cardfixno"])
            card.department = original_card["dptname4"]
            card.department_1 = original_card["dptname1"]
            card.department_2 = original_card["dptname2"]
            card.department_3 = original_card["dptname3"]
            card.origin_card_id = original_card["empcardtid"]
            card.save()

        # mongodb 未中找得到工号的 卡片, 则新建
        except Card.DoesNotExist:
            card = Card(
                job_number=original_card["empno"],
                name=original_card["empname"],
                card_number=normalize_card_number(original_card["cardfixno"]),
                department=original_card["dptname4"],
                department_1=original_card["dptname1"],
                department_2=original_card["dptname2"],
                department_3=original_card["dptname3"],
                origin_card_id=original_card["empcardtid"],
            )
            card.save()
        except Exception as e:
            error_cards.append(
                {"original_job_number": original_card["empno"], 'error': e}
            )
    for card in Card.objects.filter(job_number__nin=not_need_to_delete_cards):
        cards_deleted.append({'job_number': card['job_number']})
        card.delete()

    logger.log('deleted cards: {}'.format(cards_deleted))
    logger.log('error cards: {}'.format(error_cards))
    
        


