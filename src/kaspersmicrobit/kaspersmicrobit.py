#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Union

from bleak import BleakClient, BleakScanner

from .bluetoothdevice import BluetoothDevice, BluetoothEventLoop, ThreadEventLoop
from .errors import KaspersMicrobitNotFound
from .services.device_information import DeviceInformationService
from .services.generic_access import GenericAccessService
from .services.buttons import ButtonService
from .services.temperature import TemperatureService
from .services.accelerometer import AccelerometerService
from .services.events import EventService
from .services.uart import UartService
from .services.magnetometer import MagnetometerService
from .services.io_pin import IOPinService
from .services.led import LedService


class KaspersMicrobit:
    """
    This is the class you can use to connect to a micro:bit.
    You can do this:

    - read data about the micro:bit
    - read data from the sensors of the micro:bit or be notified of data from sensors
    - control components on the micro:bit, for example the LEDs

    Example:
    ```python
    with KaspersMicrobit.find_one_microbit() as microbit:
        microbit.buttons.on_button_a(press=pressed, long_press=pressed_long, up=released)
        microbit.temperature.notify(lambda temp: print(f'{temp}°C'))
        time.sleep(25)
    ```

    ```python
    microbit = KaspersMicrobit.find_one_microbit()
    try:
        microbit.connect()
        microbit.buttons.on_button_a(press=pressed, long_press=pressed_long, up=released)
        microbit.temperature.notify(lambda temp: print(f'{temp}°C'))
        time.sleep(25)
    finally:
        microbit.disconnect()
    ```

    Attributes:
        device_information (DeviceInformationService):
            To request information about the maker of your micro:bit
        generic_access (GenericAccessService):
            To request information about your micro:bit
        buttons (ButtonService):
            To notify you when one of the two buttons on the micro:bit is pressed (or released)
        temperature (TemperatureService):
            To request the temperature of the environment of the micro:bit (or to be notified)
        accelerometer (AccelerometerService):
            To notify you of acceleration (movement, collision,...) of the micro:bit
        events (EventService):
            To subscribe to receive events from various components of the micro:bit
        uart (UartService):
            To send or receive text to the micro:bit
        io_pin (IOPinService):
            Control, read, configure the I/O contacts (pins) on the micro:bit
        led (LedService):
            Control the LEDs of the micro:bit
        magnetometer (MagnetometerService):
            To read the data from the magnetometer, or to be notified. The magnetometer measures
            the magnetic field in the vicinity of the micro:bit (e.g. the magnetic field of the earth)


    See Also: https://makecode.microbit.org/reference/bluetooth

    See Also: https://makecode.microbit.org/device
    """

    def __init__(self, address_or_bluetoothdevice: Union[str, BluetoothDevice]):
        """
        Create a KaspersMicrobit object with a given Bluetooth address.

        Args:
            address_or_bluetoothdevice: the bluetooth address of the micro:bit
        """
        if isinstance(address_or_bluetoothdevice, BluetoothDevice):
            self._device = address_or_bluetoothdevice
        else:
            self._device = BluetoothDevice(BleakClient(address_or_bluetoothdevice))

        self.device_information = DeviceInformationService(self._device)
        self.generic_access = GenericAccessService(self._device)
        self.buttons = ButtonService(self._device)
        self.temperature = TemperatureService(self._device)
        self.accelerometer = AccelerometerService(self._device)
        self.events = EventService(self._device)
        self.uart = UartService(self._device)
        self.io_pin = IOPinService(self._device)
        self.led = LedService(self._device)
        self.magnetometer = MagnetometerService(self._device)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self) -> None:
        """
        Connect to the micro:bit. This establishes a connection. Your micro:bit may not already have (another)
        connection.

        Troubleshooting:
            First try turning the micro:bit off and on again.

            If you are not using the "with"-block, but calling .connect() yourself, always make sure that in any case
            you call .disconnect() when you don't need the connection anymore
            (for instance when you exit your application)

            - In case you are using "No pairing required":
              Make sure the micro:bit is not paired to your computer, if it was, remove it from the paired bluetooth
              devices
            - In case you are using "Just works pairing":
              Try to remove the micro:bit from the paired bluetooth devices and pairing it your computer again.

        See Also: https://support.microbit.org/helpdesk/attachments/19075694226
        """
        self._device.connect()

    def disconnect(self) -> None:
        """
        Disconnect the micro:bit.
        You must be connected to this micro:bit to successfully invoke this method.
        """
        self._device.disconnect()

    def address(self) -> str:
        """
        Returns the Bluetooth address of this micro:bit

        Returns:
            The address of the micro:bit
        """
        return self._device.address()

    def name(self) -> str:
        """
        Returns the name of this micro:bit.
        When paired it will return "BBC micro:bit"
        When not paired it will return the full name, for example: "BBC micro:bit [gatug]"

        Returns:
            The name of the micro:bit
        """
        return self._device.name()

    @staticmethod
    def find_microbits(timeout: int = 3, loop: BluetoothEventLoop = None) -> List['KaspersMicrobit']:
        """
        Scans for Bluetooth devices. Returns a list of micro:bits found within the timeout

        Args:
             timeout: maximum scanning time (in seconds)
             loop (BluetoothEventLoop): you can leave this empty, this determines which thread communicates with the micro:bit.

        Returns:
            A list of micro:bits found, this can also be empty if no micro:bits were found

        """

        loop = loop if loop else ThreadEventLoop.single_thread()
        devices = loop.run_async(BleakScanner.discover(timeout)).result()
        name_filter = KaspersMicrobit._name_filter()
        return [
            KaspersMicrobit(BluetoothDevice(BleakClient(d), loop))
            for d in devices
            if name_filter(d.name)
        ]

    @staticmethod
    def find_one_microbit(microbit_name: str = None, timeout: int = 3, loop: BluetoothEventLoop = None) -> 'KaspersMicrobit':
        """
        Scans for Bluetooth devices. Returns exactly 1 micro:bit if one is found. You can optionally
        Specify a name to search for. If no name is given, and there are multiple micro:bits
        active then a found micro:bit will be chosen at random and returned.

        Warning:
            Only when the micro:bit works with "No pairing required" will the micro:bit advertise a name. So only
            in case you use hex files with "No pairing required" it is useful to set the 'microbit_name' parameter.
            This does not work with a micro:bit that is paired.

        Args:
             microbit_name: the name of the micro:bit. This is a name of 5 letters such as 'tupaz' or 'gatug' or
                  something like that. This is optional.
             timeout: maximum scanning time (in seconds)
             loop (BluetoothEventLoop): you can leave this empty, this determines which thread communicates with the micro:bit.

        Returns:
            KaspersMicrobit: The micro:bit found

        Raises:
            KaspersMicrobitNotFound: if no micro:bit was found
        """
        loop = loop if loop else ThreadEventLoop.single_thread()

        def name_filter(d, ad):
            return KaspersMicrobit._name_filter(microbit_name)(ad.local_name)

        device = loop.run_async(BleakScanner.find_device_by_filter(filterfunc=name_filter, timeout=timeout)).result()
        if device:
            return KaspersMicrobit(BluetoothDevice(BleakClient(device), loop))
        else:
            raise KaspersMicrobitNotFound(microbit_name, loop.run_async(BleakScanner.discover(timeout)).result())

    @staticmethod
    def _name_filter(microbit_name: str = None):
        return lambda \
            device_name: device_name == f'BBC micro:bit [{microbit_name.strip()}]' \
            if microbit_name \
            else device_name and device_name.startswith('BBC micro:bit')
