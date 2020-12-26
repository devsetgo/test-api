import pytest

from app.settings import Settings


@pytest.fixture
def settings_override():
    return Settings(app_version="0.0.1")

