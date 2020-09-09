"""
    adbts.tcp.asynchronous
    ~~~~~~~~~~~~~~~~~~~~~~

    Contains functionality for asynchronous Transmission Control Protocol (TCP) transport using `asyncio`.
"""
import asyncio

from .. import exceptions, hints, transport
from . import timeouts

__all__ = ['Transport']


# Disable incorrect warning on asyncio.wait_for, https://github.com/PyCQA/pylint/issues/996.
# pylint: disable=not-an-iterable

class Transport(transport.Transport):
    """
    Defines asynchronous (non-blocking) TCP transport using `asyncio`.
    """

    def __init__(self,
                 host: hints.Str,
                 port: hints.Int,
                 reader: hints.StreamReader,
                 writer: hints.StreamWriter,
                 loop: hints.OptionalEventLoop = None) -> None:
        self._host = host
        self._port = port
        self._reader = reader
        self._writer = writer
        self._loop = loop
        self._closed = False

    def __repr__(self) -> hints.Str:
        address = str(self)
        state = 'closed' if self.closed else 'open'
        return '<{}(address={!r}, state={!r})>'.format(self.__class__.__name__, address, state)

    def __str__(self) -> hints.Str:
        return '{}:{}'.format(self._host, self._port)

    @property
    def closed(self) -> hints.Bool:
        """
        Checks to see if the transport is closed.

        :return: Closed state of the transport
        :rtype: :class:`~bool`
        """
        return self._closed is True

    @asyncio.coroutine
    @transport.ensure_opened
    @transport.ensure_num_bytes
    @exceptions.reraise(OSError)
    @exceptions.reraise_timeout_errors(asyncio.TimeoutError)
    def read(self,
             num_bytes: hints.Int,
             timeout: hints.Timeout = timeouts.UNDEFINED) -> transport.TransportReadResult:
        """
        Read bytes from the transport.

        :param num_bytes: Number of bytes to read.
        :type num_bytes: :class:`~int`
        :param timeout: Maximum number of milliseconds to read before raising an exception.
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return: Collection of bytes read
        :rtype: :class:`~bytes` or :class:`~bytearray`
        :raises :class:`~adbts.exceptions.TransportError`: When underlying transport encounters an error
        :raises :class:`~adbts.exceptions.TimeoutError`: When timeout is exceeded
        """
        data = yield from asyncio.wait_for(self._reader.read(num_bytes),
                                           timeout=timeouts.timeout(timeout),
                                           loop=self._loop)
        return data

    @asyncio.coroutine
    @transport.ensure_opened
    @transport.ensure_data
    @exceptions.reraise(OSError)
    @exceptions.reraise_timeout_errors(asyncio.TimeoutError)
    def write(self,
              data: hints.Buffer,
              timeout: hints.Timeout = timeouts.UNDEFINED) -> transport.TransportWriteResult:
        """
        Write bytes to the transport.

        :param data: Collection of bytes to write.
        :type data: :class:`~bytes` or :class:`~bytearray`
        :param timeout: Maximum number of milliseconds to write before raising an exception.
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return Nothing
        :return: :class:`~NoneType`
        :raises :class:`~adbts.exceptions.TransportError`: When underlying transport encounters an error.
        :raises :class:`~adbts.exceptions.TimeoutError`: When timeout is exceeded
        """
        self._writer.write(data)
        yield from asyncio.wait_for(self._writer.drain(), timeout=timeouts.timeout(timeout), loop=self._loop)

    @transport.ensure_opened
    @exceptions.reraise(OSError)
    def close(self) -> None:
        """
        Close the transport.

        :return: Nothing
        :rtype: `None`
        :raises :class:`~adbts.exceptions.TransportError`: When underlying transport encounters an error
        """
        self._writer.close()
        self._closed = True


@asyncio.coroutine
@exceptions.reraise(OSError)
def open(host: hints.Str,  # pylint: disable=redefined-builtin
         port: hints.Int,
         timeout: hints.Timeout = timeouts.UNDEFINED,
         loop: hints.OptionalEventLoop = None) -> transport.TransportOpenResult:
    """
    Open a new :class:`~adbts.tcp.async.Transport` transport to the given host/port.

    :param host: Remote host
    :type host: :class:`~str`
    :param port: Remote port
    :type port: :class:`~int`
    :param timeout: Maximum number of milliseconds to write before raising an exception.
    :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
    :param loop: Asyncio Event Loop
    :type loop: :class:`~asyncio.events.AbstractEventLoop`
    :return: Asynchronous TCP transport
    :rtype: :class:`~adbts.tcp.async.Transport`
    :raises :class:`~adbts.exceptions.TransportError`: When underlying transport encounters an error
    """
    reader, writer = yield from asyncio.wait_for(asyncio.open_connection(host, port, loop=loop),
                                                 timeout=timeouts.timeout(timeout), loop=loop)
    return Transport(host, port, reader, writer, loop)
