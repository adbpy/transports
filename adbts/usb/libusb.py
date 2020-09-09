"""
    adbts.usb.libusb
    ~~~~~~~~~~~~~~~~

    Functional wrapper around the `usb1` and `libusb` packages.
"""
import contextlib
import functools
import typing

import usb1

from adbts import exceptions, hints

#: Type hint alias for libusb :class:`~usb1.USBContext`.
Context = usb1.USBContext  # pylint: disable=invalid-name


#: Type hint alias for libusb :class:`~usb1.USBDevice`.
Device = usb1.USBDevice  # pylint: disable=invalid-name


#: Type hint alias for an optional libusb :class:`~usb1.USBDevice`.
OptionalDevice = typing.Optional[usb1.USBDevice]  # pylint: disable=invalid-name


#: Type hint for a USB device class.
DeviceClass = typing.Optional[hints.Int]  # pylint: disable=invalid-name


#: Type hist for a list of :class:`~usb1.USBDevice`.
DeviceList = typing.List[Device]  # pylint: disable=invalid-name


#: Type hint for a USB device endpoint.
Endpoint = usb1.USBEndpoint  # pylint: disable=invalid-name


#: Type hint for a generator that yields USB device endpoint.
EndpointGenerator = typing.Generator[usb1.USBEndpoint, None, None]  # pylint: disable=invalid-name


#: Type hint for an optional USB device endpoint.
OptionalEndpoint = typing.Optional[Endpoint]  # pylint: disable=invalid-name


#: Type hint alias for libusb :class:`~usb1.USBDeviceHandle`.
Handle = usb1.USBDeviceHandle  # pylint: disable=invalid-name


#: Type hint alias for an optional libusb :class:`~usb1.USBDeviceHandle`.
OptionalHandle = typing.Optional[usb1.USBDeviceHandle]  # pylint: disable=invalid-name


#: Type hint for device interface settings.
InterfaceSettings = usb1.USBInterfaceSetting  # pylint: disable=invalid-name


#: Type hint for optional device interface settings.
OptionalInterfaceSettings = typing.Optional[usb1.USBInterfaceSetting]  # pylint: disable=invalid-name


#: Type hint for USB context that is optional.
OptionalContext = typing.Optional[Context]  # pylint: disable=invalid-name


#: Type hint for a USB product id.
ProductId = typing.Optional[hints.Int]  # pylint: disable=invalid-name


#: Type hint for context manager that releases an interface.
# pylint: disable=invalid-name, protected-access
ReleaseInterfaceContextManager = usb1._ReleaseInterface
# pylint: enable=invalid-name, protected-access


#: Type hint for a USB serial number.
SerialNumber = typing.Optional[hints.Str]  # pylint: disable=invalid-name


#: Type hint for a USB vendor id.
VendorId = typing.Optional[hints.Int]  # pylint: disable=invalid-name


#: Type hint for an two-item tuple of USB device and settings.
DeviceAndInterfaceSettings = typing.Tuple[Device, InterfaceSettings]  # pylint: disable=invalid-name


#: Type hint for a generator function that yields device and interface settings.
# pylint: disable=invalid-name
DeviceAndInterfaceSettingsGenerator = typing.Generator[DeviceAndInterfaceSettings, None, None]
# pylint: enable=redefined-outer-name


#: Type hint for an optional two-item tuple of USB device and settings.
# pylint: disable=invalid-name
OptionalDeviceAndInterfaceSettings = typing.Union[DeviceAndInterfaceSettings, typing.Tuple[None, None]]
# pylint: enable=redefined-outer-name


#: USB device class supported by ADB (vendor specific).
USB_DEVICE_CLASS = 0xff


#: USB device subclass supported by ADB.
USB_DEVICE_SUBCLASS = 0x42


#: USB device protocol supported by ADB.
USB_DEVICE_PROTOCOL = 0x1


#: USB interface endpoint address flag value indicating it is used for reading.
USB_ENDPOINT_DIRECTION_IN = 0x80


