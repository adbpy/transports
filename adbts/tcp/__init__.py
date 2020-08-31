"""
    adbts.tcp
    ~~~~~~~~~

    Package that contains Transmission Control Protocol (TCP) transports.
"""
import functools
import socket

from .. import timeouts

#: Function partial that sets the default transport operation timeout to the
#: default socket timeout value and convert it from seconds to milliseconds.
tcp_timeout = functools.partial(timeouts.timeout,  # pylint: disable=invalid-name
                                default=socket.getdefaulttimeout(),
                                seconds=True)


from . import asynchronous, synchronous  # noqa pylint: disable=wrong-import-position

__all__ = ['asynchronous', 'synchronous']
