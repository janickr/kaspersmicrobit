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
    Deze klasse bevat methodes om bytes of strings naar de micro:bit te verzenden of te ontvangen

    See Also: https://lancaster-university.github.io/microbit-docs/ble/uart-service/
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Kijkt na of de uart bluetooth service gevonden wordt op de geconnecteerde micro:bit.

        Returns:
            true als de uart service gevonden werd, false indien niet.
        """
        return self._device.is_service_available(Service.UART)

    def receive(self, callback: Callable[[ByteData], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil wanneer er bytes worden verstuurd vanuit de micro:bit
        via de uart service

        Args:
            callback (Callable[[ByteData], None]): een functie wordt opgeroepen met de ontvangen bytes

        Raises:
            BluetoothServiceNotFound: Wanneer de uart service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de uart service actief is, maar er geen manier was
                om de notificaties van uart data te activeren (komt normaal gezien niet voor)
        """
        self._device.notify(Service.UART, Characteristic.TX_CHARACTERISTIC, lambda sender, data: callback(data))

    def receive_string(self, callback: Callable[[str], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil wanneer er een string wordt verstuurd vanuit de micro:bit
        via de uart service

        Args:
            callback (Callable[[str], None]): een functie wordt opgeroepen met de ontvangen string

        Raises:
            BluetoothServiceNotFound: Wanneer de uart service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de uart service actief is, maar er geen manier was
                om de notificaties van uart data te activeren (komt normaal gezien niet voor)
        """
        self.receive(UartService.to_string(callback))

    def send(self, data: ByteData):
        """
        Verzend bytes via de uart service naar de micro:bit

        Args:
            data (ByteData): de bytes die verzonden worden

        Raises:
            BluetoothServiceNotFound: Wanneer de uart service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de uart service actief is, maar er geen manier was
                om data via de uart service te verzenden (komt normaal gezien niet voor)
        """
        for i in range(0, len(data), PDU_BYTE_LIMIT):
            self._device.write(Service.UART, Characteristic.RX_CHARACTERISTIC, data[i:i + PDU_BYTE_LIMIT])

    def send_string(self, string: str):
        """
        Verzend een string via de uart service naar de micro:bit

        Args:
            string (str): de string die verzonden wordt

        Raises:
            BluetoothServiceNotFound: Wanneer de uart service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de uart service actief is, maar er geen manier was
                om data via de uart service te verzenden (komt normaal gezien niet voor)
        """
        self.send(UartService.from_string(string))

    @staticmethod
    def from_string(string: str) -> bytes:
        return string.encode("utf-8")

    @staticmethod
    def to_string(callback):
        return lambda data: callback(str(data, "utf-8"))
