# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient

from app import main
from app.settings import config

client = TestClient(main.app)

def test_settings():
    assert config.app_version != None
    assert config.owner != None
    assert config.website != None
    assert config.license_type != None
    assert config.license_link != None
    assert config.create_sample_data != None
    assert config.number_tasks != None
    assert config.number_users != None
    assert config.number_groups != None
    assert config.host_domain != None
    assert config.release_env != None
    assert config.https_on != None
    assert config.prometheus_on != None
    assert config.add_default_group != None
    assert config.sqlalchemy_database_uri != None
    assert config.loguru_retention != None
    assert config.loguru_rotation != None
    assert config.workers != None

