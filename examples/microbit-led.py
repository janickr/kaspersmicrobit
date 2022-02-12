#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time

from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.leddisplay import Image, LedDisplay

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'
# example {

with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.led.show(Image.HEART)
    time.sleep(3)
    microbit.led.show_text("Hello kasper")
    time.sleep(15)
    microbit.led.show(LedDisplay.image("""
        . . . # #
        . . . # .
        . .   # .
        . # # # .
        . # . # .
    """))
    time.sleep(3)
    microbit.led.show(Image.HAPPY)
    time.sleep(3)
# }
