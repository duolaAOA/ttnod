# -*-coding:utf-8 -*-
import datetime


def string_to_datetime(string: str):
    """
    将string转为datetime类型
    """
    return datetime.datetime.strptime(string, "%Y-%m-%d")



def get_weeks_before_toady(n=1):
    """
    format: "YYYY-MM-DD HH:MM:SS"
    """
    now = datetime.datetime.now()
    if n < 0:
        return datetime.datetime(now.year, now.month, now.day, now.hour,
                                 now.minute, now.second)
    else:
        n_days_before = now - datetime.timedelta(days=n * 7)
    return datetime.datetime(n_days_before.year, n_days_before.month,
                             n_days_before.day, n_days_before.hour,
                             n_days_before.minute, n_days_before.second)


def get_days_before_current_datetime(string: str, days=1) -> datetime.datetime:
    current_datetime = string_to_datetime(string)

    n_days_before = current_datetime + datetime.timedelta(days)
    return datetime.datetime(n_days_before.year, n_days_before.month,
                             n_days_before.day, n_days_before.hour,
                             n_days_before.minute, n_days_before.second)



