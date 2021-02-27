# -*- coding: utf-8 -*-
import unittest
from pathlib import Path

from starlette.testclient import TestClient

from src.main import app

client = TestClient(app)

directory_to__files: str = "data"

base_url: str = "api/v1/textblob"


class Test(unittest.TestCase):
    # text endpoint
    def test_spellcheck_four_hundred(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/no_data.txt"

        url = f"{base_url}/spellcheck"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 400

    def test_spellcheck(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/bad.txt"

        url = f"{base_url}/spellcheck?delay=1"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 201

    def test_spellcheck_delay_error(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/bad.txt"

        url = f"{base_url}/spellcheck?delay=122"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 422

    def test_sentiment_delay_error(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/bad.txt"

        url = f"{base_url}/sentiment?delay=122"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 422

    def test_sentiment_four_hundred(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/no_data.txt"

        url = f"{base_url}/sentiment"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 400

    def test_sentiment(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/negative_sent.txt"

        url = f"{base_url}/sentiment?delay=1"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 201
