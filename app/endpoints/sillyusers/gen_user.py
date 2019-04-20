import silly
import uuid


def user_info(user: str = None, id: str = None):
    if id == None:
        set_id = uuid.uuid1()
    else:
        set_id = id
    if user is None:
        username: str = silly.name(capitalize=True)
    else:
        username = user

    title: str = silly.title(capitalize=True)
    company: str = silly.company(capitalize=True)
    address: str = silly.address(capitalize=True)
    city: str = silly.city(capitalize=True)
    country: str = silly.country(capitalize=True)
    postal_code: str = silly.postal_code()
    email = silly.email()
    phone = silly.phone_number()
    description: str = silly.paragraph(length=3)
    website = f"http://www.{silly.domain()}"
    create_date = (
        f"{silly.datetime().year}/{silly.datetime().month}/{silly.datetime().day}"
    )

    result = {
        "useId": str(set_id),
        "username": username,
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
        "dateCreate": create_date,
    }
    return result


if __name__ == "__main__":
    id = "123"
    user = None
    for i in range(0, 1):
        x = user_info(user, id)
        print(x)
