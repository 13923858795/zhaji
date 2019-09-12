import os, time
from uuid import uuid1
from celerybeatmongo.models import PeriodicTask
from flask import Blueprint, abort, current_app, jsonify, make_response, request
from mongoengine.queryset.visitor import Q
from pymongo import MongoClient, UpdateOne, bulk
from app.mod_task.tasks import (
    update_all_cards_to_mc_task,
    delete_all_cards_task,
)


bp = Blueprint("mod_task", __name__)

MONGODB_DB = os.environ.get("MONGODB_DB", "quatek_web_app")
MONGODB_HOST = os.environ.get("MONGODB_HOST", "127.0.0.1")
MONGODB_PORT = os.environ.get("MONGODB_PORT", 27017)
client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client[MONGODB_DB]


@bp.route("/connect_status", methods=["GET"])
def connect_status():

    db_every = [i for i in db.log_every.find()]
    if db_every:
        log_every = db_every[0]['value']
    else:
        log_every = 60*2

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

    return jsonify(resp), {"Content-Type": "application/json"}


@bp.route("/task-interval", methods=["GET"])
def task_interval():
    if request.method == "GET":
        tasks = PeriodicTask.objects.filter(interval__exists=True)
        return tasks.to_json(), {"Content-Type": "application/json"}


@bp.route("/task-crontab", methods=["GET"])
def task_crontab():
    if request.method == "GET":
        tasks = PeriodicTask.objects.filter(crontab__exists=True)
        return tasks.to_json(), {"Content-Type": "application/json"}


@bp.route("/task-interval-add-one", methods=["POST"])
def task_interval_add_one():
    if request.method == "POST":
        task = PeriodicTask(
            name=str(uuid1()),
            task=request.json["task"],
            enabled=True,
            run_immediately=True,
            interval=PeriodicTask.Interval(
                every=int(request.json["every"]), period="seconds"
            ),
        )

        every = int(request.json["every"])
        db_every = db.log_every
        if [i for i in db_every.find()]:
            db_every.update_one({'name': 'log_every'}, {"$set": {'value': every}})
        else:
            db_every.insert_one({'name': 'log_every', 'value': every})

        result = task.save()
        return result.to_json(), {"Content-Type": "application/json"}


@bp.route("/task-crontab-add-one", methods=["POST"])
def task_crontab_add_one():
    if request.method == "POST":
        if "app.mod_task.tasks.send_email_of_logs" in request.json["task"]:
            task = PeriodicTask(
                name=str(uuid1()),
                task=request.json["task"].split(":")[0],
                enabled=True,
                crontab=PeriodicTask.Crontab(
                    minute=request.json["minute"],
                    hour=request.json["hour"],
                    day_of_month=request.json["day_of_month"],
                    month_of_year=request.json["month_of_year"],
                    day_of_week=request.json["day_of_week"],
                ),
                args=[request.json["task"].split(":")[1]],
            )
            result = task.save()
            return result.to_json(), {"Content-Type": "application/json"}

        task = PeriodicTask(
            name=str(uuid1()),
            task=request.json["task"],
            enabled=True,
            crontab=PeriodicTask.Crontab(
                minute=request.json["minute"],
                hour=request.json["hour"],
                day_of_month=request.json["day_of_month"],
                month_of_year=request.json["month_of_year"],
                day_of_week=request.json["day_of_week"],
            ),
        )
        result = task.save()
        return result.to_json(), {"Content-Type": "application/json"}


@bp.route("/task-delete", methods=["POST"])
def task_delete():
    if request.method == "POST":
        task = PeriodicTask.objects.get(pk=request.json["task_id"])
        result = task.delete()
        return task.to_json(), {"Content-Type": "application/json"}


@bp.route("/does-task-exist", methods=["GET"])
def does_task_exist():
    if request.method == "GET":
        q = request.args.get("q", None)
        tasks_count = PeriodicTask.objects.filter(
            task__in=[
                "app.mod_task.tasks.get_logs_from_mc_task",
                "app.mod_task.tasks.save_to_other_database",
            ]
        ).count()

        if (
            q == "app.mod_task.tasks.get_logs_from_mc_task"
            or q == "app.mod_task.tasks.save_to_other_database"
        ) and tasks_count > 0:

            return (
                jsonify({"does_task_exist": True}),
                {"Content-Type": "application/json"},
            )
        else:
            return (
                jsonify({"does_task_exist": False}),
                {"Content-Type": "application/json"},
            )


@bp.route("/sync-cards", methods=["POST"])
def sync_cards():
    update_all_cards_to_mc_task.delay(server_last_time=30)
    return "done"


@bp.route("/delete-all-cards", methods=["POST"])
def delete_all_cards():
    delete_all_cards_task.delay(server_last_time=30)
    return "done"
