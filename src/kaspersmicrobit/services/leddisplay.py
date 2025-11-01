#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from ..bluetoothdevice import ByteData


class LedDisplay:
    """
    A class representing the LED screen of the micro:bit.
    The LED on the top left of the micro:bit is the LED on row 1, column 1
    The bottom right LED on the micro:bit is the LED in row 5, column 5
    """
    def __init__(self, _bytes: bytearray = None):
        """
        Create a display with all LEDs off
        """
        self._display = _bytes if _bytes else bytearray(5)

    def led(self, row: int, column: int) -> bool:
        """
        Indicates whether an LED on the given row and column is on or off

        Args:
            row (int): the row of the LED (valid values are 1 to 5)
            column (int): the column of the LED (valid values are 1 to 5)

        Returns:
            True when the LED is on, False when the LED is off
        """
        return ((self._display[row-1] >> (5 - column)) & 1) == 1

    def set_led(self, row: int, column: int, on: bool = True):
        """
        Turn an LED on or off on the given row and column

        Args:
            row (int): the row of the LED (valid values are 1 to 5)
            column (int): the column of the LED (valid values are 1 to 5)
            on (bool): if True the LED is turned on, if False it is turned off
        """
        if on:
            self._display[row-1] |= 1 << (5 - column)
        else:
            self._display[row-1] &= ~(1 << (5 - column))

    def to_bytes(self) -> bytearray:
        return self._display

    @staticmethod
    def from_bytes(value: ByteData):
        return LedDisplay(bytearray(value))

    @staticmethod
    def image(string: str, on: str = '#', off: str = '.') -> 'LedDisplay':
        """
        Creates an LedDisplay given a string.

        Example:

        ```python
        HEART: LedDisplay = LedDisplay.image('''
            . # . # .
            # # # # #
            # # # # #
            . # # # .
            . . # . .
        ''')
        ```

        You can choose which characters are used for an LED that is 'on' or 'off' with the 'on' and 'off'
        parameters. The given string must contain exactly 25 'on' and 'off' values, 1 for each LED.

        Args:
            string: the string representing the LED screen
            on: the letter representing an LED that is 'on' ('#' if left blank)
            off: the letter representing an LED that is 'off' ('.' if left blank)

        Returns:
            An LedDisplay representing the given string image

        Raises:
            ValueError: If the given string does not contain exactly 25 on/off values
        """
        image: List[bool] = []
        for s in string:
            if s == on:
                image.append(True)
            elif s == off:
                image.append(False)

        if len(image) != 25:
            raise ValueError("Image should contain 25 LEDs")

        leds = LedDisplay()
        for row in range(1, 6):
            for column in range(1, 6):
                leds.set_led(row, column, image[(row-1)*5+column-1])

        return leds

    def __str__(self):
        string = "\n"
        for row in range(1, 6):
            for column in range(1, 6):
                string += ' #' if self.led(row, column) else ' .'
            string += '\n'
        return string


