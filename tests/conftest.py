"""
    conftest
    ~~~~~~~~

    High level fixtures used across multiple test modules.
"""
import os
import pytest
import random


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


@pytest.fixture(scope='function', params=[
    1,
    12,
    24,
    42,
    2048
])
def valid_num_bytes(request):
    """
    Fixture that yields valid 'num_bytes' values for transport read calls.
    """
    return request.param


@pytest.fixture(scope='function')
def valid_bytes():
    """
    Fixture that yields valid collections of bytes to write to a transport.
    """
    return os.urandom(random.randint(1, 1024))
