"""
    adbts.tcp.timeouts
    ~~~~~~~~~~~~~~~~~~

    Contains timeouts for TCP transports.
"""
import functools
import socket

from .. import timeouts

#: Sentinel value indicating a timeout was not given. Equal to :attr:`~adbts.timeouts.UNDEFINED`.
UNDEFINED = timeouts.UNDEFINED

#: Function partial that sets the default transport operation timeout to the
#: default socket timeout value and convert it from seconds to milliseconds.
timeout = functools.partial(timeouts.timeout,  # pylint: disable=invalid-name
                            default=socket.getdefaulttimeout(),
                            seconds=True)
