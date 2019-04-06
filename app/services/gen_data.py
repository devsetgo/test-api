import random
import uuid
import datetime
# from rand_word import r_w
from services.rand_word import r_w


def create_list(qty: int):
    response_list = []
    for i in range(qty):
        id = uuid.uuid1()
        rand_str = r_w(random.randrange(1, 10))

        r_tags = []
        for t in range(0, random.randrange(1, 10)):
            rand_tag = r_w(1)
            rt = {'tag': rand_tag}
            r_tags.append(rt)

        right_now = datetime.datetime.now()

        j_response = {
            'id': id, 'name': rand_str, 'dateTime': str(right_now), 'tags':
            {
                str(r_tags)
            }
        }
        response_list.append(j_response)
    return response_list


def create_item(id: str):

    rand_str = r_w(random.randrange(1, 10))
    # id = uuid.uuid1()
    right_now = datetime.datetime.now()

    r_tags = []
    for t in range(0, random.randrange(1, 10)):
        rand_tag = r_w(1)
        rt = {'tag': rand_tag}
        r_tags.append(rt)

    result = {
        'id': id, 'name': rand_str, 'dateTime': str(right_now), 'tags':
        {
            str(r_tags)
        }
    }

    return result


if __name__ == '__main__':
    x = create_item('123-456')

    print(x)
