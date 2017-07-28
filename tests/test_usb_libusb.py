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


@pytest.fixture(scope='session', params=[
    1,
    2,
    12,
    24,
])
def valid_endpoint_address(request):
    """
    Fixture that yields valid timeout values in milliseconds.
    """
    return request.param


@pytest.fixture(scope='session', params=[
    1,
    2,
    3,
    60,
    92
])
def valid_interface_number(request):
    """
    Fixture that yields valid interface numbers.
    """
    return request.param


@pytest.fixture(scope='function')
def mock_context(mocker):
    """
    Fixture that yields a mock USB context.
    """
    return mocker.MagicMock(usb1.USBContext, autospec=True)


@pytest.fixture(scope='function')
def mock_context_class(mocker, mock_context):
    """
    Fixture that yields nothing but patches :class:`~usb1.USBContext` to
    return a mocked context object on instantiation.
    """
    mocker.patch.object(usb1, 'USBContext', side_effect=lambda: mock_context)


@pytest.fixture(scope='function')
def mock_device(mocker):
    """
    Fixture that yields a mock USB device.
    """
    return mocker.MagicMock(usb1.USBDevice, autospec=True)


@pytest.fixture(scope='function')
def mock_handle(mocker):
    """
    Fixture that yields a mock USB device handle.
    """
    return mocker.MagicMock(usb1.USBDeviceHandle, autospec=True)


@pytest.fixture(scope='function')
def mock_read_handle(mocker, mock_handle):
    """
    Fixture that yields a mock USB device handle used for reading.
    """
    mock_handle.bulkRead = mocker.MagicMock(return_value=None)
    return mock_handle


@pytest.fixture(scope='function')
def mock_write_handle(mocker, mock_handle):
    """
    Fixture that yields a mock USB device handle used for writing.
    """
    mock_handle.bulkWrite = mocker.MagicMock(side_effect=lambda *args: len(args[1]))
    return mock_handle


@pytest.fixture(scope='function')
def mock_write_handle_incorrect_return_value(mocker, mock_handle):
    """
    Fixture that yields a mock USB device handle used for writing that yields back and incorrect
    number of bytes written.
    """
    mock_handle.bulkWrite = mocker.MagicMock(side_effect=lambda *args: len(args[1]) - 1)
    return mock_handle


@pytest.fixture(scope='function')
def mock_endpoint(mocker, valid_endpoint_address):
    """
    Fixture that yields a mock USB endpoint.
    """
    mock = mocker.MagicMock(usb1.USBEndpoint, autospec=True)
    mock.getAddress = mocker.MagicMock(return_value=valid_endpoint_address)
    return mock


@pytest.fixture(scope='function')
def mock_interface_settings(mocker, valid_interface_number):
    """
    Fixture that yields mock USB interface settings.
    """
    mock = mocker.MagicMock(usb1.USBInterfaceSetting, autospec=True)
    mock.getNumber = mocker.MagicMock(return_value=valid_interface_number)
    return mock


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


def test_read_performs_bulk_read_on_handle(mock_read_handle, mock_endpoint, valid_endpoint_address,
                                           valid_num_bytes, valid_timeout_ms):
    """
    Assert that :func:`~adbtp.usb.libusb.read` calls :meth:`~usb1.USBDeviceHandle.bulkRead` on the given
    handle using the endpoint address and other args.
    """
    libusb.read(mock_read_handle, mock_endpoint, valid_num_bytes, valid_timeout_ms)
    mock_read_handle.bulkRead.assert_called_with(valid_endpoint_address, valid_num_bytes, valid_timeout_ms)


def test_read_performs_bulk_read_against_endpoint_address(mock_read_handle, mock_endpoint,
                                                          valid_num_bytes, valid_timeout_ms):
    """
    Assert that :func:`~adbtp.usb.libusb.read` calls :meth:`~usb1.USBDeviceHandle.bulkRead` using the
    endpoint address.
    """
    libusb.read(mock_read_handle, mock_endpoint, valid_num_bytes, valid_timeout_ms)
    mock_endpoint.getAddress.assert_called_with()


def test_write_performs_bulk_write_on_handle(mock_write_handle, mock_endpoint, valid_endpoint_address,
                                             valid_bytes, valid_timeout_ms):
    """
    Assert that :func:`~adbtp.usb.libusb.write` calls :meth:`~usb1.USBDeviceHandle.bulkWrite` on the given
    handle using the endpoint address and other args.
    """
    libusb.write(mock_write_handle, mock_endpoint, valid_bytes, valid_timeout_ms)
    mock_write_handle.bulkWrite.assert_called_with(valid_endpoint_address, valid_bytes, valid_timeout_ms)


def test_write_performs_bulk_write_against_endpoint_address(mock_write_handle, mock_endpoint,
                                                            valid_bytes, valid_timeout_ms):
    """
    Assert that :func:`~adbtp.usb.libusb.write` calls :meth:`~usb1.USBDeviceHandle.bulkWrite` using the
    endpoint address.
    """
    libusb.read(mock_write_handle, mock_endpoint, valid_bytes, valid_timeout_ms)
    mock_endpoint.getAddress.assert_called_with()


def test_write_throws_error_when_not_all_bytes_written(mock_write_handle_incorrect_return_value, mock_endpoint,
                                                       valid_bytes, valid_timeout_ms):
    """
    Assert that :func:`~adbtp.usb.libusb.write` calls :meth:`~usb1.USBDeviceHandle.bulkWrite` on the given
    handle using the endpoint address and other args.
    """
    with pytest.raises(exceptions.TransportProtocolError):
        libusb.write(mock_write_handle_incorrect_return_value, mock_endpoint, valid_bytes, valid_timeout_ms)


def test_close_releases_handle_interface(mock_context, mock_handle, mock_interface_settings, valid_interface_number):
    """
    Assert that :func:`~adbtp.usb.libusb.close` calls :meth:`~usb1.USBDeviceHandle.releaseInterface`
    on the given handle using the interface settings number.
    """
    libusb.close(mock_context, mock_handle, mock_interface_settings)
    mock_handle.releaseInterface.assert_called_with(valid_interface_number)


def test_close_closes_handle(mock_context, mock_handle, mock_interface_settings):
    """
    Assert that :func:`~adbtp.usb.libusb.close` calls :meth:`~usb1.USBDeviceHandle.close`
    on the given handle.
    """
    libusb.close(mock_context, mock_handle, mock_interface_settings)
    mock_handle.close.assert_called_with()


def test_close_closes_context(mock_context, mock_handle, mock_interface_settings):
    """
    Assert that :func:`~adbtp.usb.libusb.close` calls :meth:`~usb1.USBContext.close`
    on the given context.
    """
    libusb.close(mock_context, mock_handle, mock_interface_settings)
    mock_context.close.assert_called_with()


def test_open_context_returns_new_context(mock_context_class, mock_context):
    """
    Assert that :func:`~adbtp.usb.libusb.open_context` returns a new :class:`~usb1.USBContext` instance
    by calling :meth:`~usb1.USBContext.open`.
    """
    libusb.open_context()
    mock_context.open.assert_called_with()


def test_open_device_handle_calls_open_on_device(mock_device):
    """
    Assert that :func:`~adbtp.usb.libusb.open_device_handle` creates a new :class:`~usb1.USBDeviceHandle`
    by calling :meth:`~usb1.USBDevice.open`.
    """
    libusb.open_device_handle(mock_device)
    mock_device.open.assert_called_with()
