from datetime import datetime
from time import mktime

import pytz


def get_iso_date(date):
    try:
        return datetime.strptime(date, '%d-%B-%Y').strftime('%Y-%m-%d')
    except Exception as e:
        print(e)
        return


def get_str_date(date):
    try:
        return date.strftime('%d/%m/%Y')
    except Exception as e:
        print(e)
        return ''


def get_str_datetime(date):
    try:
        return utc_to_time(date).strftime('%d %b %Y %H:%M')
    except Exception as e:
        print(e)
        return ''


def utc_to_time(naive, timezone="Asia/Kolkata"):
    return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))


def date_to_utc(date):
    utc_millis = int(mktime(date.timetuple()) * 1000)
    return utc_millis


def get_str_to_date(date_string, date_format):
    try:
        return datetime.strptime(date_string, date_format).replace(tzinfo=pytz.utc)
    except Exception as e:
        print(e)
        return

def timestamp_to_datetime(ts):
    ts = int(ts/1000)
    return datetime.utcfromtimestamp(ts)

def get_datetime_now():
    return datetime.now().replace(tzinfo=pytz.utc)

