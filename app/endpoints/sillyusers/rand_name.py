# -*- coding: utf-8 -*-
from random import randint

names = ["Mike", "Dan", "Ger", "Chuck", "Valerie", "Cathy", "Linda", "Kristi"]


def randName():
    l = len(names) - 1
    # print(l)
    name = names[randint(0, l)]
    return name
