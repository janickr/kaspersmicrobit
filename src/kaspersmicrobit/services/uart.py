#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable

from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice, ByteData

PDU_BYTE_LIMIT = 20


class UartService:
    """
    Deze klasse bevat methodes om bytes of strings naar de microbit te verzenden of te ontvangen

    See Also: https://lancaster-university.github.io/microbit-docs/ble/uart-service/
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def receive(self, callback: Callable[[ByteData], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil wanneer er bytes worden verstuurd vanuit de microbit
        via de uart service

        Args:
            callback (Callable[[ByteData], None]): een functie wordt opgeroepen met de ontvangen bytes

        """
        self._device.notify(Characteristic.TX_CHARACTERISTIC, lambda sender, data: callback(data))

    def receive_string(self, callback: Callable[[str], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil wanneer er een string wordt verstuurd vanuit de microbit
        via de uart service

        Args:
            callback (Callable[[str], None]): een functie wordt opgeroepen met de ontvangen string

        """
        self.receive(UartService.to_string(callback))

    def send(self, data: ByteData):
        """
        Verzend bytes via de uart service naar de microbit

        Args:
            data (ByteData): de bytes die verzonden worden

        """
        for i in range(0, len(data), PDU_BYTE_LIMIT):
            self._device.write(Characteristic.RX_CHARACTERISTIC, data[i:i + PDU_BYTE_LIMIT])

    def send_string(self, string: str):
        """
        Verzend een string via de uart service naar de microbit

        Args:
            string (str): de string die verzonden wordt

        """
        self.send(UartService.from_string(string))

    @staticmethod
    def from_string(string: str) -> bytes:
        return string.encode("utf-8")

    @staticmethod
    def to_string(callback):
        return lambda data: callback(str(data, "utf-8"))
