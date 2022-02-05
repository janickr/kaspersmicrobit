#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time

from kaspersmicrobit import KaspersMicrobit

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


def pressed(button):
    print(f"button {button} pressed")


def pressed_long(button):
    print(f"button {button} pressed long")


def released(button):
    print(f"button {button} released")


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.buttons.on_button_a(press=pressed, long_press=pressed_long, up=released)
    microbit.buttons.on_button_b(press=pressed, long_press=pressed_long, up=released)
    time.sleep(10)
