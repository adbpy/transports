"""
    tests/usb/conftest
    ~~~~~~~~~~~~~~~~~~

    Contains fixtures used by usb/libusb test modules.
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
    Fixture that yields valid USB endpoint addresses.
    """
    return request.param


@pytest.fixture(scope='session', params=[
    128,
    129,
    212,
    255,
])
def valid_read_endpoint_address(request):
    """
    Fixture that yields valid USB endpoint addresses using for reading.
    """
    return request.param


@pytest.fixture(scope='session', params=[
    1,
    2,
    98,
    124,
])
def valid_write_endpoint_address(request):
    """
    Fixture that yields valid USB endpoint addresses using for writing.
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


@pytest.fixture(scope='session')
def valid_usb_device_class():
    """
    Fixture that yields a valid USB device class.
    """
    return libusb.USB_DEVICE_CLASS


@pytest.fixture(scope='session', params=[
    0x00,
    0x01,
    0x02,
    0x03,
    0x05,
    0x06,
    0x07,
    0x08,
    0x09,
    0xA,
    0xB,
    0xD,
    0xE,
    0xF,
    0x10,
    0x11,
    0x12,
    0xDC,
    0xE0,
    0xEF,
    0xFE,
])
def invalid_usb_device_class(request):
    """
    Fixture that yields a invalid USB device class.
    """
    return request.param


@pytest.fixture(scope='session')
def valid_usb_device_subclass():
    """
    Fixture that yields a valid USB device subclass.
    """
    return libusb.USB_DEVICE_SUBCLASS


@pytest.fixture(scope='session', params=[
    0x00,
    0x01,
    0x10,
    0xAB,
    0x33
])
def invalid_usb_device_subclass(request):
    """
    Fixture that yields a invalid USB device subclass.
    """
    return request.param


@pytest.fixture(scope='session')
def valid_usb_device_protocol():
    """
    Fixture that yields a valid USB device protocol.
    """
    return libusb.USB_DEVICE_PROTOCOL


@pytest.fixture(scope='session', params=[
    0x00,
    0x01,
    0x10,
    0xAB,
    0x33
])
def invalid_usb_device_protocol(request):
    """
    Fixture that yields a invalid USB device protocol.
    """
    return request.param


@pytest.fixture(scope='session', params=[
    '0123456789ABCDEF'
])
def valid_serial_number(request):
    """
    Fixture that yields valid USB device serial numbers.
    """
    return request.param


@pytest.fixture(scope='session', params=[
    0x18d1,
    0x2109,
    0x04b4,
    0x1b1c
])
def valid_vendor_id(request):
    """
    Fixture that yields valid USB device vendor id.
    """
    return request.param


@pytest.fixture(scope='session', params=[
    0x4ee2,
    0x0101,
    0x2812,
    0x1b1e
])
def valid_product_id(request):
    """
    Fixture that yields valid USB device product id.
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
    Fixture that yields a mock USB context object that is patched to be returned by
    :class:`~usb1.USBContext` and :meth:`~usb1.USBContext.open`.
    """
    mocker.patch.object(usb1, 'USBContext', side_effect=lambda: mock_context)
    mock_context.open.return_value = mock_context
    return mock_context


@pytest.fixture(scope='function')
def mock_context_no_devices(mock_context_class):
    """
    Fixture that yields a mock USB context that has no devices.
    """
    mock_context_class.getDeviceList.return_value = []
    return mock_context_class


@pytest.fixture(scope='function')
def mock_context_one_device_match(mock_context_class, mock_device, mock_interface_settings_match):
    """
    Fixture that yields a mock USB context that yields one device that matches based
    on class, subclass, and protocol.
    """
    mock_device.iterSettings.return_value = [mock_interface_settings_match]
    mock_context_class.getDeviceList.return_value = [mock_device]
    return mock_context_class


@pytest.fixture(scope='function')
def mock_context_one_device_match_serial(mock_context, mock_device_with_serial_factory, mock_interface_settings_match,
                                         valid_serial_number):
    """
    Fixture that yields a mock USB context that yields one device that matches based
    on serial number, class, subclass, and protocol.
    """
    device = mock_device_with_serial_factory(valid_serial_number)
    device.iterSettings.return_value = [mock_interface_settings_match]
    mock_context.getDeviceList.return_value = [device]
    return mock_context


@pytest.fixture(scope='function')
def mock_context_one_device_match_vid(mock_context, mock_device_with_vid_factory, mock_interface_settings_match,
                                      valid_vendor_id):
    """
    Fixture that yields a mock USB context that yields one device that matches based
    on vendor id, class, subclass, and protocol.
    """
    device = mock_device_with_vid_factory(valid_vendor_id)
    device.iterSettings.return_value = [mock_interface_settings_match]
    mock_context.getDeviceList.return_value = [device]
    return mock_context


@pytest.fixture(scope='function')
def mock_context_one_device_match_pid(mock_context, mock_device_with_pid_factory, mock_interface_settings_match,
                                      valid_product_id):
    """
    Fixture that yields a mock USB context that yields one device that matches based
    on product id, class, subclass, and protocol.
    """
    device = mock_device_with_pid_factory(valid_product_id)
    device.iterSettings.return_value = [mock_interface_settings_match]
    mock_context.getDeviceList.return_value = [device]
    return mock_context


@pytest.fixture(scope='function')
def mock_context_one_device_no_match(mock_context, mock_device, mock_interface_settings_mismatch_class):
    """
    Fixture that yields a mock USB context that yields one device that does not match based
    on class, subclass, and protocol.
    """
    mock_device.iterSettings.return_value = [mock_interface_settings_mismatch_class]
    mock_context.getDeviceList.return_value = [mock_device]
    return mock_context


@pytest.fixture(scope='function')
def mock_context_one_device_read_endpoint_no_write(mock_context_class, mock_device,
                                                   mock_interface_settings_endpoint_factory,
                                                   valid_read_endpoint_address):
    """
    Fixture that yields a mock USB context that yields one device that matches on
    class, subclass, and protocol but only has a valid read endpoint.
    """
    settings = mock_interface_settings_endpoint_factory(valid_read_endpoint_address)
    mock_device.iterSettings.return_value = [settings]
    mock_context_class.getDeviceList.return_value = [mock_device]
    return mock_context_class


@pytest.fixture(scope='function')
def mock_context_one_device_valid_endpoints(mock_context_class, mock_device, mock_endpoint_factory,
                                            mock_endpoint_valid_read_address, mock_endpoint_valid_write_address,
                                            mock_interface_settings_factory):
    """
    Fixture that yields a mock USB context that yields one device that matches on
    class, subclass, and protocol and has valid read/write endpoints.
    """
    settings = mock_interface_settings_factory(mock_endpoint_valid_read_address, mock_endpoint_valid_write_address)
    mock_device.iterSettings.return_value = [settings]
    mock_context_class.getDeviceList.return_value = [mock_device]
    return mock_context_class


@pytest.fixture(scope='function')
def mock_device(mocker):
    """
    Fixture that yields a mock USB device.
    """
    return mocker.MagicMock(usb1.USBDevice, autospec=True)


@pytest.fixture(scope='function')
def mock_device_with_serial_factory(mock_device):
    """
    Fixture that yields a function used to create mock USB devices with a specific serial number.
    """
    def factory(serial):
        mock_device.getSerialNumber.return_value = serial
        return mock_device

    return factory


@pytest.fixture(scope='function')
def mock_device_with_vid_factory(mock_device):
    """
    Fixture that yields a function used to create mock USB devices with a specific vendor id.
    """
    def factory(vendor_id):
        mock_device.getVendorID.return_value = vendor_id
        return mock_device

    return factory


@pytest.fixture(scope='function')
def mock_device_with_pid_factory(mock_device):
    """
    Fixture that yields a function used to create mock USB devices with a specific product id.
    """
    def factory(product_id):
        mock_device.getProductID.return_value = product_id
        return mock_device

    return factory


@pytest.fixture(scope='function')
def mock_handle(mocker):
    """
    Fixture that yields a mock USB device handle.
    """
    return mocker.MagicMock(usb1.USBDeviceHandle, autospec=True)


@pytest.fixture(scope='function')
def mock_read_handle(mock_handle):
    """
    Fixture that yields a mock USB device handle used for reading.
    """
    mock_handle.bulkRead.return_value = None
    return mock_handle


@pytest.fixture(scope='function')
def mock_write_handle(mock_handle):
    """
    Fixture that yields a mock USB device handle used for writing.
    """
    mock_handle.bulkWrite.side_effect = lambda *args: len(args[1])
    return mock_handle


@pytest.fixture(scope='function')
def mock_write_handle_incorrect_return_value(mock_handle):
    """
    Fixture that yields a mock USB device handle used for writing that yields back and incorrect
    number of bytes written.
    """
    mock_handle.bulkWrite.side_effect = lambda *args: len(args[1]) - 1
    return mock_handle


@pytest.fixture(scope='function')
def mock_handle_active_kernel_driver(mock_handle):
    """
    Fixture that yields a mock USB device handle that has an active kernel driver.
    """
    mock_handle.kernelDriverActive.return_value = True
    return mock_handle


@pytest.fixture(scope='function')
def mock_handle_inactive_kernel_driver(mock_handle):
    """
    Fixture that yields a mock USB device handle that has an inactive kernel driver.
    """
    mock_handle.kernelDriverActive.return_value = False
    return mock_handle


@pytest.fixture(scope='function')
def mock_endpoint(mocker, valid_endpoint_address):
    """
    Fixture that yields a mock USB endpoint.
    """
    mock = mocker.MagicMock(usb1.USBEndpoint, autospec=True)
    mock.getAddress.return_value = valid_endpoint_address
    return mock


@pytest.fixture(scope='function')
def mock_endpoint_valid_read_address(mocker, valid_read_endpoint_address):
    """
    Fixture that yields a mock USB endpoint with a valid read address.
    """
    mock = mocker.MagicMock(usb1.USBEndpoint, autospec=True)
    mock.getAddress.return_value = valid_read_endpoint_address
    return mock


@pytest.fixture(scope='function')
def mock_endpoint_valid_write_address(mocker, valid_write_endpoint_address):
    """
    Fixture that yields a mock USB endpoint with a valid write address.
    """
    mock = mocker.MagicMock(usb1.USBEndpoint, autospec=True)
    mock.getAddress.return_value = valid_write_endpoint_address
    return mock


@pytest.fixture(scope='function')
def mock_endpoint_factory(mock_endpoint):
    """
    Fixture that yields a factory function used to create a USB endpoint at the given address.
    """
    def factory(address):
        mock_endpoint.getAddress.return_value = address
        return mock_endpoint

    return factory


@pytest.fixture(scope='function')
def mock_interface_settings(mocker, valid_interface_number):
    """
    Fixture that yields mock USB interface settings.
    """
    mock = mocker.MagicMock(usb1.USBInterfaceSetting, autospec=True)
    mock.getNumber.return_value = valid_interface_number
    return mock


@pytest.fixture(scope='function')
def mock_interface_settings_factory(mock_interface_settings_match):
    """
    Fixture that yields a factory function used to create a valid USB interface settings
    object with a number of endpoints.
    """
    def factory(*endpoints):
        mock_interface_settings_match.iterEndpoints.return_value = endpoints
        return mock_interface_settings_match

    return factory


@pytest.fixture(scope='function')
def mock_interface_settings_match(mock_interface_settings):
    """
    Fixture that yields mock USB interface settings that is the correct USB class, subclass, and protocol.
    """
    mock_interface_settings.getClass.return_value = libusb.USB_DEVICE_CLASS
    mock_interface_settings.getSubClass.return_value = libusb.USB_DEVICE_SUBCLASS
    mock_interface_settings.getProtocol.return_value = libusb.USB_DEVICE_PROTOCOL
    return mock_interface_settings


@pytest.fixture(scope='function')
def mock_interface_settings_mismatch_class(mock_interface_settings, invalid_usb_device_class):
    """
    Fixture that yields mock USB interface settings that is an unsupported device class.
    """
    mock_interface_settings.getClass.return_value = invalid_usb_device_class
    return mock_interface_settings


@pytest.fixture(scope='function')
def mock_interface_settings_mismatch_subclass(mock_interface_settings, invalid_usb_device_subclass):
    """
    Fixture that yields mock USB interface settings that is an unsupported device subclass.
    """
    mock_interface_settings.getSubClass.return_value = invalid_usb_device_subclass
    return mock_interface_settings


@pytest.fixture(scope='function')
def mock_interface_settings_mismatch_protocol(mock_interface_settings, invalid_usb_device_protocol):
    """
    Fixture that yields mock USB interface settings that is an unsupported device protocol.
    """
    mock_interface_settings.getProtocol.return_value = invalid_usb_device_protocol
    return mock_interface_settings


@pytest.fixture(scope='function')
def mock_interface_settings_endpoint_factory(mocker, mock_interface_settings_match, mock_endpoint):
    """
    Fixture that yields a factory function used to create a USB interface settings object
    for a given endpoint address with a valid class, subclass, and protocol.
    """
    def factory(address):
        mock_endpoint.getAddress.return_value = address
        mock_interface_settings_match.iterEndpoints.return_value = [mock_endpoint]
        return mock_interface_settings_match

    return factory
