# -*- coding: utf-8 -*-
import pytest

from src.settings import Settings


@pytest.fixture
def settings_override():
    return Settings(app_version="0.0.1")
