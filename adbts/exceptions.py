"""
    adbts.exceptions
    ~~~~~~~~~~~~~~~~

    Contains exception types used across the package.
"""
import functools

from . import hints

__all__ = ['TransportError', 'TransportTimeoutError', 'TransportClosedError',
           'TransportEndpointNotFound', 'TransportAccessDenied']


class TransportError(Exception):
    """
    Base exception for all transport related errors.
    """


class TransportTimeoutError(TransportError):
    """
    Exception raised when a transport action exceeds the specified timeout.
    """


class TransportClosedError(TransportError):
    """
    Exception raised when attempting to perform an action of a closed transport.
    """


class TransportEndpointNotFound(TransportError):
    """
    Exception raised when the transport endpoint (peer) cannot be found or was disconnected.
    """


class TransportAccessDenied(TransportError):
    """
    Exception raised when caller has insufficient permissions to perform an action.
    """


# pylint: disable=missing-docstring
def reraise(exc_to_catch: hints.ExceptionTypes[hints.ExceptionType]) -> hints.DecoratorArgsReturnValue:
    """
    Decorator that catches specific exception types and re-raises them as
    :class:`~adbts.exceptions.TransportError`.

    :param exc_to_catch: Transport specific timeout exception type(s) to catch
    :type exc_to_catch: :class:`~Exception` or :class:`~tuple`
    """
    def decorator(func: hints.DecoratorFunc) -> hints.DecoratorReturnValue:
        @functools.wraps(func)
        def wrapper(*args: hints.Args, **kwargs: hints.Kwargs) -> hints.DecoratorReturnValue:
            try:
                return func(*args, **kwargs)
            except exc_to_catch as ex:
                raise TransportError('Transport encountered an error') from ex
        return wrapper
    return decorator


def reraise_timeout_errors(exc_to_catch: hints.ExceptionTypes[hints.ExceptionType]) -> hints.DecoratorArgsReturnValue:
    """
    Decorator that catches transport specific timeout related exceptions to re-raise another.

    :param exc_to_catch: Transport specific timeout exception type(s) to catch
    :type exc_to_catch: :class:`~Exception` or :class:`~tuple`
    """
    def decorator(func: hints.DecoratorFunc) -> hints.DecoratorReturnValue:
        @functools.wraps(func)
        def wrapper(*args: hints.Args, **kwargs: hints.Kwargs) -> hints.DecoratorReturnValue:
            try:
                return func(*args, **kwargs)
            except exc_to_catch as ex:
                raise TransportTimeoutError(
                    'Exceeded timeout of {} ms'.format(kwargs.get('timeout', 'inf'))) from ex
        return wrapper
    return decorator
# pylint: enable=missing-docstring
