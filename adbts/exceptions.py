"""
    adbts.exceptions
    ~~~~~~~~~~~~~~~~

    Contains exception types used across the package.
"""
import functools
import typing

#: Type hint that defines a exception type that derives from :class:`~Exception`.
ExceptionType = typing.TypeVar('ExceptionType', bound=Exception)  # pylint: disable=invalid-name

#: Type hint that defines a collection of one or more exception types
#: that can be caught/raised.
ExceptionTypes = typing.Union[ExceptionType,  # pylint: disable=invalid-name
                              typing.Tuple[ExceptionType, ...]]  # pylint: disable=invalid-sequence-index


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


def reraise(exc_to_catch: ExceptionTypes):
    """
    Decorator that catches specific exception types and re-raises them as
    :class:`~adbts.exceptions.TransportError`.

    :param exc_to_catch: Transport specific timeout exception type(s) to catch
    :type exc_to_catch: :class:`~Exception` or :class:`~tuple`
    """
    def decorator(func):  # pylint: disable=missing-docstring
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # pylint: disable=missing-docstring
            try:
                return func(*args, **kwargs)
            except exc_to_catch as ex:
                raise TransportError('Transport encountered an error') from ex
        return wrapper
    return decorator


def reraise_timeout_errors(exc_to_catch: ExceptionTypes):
    """
    Decorator that catches transport specific timeout related exceptions to re-raise another.

    :param exc_to_catch: Transport specific timeout exception type(s) to catch
    :type exc_to_catch: :class:`~Exception` or :class:`~tuple`
    """
    def decorator(func):  # pylint: disable=missing-docstring
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # pylint: disable=missing-docstring
            try:
                return func(*args, **kwargs)
            except exc_to_catch as ex:
                raise TransportTimeoutError(
                    'Exceeded timeout of {} ms'.format(kwargs.get('timeout', 'inf'))) from ex
        return wrapper
    return decorator
