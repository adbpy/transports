"""
    test_usb_libusb
    ~~~~~~~~~~~~~~~

    Tests for the :mod:`~adbtp.usb.libusb` module.
"""
import pytest
import usb1

from adbtp import exceptions
from adbtp.usb import libusb


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


def test_open_context_returns_new_context(mock_context_class):
    """
    Assert that :func:`~adbtp.usb.libusb.open_context` returns a new :class:`~usb1.USBContext` instance
    by calling :meth:`~usb1.USBContext.open`.
    """
    libusb.open_context()
    mock_context_class.open.assert_called_with()


def test_open_device_handle_calls_open_on_device(mock_device):
    """
    Assert that :func:`~adbtp.usb.libusb.open_device_handle` creates a new :class:`~usb1.USBDeviceHandle`
    by calling :meth:`~usb1.USBDevice.open`.
    """
    libusb.open_device_handle(mock_device)
    mock_device.open.assert_called_with()


def test_claim_interface_claims_interface_settings_number(mock_handle, mock_interface_settings,
                                                          valid_interface_number):
    """
    Assert that :func:`~adbtp.usb.libusb.claim_interface` claims the interface number of
    the given interface settings.
    """
    libusb.claim_interface(mock_handle, mock_interface_settings)
    mock_handle.claimInterface.assert_called_with(valid_interface_number)


def test_claim_interface_detaches_kernel_driver_when_active(mock_handle_active_kernel_driver, mock_interface_settings,
                                                            valid_interface_number):
    """
    Assert that :func:`~adbtp.usb.libusb.claim_interface` detaches the kernel driver if it is active.
    """
    libusb.claim_interface(mock_handle_active_kernel_driver, mock_interface_settings)
    mock_handle_active_kernel_driver.detachKernelDriver.assert_called_with(valid_interface_number)


def test_claim_interface_does_not_detach_kernel_driver_when_inactive(mock_handle_inactive_kernel_driver,
                                                                     mock_interface_settings, valid_interface_number):
    """
    Assert that :func:`~adbtp.usb.libusb.claim_interface` does not try and detach the kernel driver
    if it is inactive.
    """
    libusb.claim_interface(mock_handle_inactive_kernel_driver, mock_interface_settings)
    assert not mock_handle_inactive_kernel_driver.detachKernelDriver.called


def test_find_device_uses_match_on_class_subclass_protocol(mock_context_one_device_match):
    """
    Assert that :func:`~adbtp.usb.libusb.find_device` will find device when one is available that
    matches based on class, subclass, and protocol.
    """
    assert libusb.find_device(context=mock_context_one_device_match) != (None, None)


def test_find_device_ignores_mismatch_on_class_subclass_protocol(mock_context_one_device_no_match):
    """
    Assert that :func:`~adbtp.usb.libusb.find_device` will find no devices when one is available that
    does not match based on class, subclass, and protocol.
    """
    assert libusb.find_device(context=mock_context_one_device_no_match) == (None, None)


def test_find_device_uses_match_on_serial(mock_context_one_device_match_serial, valid_serial_number):
    """
    Assert that :func:`~adbtp.usb.libusb.find_device` will find device when one is available that
    matches based on serial, class, subclass, and protocol.
    """
    device, settings = libusb.find_device(serial=valid_serial_number, context=mock_context_one_device_match_serial)
    assert device.getSerialNumber() == valid_serial_number


def test_find_device_uses_match_on_vid(mock_context_one_device_match_vid, valid_vendor_id):
    """
    Assert that :func:`~adbtp.usb.libusb.find_device` will find device when one is available that
    matches based on vendor id, class, subclass, and protocol.
    """
    device, settings = libusb.find_device(vid=valid_vendor_id, context=mock_context_one_device_match_vid)
    assert device.getVendorID() == valid_vendor_id


def test_find_device_uses_match_on_pid(mock_context_one_device_match_pid, valid_product_id):
    """
    Assert that :func:`~adbtp.usb.libusb.find_device` will find device when one is available that
    matches based on product id, class, subclass, and protocol.
    """
    device, settings = libusb.find_device(pid=valid_product_id, context=mock_context_one_device_match_pid)
    assert device.getProductID() == valid_product_id


def test_device_matches_with_no_filter_on_class_subclass_and_protocol(mock_device, mock_interface_settings_match):
    """
    Assert that :func:`~adbtp.usb.libusb.device_matches` will match USB devices based on
    class, subclass, and protocol when no serial/vid/pid filter is given.
    """
    assert libusb.device_matches(mock_device, mock_interface_settings_match)


def test_device_mismatches_on_invalid_usb_class(mock_device, mock_interface_settings_mismatch_class):
    """
    Assert that :func:`~adbtp.usb.libusb.device_matches` will not match USB devices that
    use an invalid device class.
    """
    assert not libusb.device_matches(mock_device, mock_interface_settings_mismatch_class)


