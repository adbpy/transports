"""
    test_exceptions
    ~~~~~~~~~~~~~~~

    Tests for the :mod:`~adbts.ctxlib` module.
"""
import tempfile

import pytest

from adbts import ctxlib


def test_close_on_error_closes_on_exception():
    """
    Assert that :func:`~ctxlib.close_on_error` closes the given object if the block
    raises an exception.
    """
    obj = tempfile.TemporaryFile()
    with pytest.raises(RuntimeError):
        with ctxlib.close_on_error(obj):
            raise RuntimeError()
    assert obj.closed


def test_close_on_error_does_not_close_without_exception():
    """
    Assert that :func:`~ctxlib.close_on_error` does not try and close the object
    if no exception is raised.
    """
    obj = tempfile.TemporaryFile()
    with ctxlib.close_on_error(obj):
        pass
    assert not obj.closed