def reraise_libusb_errors(func: hints.DecoratorFunc) -> hints.DecoratorReturnValue:
    """
    Decorator that catches :class:`~usb1.USBError` exceptions and re-raises them as
    specific exception types that derive from :class:`~adbts.exceptions.TransportError`.
    """
    @functools.wraps(func)
    def decorator(*args: hints.Args, **kwargs: hints.Kwargs) -> hints.DecoratorReturnValue:
        """
        Catch and re-raise libusb related exceptions raised from the decorated function.
        """
        try:
            return func(*args, **kwargs)
        except usb1.USBError as ex:
            if ex.value == usb1.ERROR_NO_DEVICE:  # pylint: disable=no-member
                raise exceptions.TransportEndpointNotFound(
                    'Device not found or has been disconnected') from ex
            if ex.value == usb1.ERROR_ACCESS:  # pylint: disable=no-member
                raise exceptions.TransportAccessDenied(
                    'Insufficient permissions or interface already claimed') from ex
            if ex.value == usb1.ERROR_TIMEOUT:  # pylint: disable=no-member
                raise exceptions.TransportTimeoutError(
                    'Exceeded timeout of {} ms'.format(kwargs.get('timeout', 'inf'))) from ex
            raise exceptions.TransportError(
                'Unhandled USB transport error {}'.format(getattr(ex, '__name__', str(ex)))) from ex

    return decorator


def read(handle: Handle,
         endpoint: Endpoint,
         num_bytes: hints.Int,
         timeout: hints.Int) -> hints.Buffer:
    """
    Ready bytes from a USB device endpoint.

    :param handle: USB device handle
    :type handle: :class:`~usb1.USBDeviceHandle`
    :param endpoint: Endpoint to read from
    :type endpoint: :class:`~usb1.USBEndpoint`
    :param num_bytes: Number of bytes to read
    :type num_bytes: :class:`~int`
    :param timeout: Maximum number of milliseconds allowed to read bytes from endpoint
    :type timeout: :class:`~int`
    :return: Collection of bytes read
    :rtype: :class:`~bytes` or :class:`~bytearray`
    :raises :class:`~adbts.exceptions.TransportEndpointNotFound`: When device is not found/disconnected
    :raises :class:`~adbts.exceptions.TransportAccessDenied`: When we lack permissions to read
    :raises :class:`~adbts.exceptions.TransportTimeoutError`: When read call exceeds timeout
    :raises :class:`~adbts.exceptions.TransportError`: When USB transport encounters unhandled error
    """
    return handle.bulkRead(endpoint.getAddress(), num_bytes, timeout)


def write(handle: Handle,  # pylint: disable=useless-return
          endpoint: Endpoint,
          data: hints.Buffer,
          timeout: hints.Int) -> None:
    """
    Write bytes to a USB device endpoint.

    :param handle: USB device handle
    :type handle: :class:`~usb1.USBDeviceHandle`
    :param endpoint: Endpoint to write to
    :type endpoint: :class:`~usb1.USBEndpoint`
    :param data: Collection of bytes to write
    :type data: :class:`~bytes` or :class:`~bytearray`
    :param timeout: Maximum number of milliseconds allowed to write bytes to endpoint
    :type timeout: :class:`~int`
    :return: Nothing
    :rtype: :class:`~NoneType`
    :raises :class:`~adbts.exceptions.TransportEndpointNotFound`: When device is not found/disconnected
    :raises :class:`~adbts.exceptions.TransportAccessDenied`: When we lack permissions to write
    :raises :class:`~adbts.exceptions.TransportTimeoutError`: When write call exceeds timeout
    :raises :class:`~adbts.exceptions.TransportError`: When USB transport encounters unhandled error
    :raises :class:`~adbts.exceptions.TransportError`: When not all bytes were written
    """
    num_bytes = handle.bulkWrite(endpoint.getAddress(), data, timeout)
    if num_bytes != len(data):
        raise exceptions.TransportError(
            'Only wrote {} bytes when expected {} bytes'.format(num_bytes, len(data)))
    return None


def close(context: Context,
          handle: Handle,
          interface_settings: InterfaceSettings) -> None:
    """
    Close connection to USB device.

    :param context: USB context that represents a session
    :type: :class:`~usb1.USBContext`
    :param handle: USB device handle
    :type handle: :class:`~usb1.USBDeviceHandle`
    :param interface_settings: Device interface previously claimed
    :type interface_settings: :class:`~int`
    :return: Nothing
    :rtype: :class:`~NoneType`
    """
    handle.releaseInterface(interface_settings.getNumber())
    handle.close()
    context.close()


def open_context() -> Context:
    """
    Create and open a new USB context.

    :return: Newly created and opened USB context
    :rtype: :class:`~usb1.USBContext`
    """
    return usb1.USBContext().open()


