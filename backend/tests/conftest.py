import os
import pytest
import pymongo
import time
import datetime
import random
from app.mod_gate.models import Card, CardTest

from app import create_app


@pytest.fixture(scope="module")
def client():
    # get configs fom environment
    os.environ["TESTING"] = "True"
    os.environ["MONGODB_HOST"] = "127.0.0.1"
    os.environ["MONGODB_PORT"] = "27017"
    os.environ["MONGODB_DB"] = "test_db"

    app = create_app()
    client = app.test_client()

    yield client


@pytest.fixture(scope="module")
def database():
    mongo_client = pymongo.MongoClient(
        host=os.environ.get("MONGODB_HOST", "127.0.0.1"),
        port=os.environ.get("MONGODB_PORT", "27017"),
    )
    database = mongo_client[os.environ.get("MONGODB_DB", "test_db")]
    yield database

    mongo_client.drop_database(os.environ.get("MONGODB_DB", "test_db"))


@pytest.fixture()
def create_random_cards(database):
    random_cards = []
    for i in range(500):
        random_cards.append(
            Card(
                card_number="{:08X}".format(random.randint(0, 4_294_967_295)),
                card_category=random.choice(["0", "1", "2", "3"]),
                name=f"name{i}",
                job_number=str(random.randint(1, 9_999_999_999)),
                department=f"部门{i}",
                gender=random.choice(["0", "1"]),
                note="default note",
                belong_to_mc="all",
            )
        )
    insert_many_results = Card.objects.insert(random_cards)
    yield insert_many_results


@pytest.fixture()
def create_cardtest_list(database):
    dt = datetime.datetime.utcnow()
    cardtest_list = []
    cards = Card.objects.all()
    card_numbers = set()
    for card in cards:
        card_numbers.add(card.card_number)
    card_numbers = list(card_numbers)
    for i in range(50000):
        cardtest_list.append(
            CardTest(
                log_id=f"id{i}",
                card_counter=f"{i}",
                card_number=random.choice(card_numbers),
                card_category=random.choice(["0", "1", "2", "3"]),
                in_out_symbol=random.choice(["0", "1"]),
                mc_id=random.choice(["mc1", "mc2"]),
                test_datetime=dt + datetime.timedelta(minutes=i),
                test_result=random.choice(["0", "1"]),
                is_tested=random.choice(["0", "1"]),
                hand=str(random.randrange(0, 100_000)),
                left_foot=str(random.randrange(0, 100_000)),
                right_foot=str(random.randrange(0, 100_000)),
            )
        )
    CardTest.objects.insert(cardtest_list)
    yield cardtest_list


@pytest.fixture()
def data_for_route_download_cards(database):
    test_collection = database["test_collection"]
    test_collection.insert({"foo": "bar"})
