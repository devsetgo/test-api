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

import pytest
from app.main import app

# from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

# from starlette.exceptions import HTTPException

client = TestClient(app)


class test_default_endpoints(unittest.TestCase):
    def test_index(self):
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
