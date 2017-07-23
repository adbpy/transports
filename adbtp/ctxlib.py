"""
    adbtp.ctxlib
    ~~~~~~~~~~~~

    Contains functionality for dealing with context managers.
"""
import contextlib


@contextlib.contextmanager
def close_on_error(obj):
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

