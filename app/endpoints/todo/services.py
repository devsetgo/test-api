import asyncio
import random
import uuid
import os
from datetime import datetime, timedelta
import time
from loguru import logger


file_path = (os.path.abspath("logfile/file_1.log"))
# logger.debug("That's it, beautiful and simple logging!")
logger.add(file_path, backtrace=True, retention="10 days",rotation="10 MB")


def list_count(full_list):
    
    count = 0
    for i in full_list:
        count+=1
    return count

def get_todo(id, full_list):
    for i in full_list:
        if id == i['id']:
            result = i
    print(result)
    return result

def getList(data, user:str):
    result = []
    for i in data:
        if i['userId']==user:
            result.append(i)
    return result