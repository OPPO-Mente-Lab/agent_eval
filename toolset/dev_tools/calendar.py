import calendar 
import datetime


def days_of_month(args):
    year, month = args['year'], args['month']
    day_num = calendar.monthrange(year, month)[1]
    days = []
    # weekday_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_en = ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"]
    for i in range(1, day_num+1):
        d = datetime.datetime(year, month, i)
        days.append((i, weekday_en[d.weekday()]))
    return days


def display_calendar_of_month(args):
    year, month = args['year'], args['month']
    return calendar.month(year, month)



