"""
    adbts.tcp.timeouts
    ~~~~~~~~~~~~~~~~~~

    Contains timeouts for TCP transports.
"""
import socket

from .. import hints, timeouts

# Exports from wrapped timeouts module so caller doesn't need to import both.
UNDEFINED = timeouts.UNDEFINED


def timeout(value: hints.Timeout) -> hints.OptionalFloat:
    """
    Determine the timeout value in seconds to use for a TCP transport operation.

    :param value: Timeout value given
    :type value: :class:`~int`, :class:`~float`, :class:`~NoneType`
    :return: Operation timeout in milliseconds
    :rtype: :class:`~float`
    """
    if value is None:
        return value
    if value == UNDEFINED:
        return socket.getdefaulttimeout()
    return float(value) // 1000
