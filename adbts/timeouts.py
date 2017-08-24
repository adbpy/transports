"""
    adbts.timeouts
    ~~~~~~~~~~~~~~

    Contains functionality for dealing with transport call timeouts.
"""
#: Sentinel object used to indicate when a timeout value was actually passed
#: since `None` is a valid type.
SENTINEL = object()


def timeout(value, sentinel=SENTINEL, default=None, seconds=False):
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


class Timeout:
    """
    Class that represents and tracks a period of time.
    """

    def __init__(self, seconds):
        self._seconds = seconds
        self._start = None
        self._stop = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass


def wrap(_timeout=None):
    return Timeout(_timeout)


# with timeouts.milliseconds(1000) as timeout:
#    timeout.remaining_milliseconds
#    timeout.remaining_seconds



