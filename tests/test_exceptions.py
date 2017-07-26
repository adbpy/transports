"""
    test_exceptions
    ~~~~~~~~~~~~~~~

    Tests for the :mod:`~adbtp.exceptions` module.
"""
import pytest

from adbtp import exceptions


@pytest.fixture(scope='session', params=[
    RuntimeError,
    SystemError,
    OSError,
    Exception,
    BufferError,
    ConnectionError
])
def exc_to_catch(request):
    """
    Fixture that yields exception types that should be caught and reraised as transport
    specific exceptions.
    """
    return request.param


def test_reraise_converts_exception_to_transport_protocol_error(exc_to_catch):
    """
    Assert that :func:`~adbtp.exceptions.reraise` wraps functions that raise stdlib exceptions
    and reraises them as :class:`~adbtp.exceptions.TransportProtocolError`.
    """
    @exceptions.reraise(exc_to_catch)
    def func():
        raise exc_to_catch()

    with pytest.raises(exceptions.TransportProtocolError):
        func()


def test_reraise_timeout_errors_converts_exception_to_transport_timeout_error(exc_to_catch):
    """
    Assert that :func:`~adbtp.exceptions.reraise_timeout_errors` wraps functions that raise stdlib exceptions
    and reraises them as :class:`~adbtp.exceptions.TransportTimeoutError`.
    """
    @exceptions.reraise_timeout_errors(exc_to_catch)
    def func():
        raise exc_to_catch()

    with pytest.raises(exceptions.TransportTimeoutError):
        func()
