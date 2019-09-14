# -*- coding: utf-8 -*-
import datetime
import logging
import os
import sys
import time
import unittest
from unittest import mock

import pytest
import requests
import requests_mock
from _pytest.logging import caplog
from requests.exceptions import Timeout
from starlette.testclient import TestClient

from app.main import app, shutdown_event, startup_event

client = TestClient(app)


class test_default_endpoints(unittest.TestCase):
    def test_index(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_joke(self):
        response = client.get("/joke")
        assert response.status_code == 200
        assert response.json is not None

    def test_information(self):
        response = client.get("/information")
        assert response.status_code == 200
