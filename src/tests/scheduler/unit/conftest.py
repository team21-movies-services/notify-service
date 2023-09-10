from unittest.mock import Mock

import pytest


@pytest.fixture(name='celery_mock')
def celery_app():
    return Mock()
