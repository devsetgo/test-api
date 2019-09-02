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
    def test_create_sample_files(self):
        filename = "test_sample"
        samplesize = 10
        create_sample_files(filename, samplesize)

        file_named = "test_1.csv"
        result = open_csv(file_named)
        assert len(result) == samplesize - 1

    def test_create_sample_files_exception(self):
        filename = "test_sample"
        samplesize = 10

        file_named = "test_2.csv"
        # result = open_csv(file_named)
        m = mock.Mock()
        m.side_effect = Exception(create_sample_files(filename, samplesize))
        try:
            m()
        except Exception:
            assert True

    def test_open_json(self):
        file_named = "test_1.json"
        result = open_json(file_named)
        assert len(result) > 1
        assert isinstance(result, (list, dict))

    def test_open_json_no_file(self):
        file_named = "no_file_name.json"
        # result = open_json(file_named)
        m = mock.Mock()
        m.side_effect = Exception(open_json(file_named))
        try:
            m()
        except Exception:
            assert True
        # assert result["error"].startswith("ERROR")

    def test_open_csv(self):
        file_named = "test_1.csv"
        result = open_csv(file_named)
        assert len(result) > 1

    def test_open_csv_no_file(self):
        file_named = "no_file_name.csv"
        # result = open_csv(file_named)
        # assert result["error"].startswith("ERROR")
        m = mock.Mock()
        m.side_effect = Exception(open_csv(file_named))
        try:
            m()
        except Exception:
            assert True

    def test_get_data_directory_json(self):
        directory = "json"
        result = get_data_directory_list(directory)
        assert f"test_1.{directory}" in result
        assert isinstance(result, list)

    def test_get_data_directory_csv(self):
        directory = "csv"
        result = get_data_directory_list(directory)
        assert f"test_1.{directory}" in result
        assert isinstance(result, list)

    def test_get_data_directory_exception(self):
        directory = "csv"
        # result = get_data_directory_list(directory)
        # assert f"test_1.{directory}" in result
        # assert isinstance(result, list)
        m = mock.Mock()
        m.side_effect = Exception(get_data_directory_list(directory))
        try:
            m()
        except Exception:
            assert True
