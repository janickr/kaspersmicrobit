#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bluetoothdevice import BluetoothDevice, BluetoothEventLoop
from services.device_information import DeviceInformationService
from services.generic_access import GenericAccessService
from services.buttons import ButtonService
from services.temperature import TemperatureService
from services.accelerometer import AccelerometerService
from services.events import EventService
from services.uart import UartService
from services.magnetometer import MagnetometerService
from services.io_pin import IOPinService
from services.led import LedService


class KaspersMicrobit:
    def __init__(self, address: str, loop=BluetoothEventLoop.single_thread()):
        self._device = BluetoothDevice(address, loop=loop)
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
        self._device.connect()

    def disconnect(self) -> None:
        self._device.disconnect()

