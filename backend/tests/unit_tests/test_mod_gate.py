import datetime
import json
import os
import random
import pprint
import pyexcel

import pytest
from pymongo import MongoClient

from app import create_app
from app.mod_auth.models import User
from app.mod_gate.models import Card, CardTest, Gate


def test_gates_filter(client):
    for i in range(10):
        gate = Gate(name="gate1_" + str(i), category="category1")
        gate.save()

    for i in range(10):
        gate = Gate(name="gate2_" + str(i), category="category2")
        gate.save()

    rv = client.get("/gates?q=category1")
    gates = json.loads(rv.data.decode())
    assert len(gates) == 10


def test_cardtests_search_with_query_string(client):
    """ GIVEN 120 cardtests, 
        WHEN query with datetime_from, datetime_to and query_string
        THEN check returned cardtests lengths
    """

    dt = datetime.datetime.utcnow()
    cardtests = []

    gate = Gate(mc_id="mc_id_3", name="gate3")
    gate.save()

    for i in range(60):
        cardtest = CardTest(
            card_number="card_number_{}".format(i),
            test_datetime=dt + datetime.timedelta(minutes=i),
            job_number="job_number_{}".format(i),
            mc_id="mc_id_3",
        )
        cardtests.append(cardtest)

    for i in range(60, 120):
        cardtest = CardTest(
            card_number="card_number_{}".format(i),
            test_datetime=dt + datetime.timedelta(minutes=i),
            job_number="job_number_{}".format(i),
            mc_id="mc_id_4",
        )
        cardtests.append(cardtest)

    CardTest.objects.insert(cardtests)

    now = datetime.datetime.utcnow()
    datetime_from = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    datetime_to = (now + datetime.timedelta(minutes=120)).strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    query_string1 = "card_number_19"
    rv1 = client.get(
        "/cardtests?datetime_from={}&datetime_to={}&q={}".format(
            datetime_from, datetime_to, query_string1
        )
    )
    cardtests1 = json.loads(rv1.data.decode())
    assert len(cardtests1) == 1

    query_string2 = "gate3"
    rv2 = client.get(
        "/cardtests?datetime_from={}&datetime_to={}&q={}".format(
            datetime_from, datetime_to, query_string2
        )
    )
    cardtests2 = json.loads(rv2.data.decode())
    assert len(cardtests2) == 50

    query_string3 = ""
    rv3 = client.get(
        "/cardtests?datetime_from={}&datetime_to={}&q={}".format(
            datetime_from, datetime_to, query_string3
        )
    )
    cardtests3 = json.loads(rv3.data.decode())
    assert len(cardtests3) == 50


def test_cardtests2(client, database):
    # GIVEN some card tests
    # WHEN request route cardtests2
    # THEN return the right excel io

    card_test_collection = database["card_test"]

    datetime_now = datetime.datetime.utcnow()

    # in_out_symbol: 0 : out | 1 : in
    # test_result: 0 : 不通过 | 1 : 通过
    results = card_test_collection.insert_many(
        [
            # out log
            {
                "log_id": "1",
                "card_counter": "1",
                "card_number": "F13E9C19",
                "card_category": "2",
                "in_out_symbol": "0",
                "mc_id": "mc1",
                "test_datetime": datetime.datetime(2019, 3, 4, 18),
                "test_result": "1",
                "is_tested": "1",
                "hand": "111",
                "left_foot": "111",
                "right_foot": "111",
                "after_erg": "",
                "rsg": "",
                "created_time": datetime_now,
                "is_copied_to_other_database": False,
            },
            # in log 1: test_datetime > out log
            {
                "log_id": "2",
                "card_counter": "1",
                "card_number": "F13E9C19",
                "card_category": "2",
                "in_out_symbol": "1",
                "mc_id": "mc2",
                "test_datetime": datetime.datetime(2019, 3, 4, 19),
                "test_result": "1",
                "is_tested": "1",
                "hand": "222",
                "left_foot": "222",
                "right_foot": "222",
                "after_erg": "",
                "rsg": "",
                "created_time": datetime_now,
                "is_copied_to_other_database": False,
            },
            # in log 2: test_result is failed
            {
                "log_id": "3",
                "card_counter": "1",
                "card_number": "F13E9C19",
                "card_category": "2",
                "in_out_symbol": "1",
                "mc_id": "mc2",
                "test_datetime": datetime.datetime(2019, 3, 4, 13),
                "test_result": "0",
                "is_tested": "1",
                "hand": "9264",
                "left_foot": "67450",
                "right_foot": "60787",
                "after_erg": "",
                "rsg": "",
                "created_time": datetime_now,
                "is_copied_to_other_database": False,
            },
            # in log 3
            {
                "log_id": "4",
                "card_counter": "1",
                "card_number": "F13E9C19",
                "card_category": "2",
                "in_out_symbol": "1",
                "mc_id": "mc2",
                "test_datetime": datetime.datetime(2019, 3, 4, 14),
                "test_result": "1",
                "is_tested": "1",
                "hand": "9264",
                "left_foot": "67450",
                "right_foot": "60787",
                "after_erg": "",
                "rsg": "",
                "created_time": datetime_now,
                "is_copied_to_other_database": False,
            },
            # in log 4
            {
                "log_id": "5",
                "card_counter": "1",
                "card_number": "F13E9C19",
                "card_category": "2",
                "in_out_symbol": "1",
                "mc_id": "mc2",
                "test_datetime": datetime.datetime(2019, 3, 4, 15),
                "test_result": "1",
                "is_tested": "1",
                "hand": "9264",
                "left_foot": "67450",
                "right_foot": "60787",
                "after_erg": "",
                "rsg": "",
                "created_time": datetime_now,
                "is_copied_to_other_database": False,
            },
        ]
    )
