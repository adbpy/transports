"""
    test_exceptions
    ~~~~~~~~~~~~~~~

    Tests for the :mod:`~adbts.exceptions` module.
"""
import pytest

from adbts import exceptions


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


def test_reraise_converts_exception_to_transport_error(exc_to_catch):
    """
    Assert that :func:`~adbts.exceptions.reraise` wraps functions that raise stdlib exceptions
    and reraises them as :class:`~adbts.exceptions.TransportError`.
    """
    @exceptions.reraise(exc_to_catch)
    def func():
        raise exc_to_catch()

    with pytest.raises(exceptions.TransportError):
        func()


def test_reraise_timeout_errors_converts_exception_to_transport_timeout_error(exc_to_catch):
    """
    Assert that :func:`~adbts.exceptions.reraise_timeout_errors` wraps functions that raise stdlib exceptions
    and reraises them as :class:`~adbts.exceptions.TransportTimeoutError`.
    """
    @exceptions.reraise_timeout_errors(exc_to_catch)
    def func():
        raise exc_to_catch()

    with pytest.raises(exceptions.TransportTimeoutError):
        func()
