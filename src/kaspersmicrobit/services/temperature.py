#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ..characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice


class TemperatureService:
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def notify(self, callback):
        self._device.notify(Characteristic.TEMPERATURE, lambda sender, data: callback(data[0]))

    def read(self) -> int:
        return self._device.read(Characteristic.TEMPERATURE)[0]

    def set_period(self, period: int):
        self._device.write(Characteristic.TEMPERATURE_PERIOD, period.to_bytes(2, "little"))

    def read_period(self) -> int:
        return int.from_bytes(self._device.read(Characteristic.TEMPERATURE_PERIOD)[0:2], "little")
