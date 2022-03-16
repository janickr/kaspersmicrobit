#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from kaspersmicrobit.services.leddisplay import LedDisplay


def test_get_led_returns_true_if_led_is_on():
    image = LedDisplay.image("""
     . # . . .
     . . . . .
     . . . . .
     . . . . .
     . . . . .
    """)

    assert image.led(1, 2)


def test_get_led_returns_false_if_led_is_off():
    image = LedDisplay.image("""
     . # . . .
     . . . . .
     . . . . .
     . . . . .
     . . . . .
    """)

    assert not image.led(1, 1)


def test_set_led_can_turn_led_on():
    image = LedDisplay()
    image.set_led(1, 2, True)

    assert image.led(1, 2)


def test_set_led_can_turn_led_off():
    image = LedDisplay()
    image.set_led(1, 2, True)

    image.set_led(1, 2, False)

    assert not image.led(1, 2)


def test_can_choose_characters_for_on_and_off_leds():
    image = LedDisplay.image("""
 0 1 0 1 0
 1 1 1 1 1
 1 1 1 1 1
 0 1 1 1 0
 0 0 1 0 0
""", on='1', off='0')

    assert image.__str__() == """
 . # . # .
 # # # # #
 # # # # #
 . # # # .
 . . # . .
"""


def test_to_bytes_each_led_row_is_a_byte():
    image = LedDisplay.image("""
     . # . . .
     . . # . .
     # . # . .
     . . . # .
     . . . . #
    """)

    assert image.to_bytes() == bytearray.fromhex("08 04 14 02 01")


def test_from_bytes_each_led_row_is_a_byte():
    image = LedDisplay(bytearray.fromhex("08 04 14 02 01"))

    assert image.__str__() == """
 . # . . .
 . . # . .
 # . # . .
 . . . # .
 . . . . #
"""


def test_roundtrip_from_string_to_bytes_new_image_from_bytes_back_to_string_should_be_equal_string():
    image1 = LedDisplay.image("""
 . # . # .
 # # # # #
 # # # # #
 . # # # .
 . . # . .
""")

    image2 = LedDisplay.from_bytes(image1.to_bytes())
    assert image2.__str__() == """
 . # . # .
 # # # # #
 # # # # #
 . # # # .
 . . # . .
"""


def test_image_should_not_have_less_than_25_leds():
    with pytest.raises(ValueError, match="Image should contain 25 LEDs"):
        LedDisplay.image("""
               . . . .
             . . . . .
             . . . . .
             . . . . .
             . . . . .
            """)


def test_image_should_not_have_more_than_25_leds():
    with pytest.raises(ValueError, match="Image should contain 25 LEDs"):
        LedDisplay.image("""
             . . . . .
             . . . . .
             . . . . .
             . . . . .
             . . . . . .
            """)
