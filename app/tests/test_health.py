# -*- coding: utf-8 -*-
import datetime
import json
import os
import sys
import time
import unittest
from pathlib import Path
from unittest import mock

import pytest
import requests
import requests_mock
from loguru import logger
from requests.exceptions import Timeout
from starlette.testclient import TestClient

from app.com_lib.file_functions import open_json, save_json
from app.health.checks import get_platform
from app.main import app

client = TestClient(app)

directory_to__files: str = "data"


class TestHealth(unittest.TestCase):
    def test_health_status(self):
        response = client.get(f"/api/health/")
        assert response.status_code == 200

    def test_health_system_info(self):

        response = client.get(f"/api/health/system-info")
        assert response.status_code == 200

    def test_health_processes(self):

        response = client.get(f"/api/health/processes")
        assert response.status_code == 200

    def test_get_platform(self):
        result = get_platform()
        assert result is not None