def open_device_handle(device: Device) -> Handle:
    """
    Open a new handle for the given device.

    :param device: Device to open handle on
    :type device: :class:`~usb1.USBDevice`
    :return: Handle to device used for I/O
    :rtype: :class:`~usb1.USBDeviceHandle`
    """
    return device.open()


def claim_interface(handle: Handle,
                    interface_settings: InterfaceSettings) -> ReleaseInterfaceContextManager:
    """
    Claim the interface represented by the settings on the given device handle.

    :param handle: Handle open to a USB device to claim interface on
    :type handle: :class:`~usb1.USBDeviceHandle`
    :param interface_settings: Settings that represent interface to claim
    :type interface_settings: :class:`~usb1.USBInterfaceSetting`
    :return: Nothing
    :rtype: :class:`~NoneType`
    """
    interface = interface_settings.getNumber()

    # Detach any existing kernel drivers for this USB device interface.
    # Note: If the device has "auto_detach_kernel_driver" enabled in the config, it will automatically
    # reattach.
    if handle.kernelDriverActive(interface):
        handle.detachKernelDriver(interface)

    # Claim the USB device interface so we can read/write to its endpoints.
    return handle.claimInterface(interface)


def find_device(serial: SerialNumber = None,
                vid: VendorId = None,
                pid: ProductId = None,
                context: OptionalContext = None,
                skip_on_error: hints.Bool = True) -> OptionalDeviceAndInterfaceSettings:
    """
    Find a local USB device.

    :param serial: Optional serial number filter
    :type serial: :class:`~str` or :class:`~NoneType`
    :param vid: Optional vendor id filter
    :type vid: :class:`~int` or :class:`~NoneType`
    :param vid: Optional product id filter
    :type pid: :class:`~int` or :class:`~NoneType`
    :param context: Optional USB context to use for querying devices
    :type context: :class:`~usb1.USBContext` or :class:`~NoneType`
    :param skip_on_error: Optional flag indicating if devices that raise errors should be ignored
    :type skip_on_error: :class:`~bool`
    :return: Two item tuple with device and interface settings
    :rtype: :class:`~tuple` containing :class:`~usb1.USBDevice` and :class:`~usb1.USBInterfaceSetting`
    """
    return next(find_devices_generator(serial, vid, pid, context, skip_on_error), (None, None))


def find_devices_generator(serial: SerialNumber = None,
                           vid: VendorId = None,
                           pid: ProductId = None,
                           context: OptionalContext = None,
                           skip_on_error: hints.Bool = True) -> DeviceAndInterfaceSettingsGenerator:
    """
    Generator function that yields local USB devices.

    :param serial: Optional serial number filter
    :type serial: :class:`~str` or :class:`~NoneType`
    :param vid: Optional vendor id filter
    :type vid: :class:`~int` or :class:`~NoneType`
    :param vid: Optional product id filter
    :type pid: :class:`~int` or :class:`~NoneType`
    :param context: Optional USB context to use for querying devices
    :type context: :class:`~usb1.USBContext` or :class:`~NoneType`
    :param skip_on_error: Optional flag indicating if devices that raise errors should be ignored
    :type skip_on_error: :class:`~bool`
    :return: Generator that yields tuples for matching devices
    :rtype: :class:`~generator`
    """
    yield from ((device, settings)
                for device, settings in find_devices_interfaces_generator(context, skip_on_error)
                if device_matches(device, settings, serial, vid, pid))


def find_devices_interfaces_generator(context: OptionalContext = None,  # pylint: disable=invalid-name
                                      skip_on_error: hints.Bool = True) -> DeviceAndInterfaceSettingsGenerator:
    """
    Generator function that yields combinations of all USB devices with settings
    for all of their interfaces.

    :param context: Optional USB context to use for querying devices
    :type context: :class:`~usb1.USBContext` or :class:`~NoneType`
    :param skip_on_error: Optional flag indicating if devices that raise errors should be ignored
    :type skip_on_error: :class:`~bool`
    :return: Generator that yields tuples for devices and all interfaces
    :rtype: :class:`~generator`
    """
    with optional_usb_context(context) as ctx:
        for device in ctx.getDeviceList(skip_on_error=skip_on_error):
            for settings in device.iterSettings():
                yield device, settings


