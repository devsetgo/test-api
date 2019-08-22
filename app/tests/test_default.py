# -*- coding: utf-8 -*-
import datetime
import os
import sys
import time
import unittest
from unittest import mock
import requests
from requests.exceptions import Timeout
import requests_mock
import logging
import pytest
from _pytest.logging import caplog
from app.main import app, startup_event, shutdown_event

# from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

# from starlette.exceptions import HTTPException

client = TestClient(app)


class test_default_endpoints(unittest.TestCase):
    def test_index(self):
        # client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200

    def test_joke(self):
        # client = TestClient(app)
        response = client.get("/joke")
        assert response.status_code == 200
        assert response.json != None
        # ['Credit'] == "https://pyjok.es/"

    def test_information(self):
        # client = TestClient(app)
        response = client.get("/information")
        assert response.status_code == 200

    # async def test_startup(self):
    #     response = startup_event()
    #     assert await response['database'] == 'connected'
