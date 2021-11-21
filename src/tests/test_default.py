# -*- coding: utf-8 -*-
# import unittest
from unittest import TestCase

from starlette.testclient import TestClient

from src.main import app

client = TestClient(app)


class Test(TestCase):
    def test_index(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_joke(self):
        response = client.get("/joke")
        assert response.status_code == 200
        assert response.json is not None

    def test_information(self):
        response = client.get("/info")
        assert response.status_code == 200

    def test_metrics(self):
        response = client.get("/api/health/metrics")
        assert response.status_code == 200

    def test_robots(self):
        response = client.get("/robots.txt")
        assert response.status_code == 200
