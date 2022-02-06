#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ..characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice, ByteData

PDU_BYTE_LIMIT = 20


class UartService:
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def receive(self, callback):
        self._device.notify(Characteristic.TX_CHARACTERISTIC, lambda sender, data: callback(data))

    def receive_string(self, callback):
        self.receive(UartService.to_string(callback))

    def send(self, data: ByteData):
        for i in range(0, len(data), PDU_BYTE_LIMIT):
            self._device.write(Characteristic.RX_CHARACTERISTIC, data[i:i + PDU_BYTE_LIMIT])

    def send_string(self, string: str):
        self.send(UartService.from_string(string))

    @staticmethod
    def from_string(string: str) -> bytes:
        return string.encode("utf-8")

    @staticmethod
    def to_string(callback):
        return lambda data: callback(str(data, "utf-8"))
