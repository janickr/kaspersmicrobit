#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable

from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service
from ..bluetoothdevice import BluetoothDevice, ByteData

PDU_BYTE_LIMIT = 20


class UartService:
    """
    This class contains methods to send or receive bytes or strings to the micro:bit

    See Also: https://lancaster-university.github.io/microbit-docs/ble/uart-service/
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Checks whether the UART Bluetooth service is found on the connected micro:bit.

        Returns:
            true if the uart service was found, false if not.
        """
        return self._device.is_service_available(Service.UART)

    def receive(self, callback: Callable[[ByteData], None]):
        """
        You can call this method if you want to be notified when bytes are sent from the micro:bit
        via the uart service

        Args:
            callback (Callable[[ByteData], None]): a function that will be called with the received bytes

        Raises:
            errors.BluetoothServiceNotFound: When the uart service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the uart service is running but there was no way
                to activate the notifications of uart data (normally does not occur)
        """
        self._device.notify(Service.UART, Characteristic.TX_CHARACTERISTIC, lambda sender, data: callback(data))

    def receive_string(self, callback: Callable[[str], None]):
        """
        You can call this method if you want to be notified when a string is sent from the micro:bit
        via the uart service

        Args:
            callback (Callable[[str], None]): a function that will be called with the received string

        Raises:
            errors.BluetoothServiceNotFound: When the uart service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the uart service is running but there was no way
                to activate the notifications of uart data (normally does not occur)
        """
        self.receive(UartService.to_string(callback))

    def send(self, data: ByteData):
        """
        Send bytes via the uart service to the micro:bit

        Args:
            data (ByteData): the bytes that are sent

        Raises:
            errors.BluetoothServiceNotFound: When the uart service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the uart service is running but there was no way
                to send data via the UART service (normally does not occur)
        """
        for i in range(0, len(data), PDU_BYTE_LIMIT):
            self._device.write(Service.UART, Characteristic.RX_CHARACTERISTIC, data[i:i + PDU_BYTE_LIMIT])

    def send_string(self, string: str):
        """
        Send a string via the uart service to the micro:bit

        Args:
            string (str): the string to be sent

        Raises:
            errors.BluetoothServiceNotFound: When the uart service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the uart service is running but there was no way
                to send data via the UART service (normally does not occur)
        """
        self.send(UartService.from_string(string))

    @staticmethod
    def from_string(string: str) -> bytes:
        return string.encode("utf-8")

    @staticmethod
    def to_string(callback):
        return lambda data: callback(str(data, "utf-8"))
