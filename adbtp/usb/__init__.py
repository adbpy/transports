"""
    adbtp.usb
    ~~~~~~~~~

    Package that contains Universal Serial Bus (USB) transports.
"""
import functools

from .. import timeouts


#: Function partial that sets the default USB transport operation timeout to zero milliseconds.
usb_timeout = functools.partial(timeouts.timeout, default=0)  # pylint: disable=invalid-name


from . import async, sync  # noqa pylint: disable=wrong-import-position

__all__ = ['sync', 'async']
