"""
    adbtp.usb
    ~~~~~~~~~

    Package that contains Universal Serial Bus (USB) transports.
"""
import functools

from .. import transport


#: Function partial that sets the default USB transport operation timeout to zero milliseconds.
transport_timeout = functools.partial(transport.transport_timeout, default=0)  # pylint: disable=invalid-name


from . import async, sync  # noqa pylint: disable=wrong-import-position

__all__ = ['sync', 'async']
