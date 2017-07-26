"""
    adbtp.usb.sync
    ~~~~~~~~~~~~~~

    Contains functionality for synchronous Universal Serial Bus (USB) transport.
"""
from . import transport_timeout, libusb
from .. import ctxlib, exceptions, hints, transport

__all__ = ['Transport']


class Transport(transport.Transport):
    """
    Defines synchronous (blocking) USB transport.
    """

    def __init__(self, serial: libusb.SerialNumber, vid: libusb.VendorId,
                 pid: libusb.ProductId, context: libusb.Context, device: libusb.Device,
                 handle: libusb.Handle, interface_settings: libusb.InterfaceSettings,
                 read_endpoint: libusb.Endpoint, write_endpoint: libusb.Endpoint) -> None:
        self._serial = serial
        self._vid = vid
        self._pid = pid
        self._context = context
        self._device = device
        self._handle = handle
        self._interface_settings = interface_settings
        self._read_endpoint = read_endpoint
        self._write_endpoint = write_endpoint

    def __repr__(self):
        return '<{}({}, state={!r})>'.format(self.__class__.__name__, str(self),
                                             'closed' if self.closed else 'open')

    def __str__(self):
        serial = 'serial={!r}'.format(self._serial or '*')
        vid = 'vid={!r}'.format(self._vid or '*')
        pid = 'pid={!r}'.format(self._pid or '*')
        return ', '.join((serial, vid, pid))

    @property
    def closed(self):
        """
        Checks to see if the transport is closed.

        :return: Closed state of the transport
        :rtype: :class:`~bool`
        """
        return self._context is None

    @libusb.reraise_libusb_errors
    def read(self, num_bytes: hints.Int,
             timeout: hints.Timeout=transport.TIMEOUT_SENTINEL) -> transport.TransportReadResult:
        """
        Read bytes from the transport.

        :param num_bytes: Number of bytes to read.
        :type num_bytes: :class:`~int`
        :param timeout: Maximum number of milliseconds to read before raising an exception.
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return: Collection of bytes read
        :rtype: :class:`~bytes` or :class:`~bytearray`
        :raises :class:`~adbtp.exceptions.TransportProtocolError`: When underlying transport encounters an error
        :raises :class:`~adbtp.exceptions.TimeoutError`: When timeout is exceeded
        """
        return libusb.read(self._handle, self._read_endpoint, num_bytes, transport_timeout(timeout))

    @libusb.reraise_libusb_errors
    def write(self, data: hints.Buffer,
              timeout: hints.Timeout=transport.TIMEOUT_SENTINEL) -> transport.TransportWriteResult:
        """
        Write bytes to the transport.

        :param data: Collection of bytes to write.
        :type data: :class:`~bytes` or :class:`~bytearray`
        :param timeout: Maximum number of milliseconds to write before raising an exception.
        :type timeout: :class:`~int`, :class:`~NoneType`, or :class:`~object`
        :return Nothing
        :rtype: :class:`~NoneType`
        :raises :class:`~adbtp.exceptions.TransportProtocolError`: When underlying transport encounters an error
        :raises :class:`~adbtp.exceptions.TimeoutError`: When timeout is exceeded
        """
        return libusb.write(self._handle, self._write_endpoint, data, transport_timeout(timeout))

    @libusb.reraise_libusb_errors
    def close(self) -> None:
        """
        Close the transport.

        :return: Nothing
        :rtype: `None`
        :raises :class:`~adbtp.exceptions.TransportProtocolError`: When underlying transport encounters an error
        """
        libusb.close(self._context, self._handle, self._interface_settings)
        self._context = None
        self._device = None
        self._handle = None
        self._interface_settings = None
        self._read_endpoint = None
        self._write_endpoint = None


@libusb.reraise_libusb_errors
def open(serial: libusb.SerialNumber, vid: libusb.VendorId,  # pylint: disable=redefined-builtin
         pid: libusb.ProductId) -> transport.TransportOpenResult:
    """
    Open a new :class:`~adbtp.usb.sync.Transport` transport to a USB device.

    :param serial: Optional serial number filter
    :type serial: :class:`~str` or :class:`~NoneType`
    :param vid: Optional vendor id filter
    :type vid: :class:`~int` or :class:`~NoneType`
    :param vid: Optional product id filter
    :type pid: :class:`~int` or :class:`~NoneType`
    :return:
    """
    # Create a new context for accessing a USB device. Libusb uses a context structure to represent
    # individual user sessions and prevent interference between then when using a device concurrently.
    with ctxlib.close_on_error(libusb.open_context()) as context:
        # Grab first device that matches the given serial/vid/pid filter provided. If no filter
        # was provided, this will yield back the first device that matches the USB class/subclass/protocol
        # supported by ADB.
        device, interface_settings = libusb.find_device(serial, vid, pid, context)
        if not device or not interface_settings:
            raise exceptions.TransportEndpointNotFound(
                'Cannot find USB device for serial={} vid={} pid={}'.format(serial, vid, pid))

        # Grab first device interface endpoint that is used for reading.
        read_endpoint = libusb.find_read_endpoint(interface_settings)
        if not read_endpoint:
            raise exceptions.TransportProtocolError('Cannot find read endpoint for USB device interface')

        # Grab first device interface endpoint that is used for writing.
        write_endpoint = libusb.find_write_endpoint(interface_settings)
        if not write_endpoint:
            raise exceptions.TransportProtocolError('Cannot find write endpoint for USB device interface')

        # Open this USB device and grab a handle required to perform I/O. Grabbing a handle is purely a libusb
        # construct and this does not sent any data over the bus.
        with ctxlib.close_on_error(libusb.open_device_handle(device)) as handle:
            # Claim the device interface. Doing makes this USB device interface unusable to other clients
            # until it is released.
            libusb.claim_interface(handle, interface_settings)

            return Transport(serial, vid, pid, context, device, handle,
                             interface_settings, read_endpoint, write_endpoint)
