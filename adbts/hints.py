"""
    adbts.hints
    ~~~~~~~~~~~

    Contains type hint definitions used across modules in this package.
"""
import asyncio
import socket
import typing

# pylint: disable=invalid-name,no-member,unsubscriptable-object

#: Type hint that is an alias for the built-in :class:`~bool` type.
Bool = bool


#: Type hint that defines multiple types that can represent a collection of
#: bytes that can be used to create model types.
Buffer = typing.Union[bytes, bytearray]


#: Type hint that represents a co-routine that yields :class:`~bytes` or :class:`~bytearray`.
BufferGenerator = typing.Generator[Buffer, None, None]


#: Type hint that is an alias for the built-in :class:`~bytes` type.
Bytes = bytes


#: Type hint that is an alias for :class:`~typing.Callable`.
Callable = typing.Callable


#: Type that is an alias for :class:`~asyncio.events.AbstractEventLoop`.
EventLoop = asyncio.AbstractEventLoop


#: Type that is an alias for an optional :class:`~asyncio.events.AbstractEventLoop`.
OptionalEventLoop = typing.Optional[asyncio.AbstractEventLoop]


#: Type hint that is an alias for the built-in :class:`~float` type.
Float = float


#: Type hint that is an alias for the built-in :class:`~int` type.
Int = int


#: Type hint that represents a co-routine that yields :class:`~NoneType`.
NoneGenerator = typing.Generator[None, None, None]


#: Type hint that is an alias for :class:`~socket.socket`.
Socket = socket.socket


#: Type hint that is an alias for the built-in :class:`~str` type.
Str = str


#: Type hint that is an alias for :class:`~asyncio.streams.StreamReader`.
StreamReader = asyncio.StreamReader


#: Type hint that is an alias for :class:`~asyncio.streams.StreamWriter`.
StreamWriter = asyncio.StreamWriter


#: Type hint that defines an optional value that represents a timeout value to a transport.
Timeout = typing.Union[int, float, None]


#: Type hint that represents an optional :class:`~hints.Float`.
OptionalFloat = typing.Optional[Float]


#: Type hint that represents an optional :class:`~hints.Int`.
OptionalInt = typing.Optional[Int]


#: Type hint that represents an optional :class:`~hints.Str`.
OptionalStr = typing.Optional[Str]


#: Type hint that is an alias for an optional :class:`~asyncio.streams.StreamReader`.
OptionalStreamReader = typing.Optional[asyncio.StreamReader]


#: Type hint that is an alias for an optional :class:`~asyncio.streams.StreamWriter`.
OptionalStreamWriter = typing.Optional[asyncio.StreamWriter]
