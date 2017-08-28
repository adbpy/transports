"""
    adbts.tcp.sync
    ~~~~~~~~~~~~~~

    Contains functionality for synchronous Transmission Control Protocol (TCP) transport.
"""
import contextlib
import socket

from . import tcp_timeout
from .. import exceptions, hints, timeouts, transport

__all__ = ['Transport']


@contextlib.contextmanager
def socket_timeout_scope(sock: hints.Socket, timeout: hints.Timeout=timeouts.SENTINEL):
    """
    Patches the socket timeout for the scope of the context manager.

    :param sock: Socket to set the timeout on
    :type sock: :class:`~socket.socket`
    :param timeout: Socket timeout in milliseconds
    :type timeout: :class:`~int`
    """
    current_timeout = sock.gettimeout()
    sock.settimeout(timeout)
    try:
        yield
    finally:
        sock.settimeout(current_timeout)


class Transport(transport.Transport):
    """
    Defines synchronous (blocking) TCP transport.

    .. note:: This transport is not thread-safe.
    """

    def __init__(self, host: hints.Str, port: hints.Int, sock: hints.Socket) -> None:
        self._host = host
        self._port = port
        self._socket = sock

    def __repr__(self):
        return '<{}(address={!r}, state={!r})>'.format(self.__class__.__name__, str(self),
                                                       'closed' if self.closed else 'open')

    def __str__(self):
        return '{}:{}'.format(self._host, self._port)

    @property
    def closed(self):
        """
        Checks to see if the transport is closed.

        :return: Closed state of the transport
        :rtype: :class:`~bool`
        """
        return self._socket is None or self._socket._closed  # pylint: disable=protected-access

    @transport.ensure_opened
    @transport.ensure_num_bytes
    @exceptions.reraise(OSError)
    @exceptions.reraise_timeout_errors(socket.timeout)
    def read(self, num_bytes: hints.Int,
             timeout: hints.Timeout=timeouts.SENTINEL) -> transport.TransportReadResult:
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
        with socket_timeout_scope(self._socket, tcp_timeout(timeout)):
            return self._socket.recv(num_bytes)

    @transport.ensure_opened
    @transport.ensure_data
    @exceptions.reraise(OSError)
    @exceptions.reraise_timeout_errors(socket.timeout)
    def write(self, data: hints.Buffer,
              timeout: hints.Timeout=timeouts.SENTINEL) -> transport.TransportWriteResult:
        """
        Write bytes to the transport.

        :param data: Collection of bytes to write.
        :type data: :class:`~bytes` or :class:`~bytearray`
        :param timeout: Maximum number of milliseconds to write before raising an exception.
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return Nothing
        :rtype: :class:`~NoneType`
        :raises :class:`~adbts.exceptions.TransportError`: When underlying transport encounters an error
        :raises :class:`~adbts.exceptions.TimeoutError`: When timeout is exceeded
        """
        with socket_timeout_scope(self._socket, tcp_timeout(timeout)):
            self._socket.sendall(data)
            return None

    @transport.ensure_opened
    @exceptions.reraise(OSError)
    def close(self) -> None:
        """
        Close the transport.

        :return: Nothing
        :rtype: `None`
        :raises :class:`~adbts.exceptions.TransportError`: When underlying transport encounters an error
        """
        self._socket.close()
        self._socket = None


@exceptions.reraise(OSError)
@exceptions.reraise_timeout_errors(socket.timeout)
def open(host: hints.Str, port: hints.Int,  # pylint: disable=redefined-builtin
         timeout: hints.Timeout=timeouts.SENTINEL) -> transport.TransportOpenResult:
    """
    Open a new :class:`~adbts.tcp.sync.Transport` transport to the given host/port.

    :param host: Remote host
    :type host: :class:`~str`
    :param port: Remote port
    :type port: :class:`~int`
    :param timeout: Maximum number of milliseconds on blocking socket operations before raising an exception
    :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
    :return: Synchronous TCP transport
    :rtype: :class:`~adbts.tcp.sync.Transport`
    :raises :class:`~adbts.exceptions.TransportError`: When underlying transport encounters an error
    :raises :class:`~adbts.exceptions.TimeoutError`: When timeout is exceeded
    """
    sock = socket.create_connection((host, port), tcp_timeout(timeout))
    return Transport(host, port, sock)
