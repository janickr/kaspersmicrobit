#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time

from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.leddisplay import Image, LedDisplay

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'
# example {

with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    # show one of the predefined LED images / toon een van de voorgedefieerde beelden
    microbit.led.show(Image.HEART)
    time.sleep(3)

    # scroll the text "Hello Kasper" on the microbit display / laat de tekst "Hello Kasper" op het scherm voorbijrollen
    microbit.led.show_text("Hello Kasper")
    time.sleep(10)

    # create your own image and show it on the display / maak je eigen afbeelding en toot die op de microbit
    microbit.led.show(LedDisplay.image("""
        . . . # #
        . . . # .
        . . . # .
        . # # # .
        . # . # .
    """))
    time.sleep(3)

    microbit.led.show(Image.HAPPY)
    time.sleep(3)
# }
