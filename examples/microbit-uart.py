#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import time

from kaspersmicrobit import KaspersMicrobit

logging.basicConfig(level=logging.INFO)

# example {


def print_received_string(string: str):
    print(f"Received from microbit: '{string}'")


with KaspersMicrobit.find_one_microbit() as microbit:
    # listen for strings sent by the micro:bit / luister naar tekst die verzonden wordt door de micro:bit
    microbit.uart.receive_string(print_received_string)

    # send a string to the micro:bit / verzend tekst naar de micro:bit
    microbit.uart.send_string("Hello Kasper!!!\n")

    time.sleep(20)
# }
