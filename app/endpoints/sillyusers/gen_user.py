# -*- coding: utf-8 -*-
import silly
import uuid
import random


def user_info():

    set_id = uuid.uuid1()
    rand_name: str = silly.noun()
    rand_num: int = random.randint(1, 101)
    username: str = f"{rand_name}-{rand_num}"
    firstName: str = silly.verb()
    lastName: str = silly.noun()
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
    return result


def user_test_info():
    # set_id = uuid.uuid1()
    rand_name: str = silly.noun()
    rand_num: int = random.randint(1, 101)
    username: str = f"{rand_name}-{rand_num}"
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

    result = {
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
    return result


# if __name__ == "__main__":
#     id = "123"
#     user = None
#     for i in range(0, 1):
#         x = user_info(user, id)
#         print(x)
