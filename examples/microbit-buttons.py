#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import time

from kaspersmicrobit import KaspersMicrobit

logging.basicConfig(level=logging.INFO)

# example {


def pressed(button):
    print(f"button {button} pressed")


def pressed_long(button):
    print(f"button {button} pressed long")


def released(button):
    print(f"button {button} released")


with KaspersMicrobit.find_one_microbit() as microbit:
    # read the state of the buttons / lees de toestant van de knoppen
    print(f"button A state is now: {microbit.buttons.read_button_a()}")
    print(f"button B state is now: {microbit.buttons.read_button_b()}")

    # listen for button events / luister naar drukken op knoppen
    microbit.buttons.on_button_a(press=pressed, long_press=pressed_long, release=released)
    microbit.buttons.on_button_b(press=pressed, long_press=pressed_long, release=released)

    time.sleep(15)

# }
