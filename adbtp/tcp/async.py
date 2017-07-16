"""
    adbtp.tcp.async
    ~~~~~~~~~~~~~~~

    Contains functionality for asynchronous Transmission Control Protocol (TCP) transport using `asyncio`.
"""
import asyncio

from . import transport_timeout
from .. import exceptions, hints, transport

__all__ = ['Transport']


# Disable incorrect warning on asyncio.wait_for, https://github.com/PyCQA/pylint/issues/996.
# pylint: disable=not-an-iterable

class Transport(transport.Transport):
    """
    Defines asynchronous (non-blocking) TCP transport using `asyncio`.
    """

    def __init__(self, host: hints.Str, port: hints.Int, reader: hints.StreamReader,
                 writer: hints.StreamWriter, loop: hints.EventLoop) -> None:
        self._host = host
        self._port = port
        self._reader = reader
        self._writer = writer
        self._loop = loop

    @property
    def closed(self):
        """
        Checks to see if the transport is closed.

        :return: Closed state of the transport
        :rtype: :class:`~bool`
        """
        return self._reader is None or self._writer is None

    @asyncio.coroutine
    @exceptions.reraise(OSError)
    @exceptions.reraise_timeout_errors(asyncio.TimeoutError)
    def read(self, num_bytes: hints.Int,
             timeout: hints.Timeout=transport.TIMEOUT_SENTINEL) -> transport.TransportReadResult:
        """
        Read bytes from the transport.

        :param num_bytes: Number of bytes to read.
        :type num_bytes: :class:`~int`
        :param timeout: Maximum number of milliseconds to read before raising an exception.
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return: Collection of bytes read
        :rtype: :class:`~bytes` or :class:`~bytearray`
        :raises :class:`~adbtp.exceptions.TransportProtocolError`: When underlying transport encounters an error
        :raises :class:`~adbtp.exceptions.TimeoutError`: When timeout is exceeded
        """
        data = yield from asyncio.wait_for(self._reader.read(num_bytes),
                                           timeout=transport_timeout(timeout),
                                           loop=self._loop)
        return data

    @asyncio.coroutine
    @exceptions.reraise(OSError)
    @exceptions.reraise_timeout_errors(asyncio.TimeoutError)
    def write(self, data: hints.Buffer,
              timeout: hints.Timeout=transport.TIMEOUT_SENTINEL) -> transport.TransportWriteResult:
        """
        Write bytes to the transport.

        :param data: Collection of bytes to write.
        :type data: :class:`~bytes` or :class:`~bytearray`
        :param timeout: Maximum number of milliseconds to write before raising an exception.
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return Number of bytes written
        :return: :class:`~int`
        :raises :class:`~adbtp.exceptions.TransportProtocolError`: When underlying transport encounters an error.
        :raises :class:`~adbtp.exceptions.TimeoutError`: When timeout is exceeded
        """
        self._writer.write(data)
        yield from asyncio.wait_for(self._writer.drain(), timeout=transport_timeout(timeout), loop=self._loop)
        return None

    @exceptions.reraise(OSError)
    def close(self) -> None:
        """
        Close the transport.

        :return: Nothing
        :rtype: `None`
        :raises :class:`~adbtp.exceptions.TransportProtocolError`: When underlying transport encounters an error
        """
        self._writer.close()
        self._writer = None
        self._reader = None


@asyncio.coroutine
@exceptions.reraise(OSError)
def open(host: hints.Str, port: hints.Int,  # pylint: disable=redefined-builtin
         timeout: hints.Timeout=transport.TIMEOUT_SENTINEL,
         loop: hints.EventLoop=None) -> transport.TransportOpenResult:
    """
    Open a new :class:`~adbtp.tcp.async.Transport` transport to the given host/port.

    :param host: Remote host
    :type host: :class:`~str`
    :param port: Remote port
    :type port: :class:`~int`
    :param timeout: Maximum number of milliseconds to write before raising an exception.
    :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
    :param loop: Asyncio Event Loop
    :type loop: :class:`~asyncio.events.AbstractEventLoop`
    :return: Asynchronous TCP transport
    :rtype: :class:`~adbtp.tcp.async.Transport`
    :raises :class:`~adbtp.exceptions.TransportProtocolError`: When underlying transport encounters an error
    """
    reader, writer = yield from asyncio.wait_for(asyncio.open_connection(host, port, loop=loop),
                                                 timeout=transport_timeout(timeout), loop=loop)
    return Transport(host, port, reader, writer, loop)
