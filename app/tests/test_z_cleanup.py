# -*- coding: utf-8 -*-
# import json
# import csv
import datetime
import os
import time
import unittest
from unittest import mock

import pytest

from com_lib.file_functions import (
    create_sample_files,
    delete_file,
    get_data_directory_list,
    open_csv,
    open_json,
    open_text,
    save_csv,
    save_json,
    save_text,
)


class Test(unittest.TestCase):
    def test_clean_up(self):
        files = [
            "test_1_error.json",
            "test_1_todo.json",
            "test_data_test_user.json",
            "test_data_todos.json",
            "test_data_users.json",
            "test_1.csv",
            "test_sample.csv",
        ]
        for f in files:
            delete_file(f)
