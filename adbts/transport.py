"""
    adbts.transport
    ~~~~~~~~~~~~~~~

    Defines abstract base class that all transports must implement.
"""
import abc
import typing

from . import hints, timeouts

__all__ = ['Transport']


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
    def read(self, num_bytes: hints.Int, timeout: hints.Timeout=timeouts.SENTINEL) -> TransportReadResult:
        """
        Read bytes from the transport.

        :param num_bytes: Number of bytes to read
        :type num_bytes: :class:`~int`
        :param timeout: Maximum number of milliseconds to read before raising an exception
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return: Collection of bytes read
        :rtype: :class:`~bytes` or :class:`~bytearray`
        :raises :class:`~adbts.exceptions.TransportProtocolError`: When underlying transport encounters an error
        :raises :class:`~adbts.exceptions.TimeoutError`: When timeout is exceeded
        """

    @abc.abstractmethod
    def write(self, data: hints.Buffer, timeout: hints.Timeout=timeouts.SENTINEL) -> TransportWriteResult:
        """
        Write bytes to the transport.

        :param data: Collection of bytes to write
        :type data: :class:`~bytes` or :class:`~bytearray`
        :param timeout: Maximum number of milliseconds to write before raising an exception
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return Nothing
        :rtype: :class:`~NoneType`
        :raises :class:`~adbts.exceptions.TransportProtocolError`: When underlying transport encounters an error
        :raises :class:`~adbts.exceptions.TimeoutError`: When timeout is exceeded
        """

    @abc.abstractmethod
    def close(self) -> None:
        """
        Close the transport.

        :return: Nothing
        :rtype: :class:`~NoneType`
        :raises :class:`~adbts.exceptions.TransportProtocolError`: When underlying transport encounters an error
        """


#: Type hint that represents a new instance created from a synchronous or asynchronous transport.
# pylint: disable=invalid-name,unsubscriptable-object
TransportOpenResult = typing.Union[Transport, typing.Generator[typing.Any, None, Transport]]
