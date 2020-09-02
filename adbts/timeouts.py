"""
    adbts.timeouts
    ~~~~~~~~~~~~~~

    Contains functionality for dealing with transport call timeouts.
"""
from . import hints

__all__ = ['UNDEFINED', 'timeout']

#: Sentinel object used to indicate when a timeout value was actually passed
#: since `None` is a valid type.
UNDEFINED = -1


def timeout(value: hints.Timeout,
            sentinel: hints.Timeout = UNDEFINED,
            default: hints.Timeout = None,
            seconds: hints.Bool = False) -> hints.Timeout:
    """
    Determine the timeout value in milliseconds to use for a transport operation.

    :param value: Timeout value given
    :type value: :class:`~int`, :class:`~float`, :class:`~NoneType`
    :param sentinel: Sentinel value that indicates nothing was passed
    :type sentinel: :class:`~object`
    :param default: Default value to use when value is the sentinel
    :type default: :class:`~int`, :class:`~float`, :class:`~NoneType`
    :param seconds: Flag indicating if the timeout should be in seconds
    :type seconds: :class:`~bool`
    :return: Operation timeout in milliseconds
    :rtype: :class:`~int`
    """
    value = value if value is not sentinel else default
    if seconds and isinstance(value, (int, float)):
        value //= 1000
    return value
