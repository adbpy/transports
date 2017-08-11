"""
    test_transport
    ~~~~~~~~~~~~~~

    Tests for the :mod:`~adbtp.transport` module.
"""
import pytest

from adbtp import transport


def test_transport_is_abstract():
    """
    Assert that :class:`~adbtp.transport.Transport` is an abstract class.
    """
    with pytest.raises(TypeError):
        transport.Transport()
