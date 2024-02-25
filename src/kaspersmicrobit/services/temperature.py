#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable

from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service
from ..bluetoothdevice import BluetoothDevice


class TemperatureService:
    """
    This class contains the functions that you can use in connection with the temperature sensor of the micro:bit
    This sensor measures the temperature of the micro:bit in degrees Celsius.

    These are all options offered by the Bluetooth temperature service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/temperature-service/
    """

    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Checks whether the temperature Bluetooth service is found on the connected micro:bit.

        Returns:
            true if the temperature service was found, false if not.
        """
        return self._device.is_service_available(Service.TEMPERATURE)

    def notify(self, callback: Callable[[int], None]):
        """
        You can call this method whenever you want to be notified of the temperature. How often you receive data
        depends on the period. By default the period is 1 second.

        Args:
            callback: a function that is called periodically with the temperature as an argument

        Raises:
            errors.BluetoothServiceNotFound: When the temperature service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the temperature service is active but there was no way
                to activate temperature data notifications (normally does not occur)
        """
        self._device.notify(Service.TEMPERATURE, Characteristic.TEMPERATURE,
                            lambda sender, data: callback(int.from_bytes(data[0:1], 'little', signed=True)))

    def read(self) -> int:
        """
        Reads the temperature of the micro:bit.

        Returns:
            the temperature in degrees Celsius

        Raises:
            errors.BluetoothServiceNotFound: When the temperature service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the temperature service is active but there was no way
                to read the temperature (normally does not occur)
        """
        return int.from_bytes(
            self._device.read(Service.TEMPERATURE, Characteristic.TEMPERATURE)[0:1], 'little', signed=True)

    def set_period(self, period: int):
        """
        Sets the interval at which you receive the temperature if you requested it via the notify method
        By default the period is 1 second.

        Args:
            period (int): the interval at which you receive temperature data in milliseconds

        Raises:
            errors.BluetoothServiceNotFound: When the temperature service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the temperature service is active but there was no way
                to write the temperature period (normally does not occur)
        """
        self._device.write(Service.TEMPERATURE, Characteristic.TEMPERATURE_PERIOD, period.to_bytes(2, "little"))

    def read_period(self) -> int:
        """
        Returns the interval at which you receive the temperature via notify

        Returns:
            The interval in milliseconds

        Raises:
            errors.BluetoothServiceNotFound: When the temperature service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the temperature service is active but there was no way
                to read the temperature period (normally does not occur)
        """
        return int.from_bytes(
            self._device.read(Service.TEMPERATURE, Characteristic.TEMPERATURE_PERIOD)[0:2], "little")
