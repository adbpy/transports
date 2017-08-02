"""
    test_usb_sync
    ~~~~~~~~~~~~~

    Tests for the :mod:`~adbtp.usb.sync` module.
"""
import pytest

from adbtp import exceptions, usb


def test_open_raises_when_no_device_found(mock_context_no_devices):
    """
    Assert that :func:`~adbtp.usb.sync.open` raises a :class:`~adbtp.exceptions.TransportEndpointNotFound`
    exception when no matching device is found.
    """
    with pytest.raises(exceptions.TransportEndpointNotFound):
        usb.sync.open()


def test_open_closes_context_when_no_device_found(mock_context_no_devices):
    """
    Assert that :func:`~adbtp.usb.sync.open` will close the USB context it creates when it cannot
    find a suitable device to use.
    """
    with pytest.raises(exceptions.TransportEndpointNotFound):
        usb.sync.open()
    mock_context_no_devices.close.assert_called_with()


def test_open_raises_when_no_read_endpoint_found(mock_context_one_device_match):
    """
    Assert that :func:`~adbtp.usb.sync.open` raises a :class:`~adbtp.exceptions.TransportProtocolError`
    exception when unable to find a read endpoint on the USB device.
    """
    with pytest.raises(exceptions.TransportProtocolError):
        usb.sync.open()


def test_open_closes_context_when_no_read_endpoint_found(mock_context_one_device_match):
    """
    Assert that :func:`~adbtp.usb.sync.open` will close the USB context it creates when it cannot
    find a read endpoint on the USB device.
    """
    with pytest.raises(exceptions.TransportProtocolError):
        usb.sync.open()
    mock_context_one_device_match.close.assert_called_with()


def test_open_raises_when_no_write_endpoint_found(mock_context_one_device_read_endpoint_no_write):
    """
    Assert that :func:`~adbtp.usb.sync.open` raises a :class:`~adbtp.exceptions.TransportProtocolError`
    exception when unable to find a write endpoint on the USB device.
    """
    with pytest.raises(exceptions.TransportProtocolError):
        usb.sync.open()


def test_open_closes_context_when_no_write_endpoint_found(mock_context_one_device_read_endpoint_no_write):
    """
    Assert that :func:`~adbtp.usb.sync.open` will close the USB context it creates when it cannot
    find a write endpoint on the USB device.
    """
    with pytest.raises(exceptions.TransportProtocolError):
        usb.sync.open()
    mock_context_one_device_read_endpoint_no_write.close.assert_called_with()


def test_open_opens_device_handle(mock_context_one_device_valid_endpoints, mock_device):
    """
    Assert that :func:`~adbtp.usb.sync.open` will open a device handle on the selected device.
    """
    usb.sync.open()
    mock_device.open.assert_called_with()
