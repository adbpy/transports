"""
    adbtp.tcp
    ~~~~~~~~~

    Package that contains Transmission Control Protocol (TCP) transports.
"""
import functools
import socket

from .. import transport

#: Function partial that sets the default transport operation timeout to the
#: default socket timeout value and convert it from seconds to milliseconds.
transport_timeout = functools.partial(transport.transport_timeout,  # pylint: disable=invalid-name
                                      default=socket.getdefaulttimeout(),
                                      seconds=True)


from . import async, sync  # noqa pylint: disable=wrong-import-position

__all__ = ['sync', 'async']
