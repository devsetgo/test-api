# -*- coding: utf-8 -*-
import random
import uuid

import silly


def generate_data():

    set_id = uuid.uuid1()
    rand_name: str = silly.noun()
    rand_num: int = random.randint(1, 10000)
    username: str = f"{rand_name}-{rand_num}"
    first_name: str = silly.verb()
    last_name: str = rand_name
    password: str = f"{silly.verb()}-{silly.noun()}"
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

    result = {
        "userId": set_id,
        "user_name": username,
        "firstName": first_name,
        "lastName": last_name,
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
    return result


def user_info():
    user_data = generate_data()

    result = {
        "userId": user_data["userId"],
        "user_name": user_data["user_name"],
        "firstName": user_data["firstName"],
        "lastName": user_data["lastName"],
        "password": user_data["password"],
        "title": user_data["title"],
        "company": user_data["company"],
        "address": user_data["address"],
        "city": user_data["city"],
        "country": user_data["country"],
        "postal": user_data["postal"],
        "email": user_data["email"],
        "phone": user_data["phone"],
        "website": user_data["website"],
        "description": user_data["description"],
    }
    return result


def user_test_info():
    user_data = generate_data()

    result = {
        "user_name": user_data["user_name"],
        "firstName": user_data["firstName"],
        "lastName": user_data["lastName"],
        "password": user_data["password"],
        "title": user_data["title"],
        "company": user_data["company"],
        "address": user_data["address"],
        "city": user_data["city"],
        "country": user_data["country"],
        "postal": user_data["postal"],
        "email": user_data["email"],
        "phone": user_data["phone"],
        "website": user_data["website"],
        "description": user_data["description"],
    }
    return result
