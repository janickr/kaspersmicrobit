#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time

from kaspersmicrobit import KaspersMicrobit

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'
# example {


def print_received_string(string: str):
    print(f"Received from microbit: '{string}'")


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    # You can listen for strings sent by the microbit
    microbit.uart.receive_string(print_received_string)

    # You can send a string to the microbit
    microbit.uart.send_string("Hello kasper, this is working out very well\n")

    time.sleep(25)
# }