def test_device_mismatches_on_invalid_usb_subclass(mock_device, mock_interface_settings_mismatch_subclass):
    """
    Assert that :func:`~adbtp.usb.libusb.device_matches` will not match USB devices that
    use an invalid device subclass.
    """
    assert not libusb.device_matches(mock_device, mock_interface_settings_mismatch_subclass)


def test_device_mismatches_on_invalid_usb_protocol(mock_device, mock_interface_settings_mismatch_protocol):
    """
    Assert that :func:`~adbtp.usb.libusb.device_matches` will not match USB devices that
    use an invalid device protocol.
    """
    assert not libusb.device_matches(mock_device, mock_interface_settings_mismatch_protocol)


def test_device_matches_on_settings_and_serial(mock_device_with_serial_factory, mock_interface_settings_match,
                                               valid_serial_number):
    """
    Assert that :func:`~adbtp.usb.libusb.device_matches` will match a device based on correct interface
    settings and serial number.
    """
    device = mock_device_with_serial_factory(valid_serial_number)
    assert libusb.device_matches(device, mock_interface_settings_match)


def test_device_matches_on_settings_and_vendor_id(mock_device_with_vid_factory, mock_interface_settings_match,
                                                  valid_vendor_id):
    """
    Assert that :func:`~adbtp.usb.libusb.device_matches` will match a device based on correct interface
    settings and vendor id.
    """
    device = mock_device_with_vid_factory(valid_vendor_id)
    assert libusb.device_matches(device, mock_interface_settings_match)


def test_device_matches_on_settings_and_product_id(mock_device_with_pid_factory, mock_interface_settings_match,
                                                   valid_product_id):
    """
    Assert that :func:`~adbtp.usb.libusb.device_matches` will match a device based on correct interface
    settings and product id.
    """
    device = mock_device_with_pid_factory(valid_product_id)
    assert libusb.device_matches(device, mock_interface_settings_match)


def test_optional_usb_context_yields_context_when_given(mock_context):
    """
    Assert that :func:`~adbtp.usb.libusb.optional_usb_context` yields back the USB context instance
    if one was given.
    """
    with libusb.optional_usb_context(mock_context) as ctx:
        assert ctx is mock_context


def test_optional_usb_context_doesnt_close_context_when_given(mock_context):
    """
    Assert that :func:`~adbtp.usb.libusb.optional_usb_context` does not close the USB context
    if one was given.
    """
    with libusb.optional_usb_context(mock_context):
        pass
    assert not mock_context.close.called


def test_optional_usb_context_creates_new_one_when_not_given(mock_context_class):
    """
    Assert that :func:`~adbtp.usb.libusb.optional_usb_context` creates a new USB context instance
    if one was not given.
    """
    with libusb.optional_usb_context():
        pass
    assert usb1.USBContext.called


def test_optional_usb_context_closes_context_when_not_given(mock_context_class):
    """
    Assert that :func:`~adbtp.usb.libusb.optional_usb_context` closes the USB context it
    creates if one was not given.
    """
    with libusb.optional_usb_context():
        pass
    mock_context_class.close.assert_called_with()


def test_find_read_endpoint_returns_read_endpoint_on_match(mock_interface_settings_endpoint_factory,
                                                           valid_read_endpoint_address):
    """
    Assert that :func:`~adbtp.usb.libusb.find_read_endpoint` returns a matching endpoint object when
    one that supports reading is available.
    """
    settings = mock_interface_settings_endpoint_factory(valid_read_endpoint_address)
    endpoint = libusb.find_read_endpoint(settings)
    assert endpoint is not None
    assert endpoint.getAddress() == valid_read_endpoint_address


def test_find_read_endpoint_returns_none_on_mismatch(mock_interface_settings_endpoint_factory,
                                                     valid_write_endpoint_address):
    """
    Assert that :func:`~adbtp.usb.libusb.find_read_endpoint` returns None when no read
    endpoints are available.
    """
    settings = mock_interface_settings_endpoint_factory(valid_write_endpoint_address)
    endpoint = libusb.find_read_endpoint(settings)
    assert not endpoint


def test_find_write_endpoint_returns_read_endpoint_on_match(mock_interface_settings_endpoint_factory,
                                                           valid_write_endpoint_address):
    """
    Assert that :func:`~adbtp.usb.libusb.find_write_endpoint` returns a matching endpoint object when
    one that supports writing is available.
    """
    settings = mock_interface_settings_endpoint_factory(valid_write_endpoint_address)
    endpoint = libusb.find_write_endpoint(settings)
    assert endpoint is not None
    assert endpoint.getAddress() == valid_write_endpoint_address


def test_find_write_endpoint_returns_none_on_mismatch(mock_interface_settings_endpoint_factory,
                                                     valid_read_endpoint_address):
    """
    Assert that :func:`~adbtp.usb.libusb.find_write_endpoint` returns None when no write
    endpoints are available.
    """
    settings = mock_interface_settings_endpoint_factory(valid_read_endpoint_address)
    endpoint = libusb.find_write_endpoint(settings)
    assert not endpoint