class Image:
    HEART: LedDisplay = LedDisplay.image("""
        . # . # .
        # # # # #
        # # # # #
        . # # # .
        . . # . .
    """)

    HEART_SMALL: LedDisplay = LedDisplay.image("""
        . . . . .
        . # . # .
        . # # # .
        . . # . .
        . . . . .
    """)

    HAPPY: LedDisplay = LedDisplay.image("""
        . . . . .
        . # . # .
        . . . . .
        # . . . #
        . # # # .
    """)

    SMILE: LedDisplay = LedDisplay.image("""
        . . . . .
        . . . . .
        . . . . .
        # . . . #
        . # # # .
    """)

    SAD: LedDisplay = LedDisplay.image("""
        . . . . .
        . # . # .
        . . . . .
        . # # # .
        # . . . #
    """)

    CONFUSED: LedDisplay = LedDisplay.image("""
        . . . . .
        . # . # .
        . . . . .
        . # . # .
        # . # . #
    """)

    ANGRY: LedDisplay = LedDisplay.image("""
        # . . . #
        . # . # .
        . . . . .
        # # # # #
        # . # . #
    """)

    ASLEEP: LedDisplay = LedDisplay.image("""
        . . . . .
        # # . # #
        . . . . .
        . # # # .
        . . . . .
    """)

    SURPRISED: LedDisplay = LedDisplay.image("""
        . # . # .
        . . . . .
        . . # . .
        . # . # .
        . . # . .
    """)

    SILLY: LedDisplay = LedDisplay.image("""
        # . . . #
        . . . . .
        # # # # #
        . . # . #
        . . # # #
    """)

    FABULOUS: LedDisplay = LedDisplay.image("""
        # # # # #
        # # . # #
        . . . . .
        . # . # .
        . # # # .
    """)

    MEH: LedDisplay = LedDisplay.image("""
        . # . # .
        . . . . .
        . . . # .
        . . # . .
        . # . . .
    """)

    YES: LedDisplay = LedDisplay.image("""
        . . . . .
        . . . . #
        . . . # .
        # . # . .
        . # . . .
    """)

    NO: LedDisplay = LedDisplay.image("""
        # . . . #
        . # . # .
        . . # . .
        . # . # .
        # . . . #
    """)

    CLOCK12: LedDisplay = LedDisplay.image("""
        . . # . .
        . . # . .
        . . # . .
        . . . . .
        . . . . .
    """)

    CLOCK1: LedDisplay = LedDisplay.image("""
        . . . # .
        . . . # .
        . . # . .
        . . . . .
        . . . . .
    """)

    CLOCK2: LedDisplay = LedDisplay.image("""
        . . . . .
        . . . # #
        . . # . .
        . . . . .
        . . . . .
    """)

    CLOCK3: LedDisplay = LedDisplay.image("""
        . . . . .
        . . . . .
        . . # # #
        . . . . .
        . . . . .
    """)

    CLOCK4: LedDisplay = LedDisplay.image("""
        . . . . .
        . . . . .
        . . # . .
        . . . # #
        . . . . .
    """)

    CLOCK5: LedDisplay = LedDisplay.image("""
        . . . . .
        . . . . .
        . . # . .
        . . . # .
        . . . # .
    """)

    CLOCK6: LedDisplay = LedDisplay.image("""
        . . . . .
        . . . . .
        . . # . .
        . . # . .
        . . # . .
    """)

    CLOCK7: LedDisplay = LedDisplay.image("""
        . . . . .
        . . . . .
        . . # . .
        . # . . .
        . # . . .
    """)

    CLOCK8: LedDisplay = LedDisplay.image("""
        . . . . .
        . . . . .
        . . # . .
        # # . . .
        . . . . .
    """)

    CLOCK9: LedDisplay = LedDisplay.image("""
        . . . . .
        . . . . .
        # # # . .
        . . . . .
        . . . . .
    """)

    CLOCK10: LedDisplay = LedDisplay.image("""
        . . . . .
        # # . . .
        . . # . .
        . . . . .
        . . . . .
    """)

    CLOCK11: LedDisplay = LedDisplay.image("""
        . # . . .
        . # . . .
        . . # . .
        . . . . .
        . . . . .
    """)

    ARROW_N: LedDisplay = LedDisplay.image("""
        . . # . .
        . # # # .
        # . # . #
        . . # . .
        . . # . .
    """)

    ARROW_NE: LedDisplay = LedDisplay.image("""
        . . # # #
        . . . # #
        . . # . #
        . # . . .
        # . . . .
    """)

    ARROW_E: LedDisplay = LedDisplay.image("""
        . . # . .
        . . . # .
        # # # # #
        . . . # .
        . . # . .
    """)

    ARROW_SE: LedDisplay = LedDisplay.image("""
        # . . . .
        . # . . .
        . . # . #
        . . . # #
        . . # # #
    """)

    ARROW_S: LedDisplay = LedDisplay.image("""
        . . # . .
        . . # . .
        # . # . #
        . # # # .
        . . # . .
    """)

    ARROW_SW: LedDisplay = LedDisplay.image("""
        . . . . #
        . . . # .
        # . # . .
        # # . . .
        # # # . .
    """)

    ARROW_W: LedDisplay = LedDisplay.image("""
        . . # . .
        . # . . .
        # # # # #
        . # . . .
        . . # . .
    """)

    ARROW_NW: LedDisplay = LedDisplay.image("""
        # # # . .
        # # . . .
        # . # . .
        . . . # .
        . . . . #
    """)

    TRIANGLE: LedDisplay = LedDisplay.image("""
        . . . . .
        . . # . .
        . # . # .
        # # # # #
        . . . . .
    """)

    TRIANGLE_LEFT: LedDisplay = LedDisplay.image("""
        # . . . .
        # # . . .
        # . # . .
        # . . # .
        # # # # #
    """)

    CHESSBOARD: LedDisplay = LedDisplay.image("""
        . # . # .
        # . # . #
        . # . # .
        # . # . #
        . # . # .
    """)

    DIAMOND: LedDisplay = LedDisplay.image("""
        . . # . .
        . # . # .
        # . . . #
        . # . # .
        . . # . .
    """)

    DIAMOND_SMALL: LedDisplay = LedDisplay.image("""
        . . . . .
        . . # . .
        . # . # .
        . . # . .
        . . . . .
    """)

    SQUARE: LedDisplay = LedDisplay.image("""
        # # # # #
        # . . . #
        # . . . #
        # . . . #
        # # # # #
    """)

    SQUARE_SMALL: LedDisplay = LedDisplay.image("""
        . . . . .
        . # # # .
        . # . # .
        . # # # .
        . . . . .
    """)

    RABBIT: LedDisplay = LedDisplay.image("""
        # . # . .
        # . # . .
        # # # # .
        # # . # .
        # # # # .
    """)

    COW: LedDisplay = LedDisplay.image("""
        # . . . #
        # . . . #
        # # # # #
        . # # # .
        . . # . .
    """)

    MUSIC_CROTCHET: LedDisplay = LedDisplay.image("""
        . . # . .
        . . # . .
        . . # . .
        # # # . .
        # # # . .
    """)

    MUSIC_QUAVER: LedDisplay = LedDisplay.image("""
        . . # . .
        . . # # .
        . . # . #
        # # # . .
        # # # . .
    """)

    MUSIC_QUAVERS: LedDisplay = LedDisplay.image("""
        . # # # #
        . # . . #
        . # . . #
        # # . # #
        # # . # #
    """)

    PITCHFORK: LedDisplay = LedDisplay.image("""
        # . # . #
        # . # . #
        # # # # #
        . . # . .
        . . # . .
    """)

    XMAS: LedDisplay = LedDisplay.image("""
        . . # . .
        . # # # .
        . . # . .
        . # # # .
        # # # # #
    """)

    PACMAN: LedDisplay = LedDisplay.image("""
        . # # # #
        # # . # .
        # # # . .
        # # # # .
        . # # # #
    """)

    TARGET: LedDisplay = LedDisplay.image("""
        . . # . .
        . # # # .
        # # . # #
        . # # # .
        . . # . .
    """)

    # The following images were designed by Abbie Brooks.

    TSHIRT: LedDisplay = LedDisplay.image("""
        # # . # #
        # # # # #
        . # # # .
        . # # # .
        . # # # .
    """)

    ROLLERSKATE: LedDisplay = LedDisplay.image("""
        . . . # #
        . . . # #
        # # # # #
        # # # # #
        . # . # .
    """)

    DUCK: LedDisplay = LedDisplay.image("""
        . # # . .
        # # # . .
        . # # # #
        . # # # .
        . . . . .
    """)

    HOUSE: LedDisplay = LedDisplay.image("""
        . . # . .
        . # # # .
        # # # # #
        . # # # .
        . # . # .
    """)

    TORTOISE: LedDisplay = LedDisplay.image("""
        . . . . .
        . # # # .
        # # # # #
        . # . # .
        . . . . .
    """)

    BUTTERFLY: LedDisplay = LedDisplay.image("""
        # # . # #
        # # # # #
        . . # . .
        # # # # #
        # # . # #
    """)

    STICKFIGURE: LedDisplay = LedDisplay.image("""
        . . # . .
        # # # # #
        . . # . .
        . # . # .
        # . . . #
    """)

    GHOST: LedDisplay = LedDisplay.image("""
        # # # # #
        # . # . #
        # # # # #
        # # # # #
        # . # . #
    """)

    SWORD: LedDisplay = LedDisplay.image("""
        . . # . .
        . . # . .
        . . # . .
        . # # # .
        . . # . .
    """)

    GIRAFFE: LedDisplay = LedDisplay.image("""
        # # . . .
        . # . . .
        . # . . .
        . # # # .
        . # . # .
    """)

    SKULL: LedDisplay = LedDisplay.image("""
        . # # # .
        # . # . #
        # # # # #
        . # # # .
        . # # # .
    """)

    UMBRELLA: LedDisplay = LedDisplay.image("""
        . # # # .
        # # # # #
        . . # . .
        # . # . .
        . # # . .
    """)

    SNAKE: LedDisplay = LedDisplay.image("""
        # # . . .
        # # . # #
        . # . # .
        . # # # .
        . . . . .
    """)

    SCISSORS: LedDisplay = LedDisplay.image("""
        # # . . #
        # # . # .
        . . # . .
        # # . # .
        # # . . #
    """)
