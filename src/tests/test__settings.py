# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient
import pytest
from src import main
from src.settings import config_settings, Settings

client = TestClient(main.app)


def test_settings():
    assert config_settings.app_version == "1.2.3"
    assert config_settings.owner != None
    assert config_settings.website != None
    assert config_settings.license_type != None
    assert config_settings.license_link != None
    assert config_settings.create_sample_data != None
    assert config_settings.number_tasks != None
    assert config_settings.number_users != None
    assert config_settings.number_groups != None
    assert config_settings.host_domain != None
    assert config_settings.release_env != None
    assert config_settings.https_on != None
    assert config_settings.prometheus_on != None
    assert config_settings.add_default_group != None
    assert config_settings.sqlalchemy_database_uri != None
    assert config_settings.loguru_retention != None
    assert config_settings.loguru_rotation != None
    assert config_settings.workers != None
