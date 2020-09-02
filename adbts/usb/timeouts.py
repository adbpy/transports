"""
    adbts.usb.timeouts
    ~~~~~~~~~~~~~~~~~~

    Contains timeouts for USB transports.
"""
from .. import hints, timeouts

# Exports from wrapped timeouts module so caller doesn't need to import both.
UNDEFINED = timeouts.UNDEFINED


def timeout(value: hints.Timeout) -> hints.Int:
    """
    Determine the timeout value in milliseconds to use for a USB transport operation.

    :param value: Timeout value given
    :type value: :class:`~int`, :class:`~float`, :class:`~NoneType`
    :return: Operation timeout in milliseconds
    :rtype: :class:`~int`
    """
    if value is None or value == UNDEFINED:
        return 0
    return int(value)
