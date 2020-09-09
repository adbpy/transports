"""
    adbts.ctxlib
    ~~~~~~~~~~~~

    Contains functionality for dealing with context managers.
"""
import contextlib

from . import hints


@contextlib.contextmanager
def close_on_error(obj: hints.Closeable) -> hints.Iterator[hints.Closeable]:
    """
    Context manager that closes the given object if the block raises an exception.

    :param obj: Object that can be closed
    :raises Exception: When block raises an exception.
    """
    try:
        yield obj
    except Exception:
        obj.close()
        raise
