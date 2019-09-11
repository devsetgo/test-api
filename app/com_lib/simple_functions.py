# -*- coding: utf-8 -*-
import time
from datetime import date, datetime, time, timedelta


def get_current_datetime() -> datetime:
    """
    get the current datetime

    Returns:
        datetime.now()
    """
    currentTime: datetime = datetime.now()
    # print(type(currentTime))
    return currentTime
