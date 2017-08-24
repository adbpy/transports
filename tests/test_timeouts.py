"""
    test_timeouts
    ~~~~~~~~~~~~~

    Tests for the :mod:`~adbts.timeouts` module.
"""
import pytest

from adbts import timeouts


@pytest.fixture(scope='session', params=[
    None,
    500,
    1000,
    2000,
    5000,
    10000
])
def default(request):
    """
    Fixture that yields default timeout values.
    """
    return request.param


@pytest.fixture(scope='session', params=[
    None,
    timeouts.SENTINEL
])
def sentinel(request):
    """
    Fixture that yields timeout sentinel values.
    """
    return request.param


def test_transport_timeout_returns_default_on_sentinel(sentinel, default):
    """
    Assert that :func:`~adbts.timeouts.timeout` returns the default value when given
    the timeout sentinel value.
    """
    assert timeouts.timeout(sentinel, sentinel=sentinel, default=default) == default


def test_transport_timeout_converts_milliseconds_to_seconds_when_flag_set(valid_timeout_ms):
    """
    Assert that :func:`~adbts.timeouts.timeout` returns the timeout value in seconds
    when the parameter is set.
    """
    assert timeouts.timeout(valid_timeout_ms, seconds=True) == valid_timeout_ms // 1000


def test_transport_timeout_returns_none_when_none_and_seconds_set():
    """
    Assert that :func:`~adbts.timeouts.timeout` returns `None` when given a `None` timeout
    value and the seconds flag set.
    """
    assert timeouts.timeout(None, seconds=True) is None