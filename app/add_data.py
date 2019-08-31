# -*- coding: utf-8 -*-
import silly
import uuid
import random
from datetime import datetime, timedelta
import asyncio
import random
import uuid
import os
from datetime import datetime, date, timedelta, time
from loguru import logger


currentTime = datetime.now()


async def user_sample_info():
    rand_name: str = silly.noun()
    username: str = f"{rand_name}-{ran_num()}"
    firstName: str = silly.verb()
    lastName: str = silly.noun()
    password: str = "testpassword"
    title: str = silly.title(capitalize=True)
    company: str = silly.company(capitalize=True)
    address: str = silly.address(capitalize=True)
    city: str = silly.city(capitalize=True)
    country: str = silly.country(capitalize=True)
    postal_code: str = silly.postal_code()
    email = silly.email()
    phone = silly.phone_number()
    description: str = silly.paragraph(length=1)
    website = f"http://www.{silly.domain()}"

    userInformation = {
        "user_name": username,
        "firstName": firstName,
        "lastName": lastName,
        "password": password,
        "title": title,
        "company": company,
        "address": address,
        "city": city,
        "country": country,
        "postal": postal_code,
        "email": email,
        "phone": phone,
        "website": website,
        "description": description,
    }

    try:
        # TODO: build this sql call
        return userInformation
    except Exception as e:
        print(e)


def ran_num():
    rand_num: int = random.randint(1, 101)
    return rand_num


def future_date():
    date = datetime.now()
    modified_date = date + timedelta(days=ran_num())
    date_due = datetime.strftime(modified_date, "%Y/%m/%d")
    return modified_date


async def todo_sample_info():
    title: str = f"{silly.verb()} {silly.noun()}"
    username: str = f"{silly.noun()}-{ran_num()}"
    date_due = future_date()
    todoInformation = {
        "todoId": str(uuid.uuid1()),
        "title": title,
        "userId": username,
        "description": username,
        "dateDue": str(date_due),
        "isComplete": False,
        "dateCreate": currentTime,
        "dateUpdate": currentTime,
        "dateComplete": None,
    }

    try:
        # TODO: build this sql call
        return todoInformation
    except Exception as e:
        print(e)
