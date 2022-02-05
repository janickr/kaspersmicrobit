#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ..characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice
from enum import IntEnum


class ButtonState(IntEnum):
    NOT_PRESSED = 0
    PRESS = 1
    PRESS_LONG = 2


class ButtonService:
    def __init__(self, device: BluetoothDevice):
        self._device = device

    @staticmethod
    def _create_button_callback(button: str, press, long_press, up):
        def button_callback(sender, data):
            if ButtonState.NOT_PRESSED == data[0] and up:
                up(button)
            elif ButtonState.PRESS == data[0] and press:
                press(button)
            elif ButtonState.PRESS_LONG == data[0] and long_press:
                long_press(button)
            else:
                pass
        return button_callback

    def on_button_a(self, press=None, long_press=None, up=None):
        self._device.notify(Characteristic.BUTTON_A,
                            ButtonService._create_button_callback('A', press, long_press, up))

    def on_button_b(self, press=None, long_press=None, up=None):
        self._device.notify(Characteristic.BUTTON_B,
                            ButtonService._create_button_callback('B', press, long_press, up))

    def read_button_a(self):
        return ButtonState(self._device.read(Characteristic.BUTTON_A)[0])

    def read_button_b(self):
        return ButtonState(self._device.read(Characteristic.BUTTON_B)[0])
