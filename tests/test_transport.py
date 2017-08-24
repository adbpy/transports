"""
    test_transport
    ~~~~~~~~~~~~~~

    Tests for the :mod:`~adbts.transport` module.
"""
import pytest

from adbts import transport


def test_transport_is_abstract():
    """
    Assert that :class:`~adbts.transport.Transport` is an abstract class.
    """
    with pytest.raises(TypeError):
        transport.Transport()
