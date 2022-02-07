#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ..characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice, ByteData
from typing import Union, Literal
from dataclasses import dataclass


AccelerometerPeriod = Union[
    Literal[1], Literal[2], Literal[5], Literal[10], Literal[20], Literal[80], Literal[160], Literal[640]
]


@dataclass
class AccelerometerData:
    x: int
    y: int
    z: int

    @staticmethod
    def from_bytes(values: ByteData):
        return AccelerometerData(
            int.from_bytes(values[0:2], "little", signed=True),
            int.from_bytes(values[2:4], "little", signed=True),
            int.from_bytes(values[4:6], "little", signed=True)
        )


class AccelerometerService:
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def notify(self, callback):
        self._device.notify(Characteristic.ACCELEROMETER_DATA,
                            lambda sender, data: callback(AccelerometerData.from_bytes(data)))

    def read(self) -> AccelerometerData:
        return AccelerometerData.from_bytes(self._device.read(Characteristic.ACCELEROMETER_DATA))

    def set_period(self, period: AccelerometerPeriod):
        self._device.write(Characteristic.ACCELEROMETER_PERIOD, period.to_bytes(2, "little"))

    def read_period(self) -> int:
        return int.from_bytes(self._device.read(Characteristic.ACCELEROMETER_PERIOD)[0:2], "little")

