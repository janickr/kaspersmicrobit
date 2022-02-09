#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Literal, Union, List

from .leds import Leds
from ..characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice


class LedService:
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def show(self, leds: Leds):
        self._device.write(Characteristic.LED_MATRIX_STATE, leds.to_bytes())

    def read(self) -> Leds:
        return Leds.from_bytes(self._device.read(Characteristic.LED_MATRIX_STATE))

    def show_text(self, text: str):
        octets = text.encode("utf-8")
        for i in range(0, len(octets), 20):
            self._device.write(Characteristic.LED_TEXT, octets[i:i+20])

    def set_scrolling_delay(self, delay_in_milis: int):
        self._device.write(Characteristic.SCROLLING_DELAY, delay_in_milis.to_bytes(2, 'little'))

    def get_scrolling_delay(self) -> int:
        return int.from_bytes(self._device.read(Characteristic.SCROLLING_DELAY)[0:2], 'little')