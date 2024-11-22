
# info about agent/assistant itself

import time
import datetime
import yaml
import os
import calendar


def get_current_time(args=None):
    now = datetime.datetime.now()
    days = ["Monday", "Tuesday", "Wednesday", 
        "Thursday", "Friday", "Saturday", "Sunday"] 
    format_now = now.strftime("%Y-%m-%d %H:%M:%S") + f" {days[now.weekday()]}"
    return {"current_time": format_now}


def get_my_location(args=None):
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../config.yml")) as file:
        conf = yaml.safe_load(file)

    return {"location": conf["AGENT"]["location"]}


def get_calendar(args=None):
    if args is None or len(args) == 0:
        now = datetime.datetime.now()
        return {"result": calendar.month(now.year, now.month)}
    if "year" not in args:
        now = datetime.datetime.now()
        year = now.year
    else:
        year = args['year']
    if "month" not in args:
        return {"result": calendar.calendar(args["year"])}
    else:
        return {"result": calendar.month(args["year"], args["month"])}




