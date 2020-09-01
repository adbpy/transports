"""
    adbts.usb.timeouts
    ~~~~~~~~~~~~~~~~~~

    Contains timeouts for USB transports.
"""
import functools

from .. import timeouts

#: Sentinel value indicating a timeout was not given. Equal to :attr:`~adbts.timeouts.UNDEFINED`.
UNDEFINED = timeouts.UNDEFINED

#: Function partial that sets the default USB transport operation timeout to zero milliseconds.
timeout = functools.partial(timeouts.timeout, default=0)  # pylint: disable=invalid-name
