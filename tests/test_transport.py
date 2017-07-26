"""
    test_transport
    ~~~~~~~~~~~~~~

    Tests for the :mod:`~adbtp.transport` module.
"""
import pytest

from adbtp import transport


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
    transport.TIMEOUT_SENTINEL
])
def sentinel(request):
    """
    Fixture that yields timeout sentinel values.
    """
    return request.param


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


def test_transport_timeout_returns_default_on_sentinel(sentinel, default):
    """
    Assert that :func:`~adbtp.transport.transport_timeout` returns the default value when given
    the timeout sentinel value.
    """
    assert transport.transport_timeout(sentinel, sentinel=sentinel, default=default) == default


def test_transport_timeout_converts_milliseconds_to_seconds_when_flag_set(valid_timeout_ms):
    """
    Assert that :func:`~adbtp.transport.transport_timeout` returns the timeout value in seconds
    when the parameter is set.
    """
    assert transport.transport_timeout(valid_timeout_ms, seconds=True) == valid_timeout_ms // 1000


def test_transport_timeout_returns_none_when_none_and_seconds_set():
    """
    Assert that :func:`~adbtp.transport.transport_timeout` returns `None` when given a `None` timeout
    value and the seconds flag set.
    """
    assert transport.transport_timeout(None, seconds=True) is None


def test_transport_is_abstract():
    """
    Assert that :class:`~adbtp.transport.Transport` is an abstract class.
    """
    with pytest.raises(TypeError):
        transport.Transport()
