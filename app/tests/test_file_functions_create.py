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
    get_data_directory_list,
    open_csv,
    open_json,
    save_csv,
    save_json,
)

time_str = datetime.datetime.now()

# TODO: Improve Exception handling to check logging


class test_file_processing(unittest.TestCase):
    def test_save_json(self):
        sample_dict = {"name": "bob", "date": str(time_str)}
        file_named = "test_1.json"
        json_data = []
        for i in range(10):
            sample_dict = {"name": "bob", "date": str(time_str)}
            json_data.append(sample_dict)

        result = save_json(file_named, json_data)
        assert result == "complete"

    def test_save_csv(self):
        csv_data = []
        file_named = "test_1.csv"
        csv_data = []
        count = 0
        for i in range(10):
            if count == 0:
                sample_dict = ["name", "date"]
            else:
                sample_dict = ["bob", str(datetime.datetime.now())]
            count += 1
            csv_data.append(sample_dict)

            result = save_csv(file_named, csv_data)
            assert result == "complete"