def device_matches(device: Device,
                   settings: InterfaceSettings,
                   serial: SerialNumber = None,
                   vid: VendorId = None,
                   pid: ProductId = None) -> hints.Bool:
    """
    Check if given device and interface settings matches filter.

    :param device: USB device to check
    :type device: :class:`~usb1.USBDevice`
    :param settings: Settings for an interface on this USB device
    :type :class:`~usb1.USBInterfaceSetting`
    :param serial: Optional serial number filter
    :type serial: :class:`~str` or :class:`~NoneType`
    :param vid: Optional vendor id filter
    :type vid: :class:`~int` or :class:`~NoneType`
    :param vid: Optional product id filter
    :type pid: :class:`~int` or :class:`~NoneType`
    :return: Boolean indicating match
    :rtype: :class:`~bool`
    """
    serial_match = not serial or device.getSerialNumber() == serial
    vid_match = not vid or device.getVendorID() == vid
    pid_match = not pid or device.getProductID() == pid
    usb_class_match = settings.getClass() == USB_DEVICE_CLASS
    usb_subclass_match = settings.getSubClass() == USB_DEVICE_SUBCLASS
    usb_protocol_match = settings.getProtocol() == USB_DEVICE_PROTOCOL
    return all((serial_match, vid_match, pid_match, usb_class_match, usb_subclass_match, usb_protocol_match))


@contextlib.contextmanager
def optional_usb_context(context: OptionalContext = None) -> typing.Generator[Context, None, None]:
    """
    Context manager that uses or creates a USB context for the duration of the block.

    :param context: Optional USB context to use
    :type context: :class:`~usb1.USBContext` or :class:`~NoneType`
    :return: Function that optionally creates a USB context for the block
    :rtype: :class:`~function`
    """
    ctx = context or open_context()
    try:
        yield ctx
    finally:
        if not context:
            ctx.close()


def find_read_endpoint(settings: InterfaceSettings) -> OptionalEndpoint:
    """
    Find read endpoint for given USB interface settings.

    :param settings: USB interface settings on a device
    :type settings: :class:`~usb1.USBInterfaceSetting`
    :return: Endpoint used for reading
    :rtype: :class:`~usb1.USBEndpoint`
    """
    return next(read_endpoints_generator(settings), None)


def find_write_endpoint(settings: InterfaceSettings) -> OptionalEndpoint:
    """
    Find write endpoint for given USB interface settings.

    :param settings: USB interface settings on a device
    :type settings: :class:`~usb1.USBInterfaceSetting`
    :return: Endpoint used for writing
    :rtype: :class:`~usb1.USBEndpoint`
    """
    return next(write_endpoints_generator(settings), None)


def read_endpoints_generator(settings: InterfaceSettings) -> EndpointGenerator:
    """
    Generator function that yields all endpoints capable of reading.

    :param settings: USB interface settings on a device
    :type settings: :class:`~usb1.USBInterfaceSetting`
    :return: Generator that yields read endpoints
    :rtype: :class:`~generator`
    """
    yield from (endpoint
                for endpoint in settings.iterEndpoints()
                if is_read_endpoint(endpoint))


def write_endpoints_generator(settings: InterfaceSettings) -> EndpointGenerator:
    """
    Generator function that yields all endpoints capable of writing.

    :param settings: USB interface settings on a device
    :type settings: :class:`~usb1.USBInterfaceSetting`
    :return: Generator that yields write endpoints
    :rtype: :class:`~generator`
    """
    yield from (endpoint
                for endpoint in settings.iterEndpoints()
                if is_write_endpoint(endpoint))


def is_read_endpoint(endpoint: Endpoint) -> hints.Bool:
    """
    Predicate function that determines if the given endpoint is capable of reading.

    :param endpoint: Endpoint to check
    :type: :class:`~usb1.USBEndpoint`
    :return: True if the endpoint is for reading, False otherwise
    :rtype: :class:`~bool`
    """
    return endpoint.getAddress() & USB_ENDPOINT_DIRECTION_IN == USB_ENDPOINT_DIRECTION_IN


def is_write_endpoint(endpoint: Endpoint) -> hints.Bool:
    """
    Predicate function that determines if the given endpoint is capable of writing.

    :param endpoint: Endpoint to check
    :type: :class:`~usb1.USBEndpoint`
    :return: True if the endpoint is for writing, False otherwise
    :rtype: :class:`~bool`
    """
    return not is_read_endpoint(endpoint)
