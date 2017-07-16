"""
    adbtp.hints
    ~~~~~~~~~~~

    Contains type hint definitions used across modules in this package.
"""
import asyncio
import socket
import typing

# pylint: disable=invalid-name,no-member

#: Type hint that is an alias for the built-in :class:`~bool` type.
Bool = bool


#: Type hint that defines multiple types that can represent a collection of
#: bytes that can be used to create model types.
Buffer = typing.Union[bytes, bytearray]


#: Type hint that represents a coroutine that yields :class:`~bytes` or :class:`~bytearray`.
BufferGenerator = typing.Generator[typing.Any, None, Buffer]


#: Type hint that is an alias for the built-in :class:`~bytes` type.
Bytes = bytes


#: Type hint that is an alias for :class:`~typing.Callable`.
Callable = typing.Callable


#: Type that is an alias for :class:`~asyncio.events.AbstractEventLoop`.
EventLoop = asyncio.AbstractEventLoop


#: Type hint that defines a collection of one or more exception types
#: that can be caught/raised.
ExceptionType = typing.Type[Exception]
ExceptionTypes = typing.Union[ExceptionType, typing.Tuple[ExceptionType, ...]]


#: Type hint that is an alias for the built-in :class:`~int` type.
Int = int


#: Type hint that is an alias for :class:`~socket.socket`.
Socket = socket.socket


#: Type hint that is an alias for the built-in :class:`~str` type.
Str = str


#: Type hint that is an alias for :class:`~asyncio.streams.StreamReader`.
StreamReader = asyncio.StreamReader


#: Type hint that is an alias for :class:`~asyncio.streams.StreamWriter`.
StreamWriter = asyncio.StreamWriter


#: Type hint that defines an optional integer value that represents
#: a timeout value to a transport.
Timeout = typing.Optional[int]
