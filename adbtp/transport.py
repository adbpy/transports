"""
    adbtp.transport
    ~~~~~~~~~~~~~~~

    Defines abstract base class that all transports must implement.
"""
import abc
import typing

from . import hints

__all__ = ['Transport']


#: Sentinel object used to indicate when a timeout value was actually passed
#: since `None` is a valid type.
TIMEOUT_SENTINEL = object()


def transport_timeout(value, sentinel=TIMEOUT_SENTINEL, default=None, seconds=False):
    """
    Determine the timeout value in milliseconds to use for a transport operation.

    :param value: Timeout value given
    :type: value: :class:`~int`, :class:`~NoneType`, or :class:`~object`
    :param sentinel: Sentinel value that indicates nothing was passed
    :type sentinel: :class:`~object`
    :param default: Default value to use when value is the sentinel
    :type default: :class:`~int`, :class:`~NoneType`
    :param seconds: Flag indicating if the timeout should be in seconds
    :type seconds: :class:`~bool`
    :return: Operation timeout in milliseconds
    :rtype: :class:`~int`
    """
    value = value if value is not sentinel else default
    if seconds and isinstance(value, int):
        value //= 1000
    return value


#: Type hint that represents a series of bytes generated from a synchronous or asynchronous transport.
TransportReadResult = typing.Union[hints.Buffer, hints.BufferGenerator]  # pylint: disable=invalid-name


#: Type hint that represents an empty result from a synchronous or asynchronous transport.
TransportWriteResult = typing.Union[None, hints.NoneGenerator]  # pylint: disable=invalid-name


class Transport(metaclass=abc.ABCMeta):
    """
    Abstract class that defines a communication transport.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return '<{}({!r})>'.format(self.__class__.__name__, str(self))

    @property
    @abc.abstractmethod
    def closed(self):
        """
        Checks to see if the transport is closed.

        :return: Closed state of the transport
        :rtype: :class:`~bool`
        """

    @abc.abstractmethod
    def read(self, num_bytes: hints.Int, timeout: hints.Timeout=TIMEOUT_SENTINEL) -> TransportReadResult:
        """
        Read bytes from the transport.

        :param num_bytes: Number of bytes to read
        :type num_bytes: :class:`~int`
        :param timeout: Maximum number of milliseconds to read before raising an exception
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return: Collection of bytes read
        :rtype: :class:`~bytes` or :class:`~bytearray`
        :raises :class:`~adbtp.exceptions.TransportProtocolError`: When underlying transport encounters an error
        :raises :class:`~adbtp.exceptions.TimeoutError`: When timeout is exceeded
        """

    @abc.abstractmethod
    def write(self, data: hints.Buffer, timeout: hints.Timeout=TIMEOUT_SENTINEL) -> TransportWriteResult:
        """
        Write bytes to the transport.

        :param data: Collection of bytes to write
        :type data: :class:`~bytes` or :class:`~bytearray`
        :param timeout: Maximum number of milliseconds to write before raising an exception
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return Nothing
        :rtype: :class:`~NoneType`
        :raises :class:`~adbtp.exceptions.TransportProtocolError`: When underlying transport encounters an error
        :raises :class:`~adbtp.exceptions.TimeoutError`: When timeout is exceeded
        """

    @abc.abstractmethod
    def close(self) -> None:
        """
        Close the transport.

        :return: Nothing
        :rtype: :class:`~NoneType`
        :raises :class:`~adbtp.exceptions.TransportProtocolError`: When underlying transport encounters an error
        """


#: Type hint that represents a new instance created from a synchronous or asynchronous transport.
# pylint: disable=invalid-name,unsubscriptable-object
TransportOpenResult = typing.Union[Transport, typing.Generator[typing.Any, None, Transport]]
