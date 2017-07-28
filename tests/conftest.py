"""
    conftest
    ~~~~~~~~

    High level fixtures used across multiple test modules.
"""
import pytest


@pytest.fixture(scope='session', params=[
    500,
    1000,
    2000,
    5000,
    10000
])
def valid_timeout_ms(request):
    """
    Fixture that yields valid timeout values in milliseconds.
    """
    return request.param
