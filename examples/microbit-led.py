#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import time

from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.leddisplay import Image, LedDisplay

logging.basicConfig(level=logging.INFO)


# example {

with KaspersMicrobit.find_one_microbit() as microbit:
    # show one of the predefined LED images / toon een van de voorgedefinieerde beelden
    microbit.led.show(Image.HEART)
    time.sleep(3)

    # scroll the text "Hello Kasper" on the micro:bit display / laat de tekst "Hello Kasper" op het scherm voorbijrollen
    microbit.led.show_text("Hello Kasper")
    time.sleep(10)

    # create your own image and show it on the display / maak je eigen afbeelding en toot die op de micro:bit
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
