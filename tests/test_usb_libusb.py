"""
    test_usb_libusb
    ~~~~~~~~~~~~~~~

    Tests for the :mod:`~adbtp.usb.libusb` module.
"""
import pytest
import usb1

from adbtp import exceptions
from adbtp.usb import libusb


@pytest.fixture(scope='session', params=[
    (usb1.ERROR_NO_DEVICE, exceptions.TransportEndpointNotFound),
    (usb1.ERROR_ACCESS, exceptions.TransportAccessDenied),
    (usb1.ERROR_TIMEOUT, exceptions.TransportTimeoutError),
    (usb1.ERROR_INVALID_PARAM, exceptions.TransportProtocolError),
    (usb1.ERROR_OTHER, exceptions.TransportProtocolError),
    (usb1.ERROR_BUSY, exceptions.TransportProtocolError),
    (usb1.ERROR_NOT_SUPPORTED, exceptions.TransportProtocolError),
    (usb1.ERROR_NO_MEM, exceptions.TransportProtocolError),
    (usb1.ERROR_PIPE, exceptions.TransportProtocolError),
    (usb1.ERROR_INTERRUPTED, exceptions.TransportProtocolError),
    (usb1.ERROR_OVERFLOW, exceptions.TransportProtocolError),
    (usb1.ERROR_IO, exceptions.TransportProtocolError),
    (usb1.ERROR_NOT_FOUND, exceptions.TransportProtocolError),
])
def error_code_to_exception(request):
    """
    Fixture that yields tuple containing libusb error code integer and the corresponding transport related
    exception that will be reraised when caught.
    """
    return request.param


def test_reraise_libusb_errors_handles_no_device(error_code_to_exception):
    """
    Assert that functions decorated with :func:`~adbtp.usb.libusb.reraise_libusb_errors` raise
    the expected exception type based on the libusb error code.
    """
    value, exc_type = error_code_to_exception

    @libusb.reraise_libusb_errors
    def func():
        raise usb1.USBError(value)

    with pytest.raises(exc_type):
        func()
