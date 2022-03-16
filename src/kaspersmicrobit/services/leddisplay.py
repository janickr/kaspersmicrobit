#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from ..bluetoothdevice import ByteData


class LedDisplay:
    """
    Een klasse die het LED scherm van de microbit voorstelt.
    De LED linksboven op de microbit is de LED op rij 1, kolom 1
    De LED rechtsbeneden op de microbit is de LED op rij 5, kolom 5
    """
    def __init__(self, _bytes: bytearray = None):
        """
        Maakt display met alle leds uit
        """
        self._display = _bytes if _bytes else bytearray(5)

    def led(self, row: int, column: int) -> bool:
        """
        Geeft aan of dat een LED op de gegeven rij en kolom aan of uit is

        Args:
            row int: de rij van de LED (geldige waarden zijn 1 tot en met 5)
            column int: de kolom van de LED (geldige waarden zijn 1 tot en met 5)

        Returns (bool):
            True wanneer de LED aan staat, False als de LED uit staat
        """
        return ((self._display[row-1] >> (5 - column)) & 1) == 1

    def set_led(self, row: int, column: int, on: bool):
        """
        Zet een LED op de gegeven rij en kolom aan of uit

        Args:
            row int: de rij van de LED (geldige waarden zijn 1 tot en met 5)
            column int: de kolom van de LED (geldige waarden zijn 1 tot en met 5)
            on bool: indien True word de LED aan gezet, indien False uit

        Returns (bool):
            True wanneer de LED aan staat, False als de LED uit staat
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
    def image(string: str, on='#', off='.'):
        """
        Maakt een LedDisplay van een string.

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

        Welke tekens gebruikt worden voor een LED die 'aan' of 'uit' is kan je zelf kiezen met de 'on' en 'of'
        parameters. De gegeven string moet exact 25 'on' en 'off' waarden bevatten, voor elke LED 1.

        Args:
            string: de string die het LED scherm voorstelt
            on: de letter die een LED voorstelt die 'aan' is ('#' indien niet ingevuld)
            off: de letter die een LED voorstelt die 'uit' is ('.' indien niet ingevuld)

        Returns (LedDisplay):
            Een LedDisplay die de gegeven string image voorstelt

        Raises:
            ValueError: Indien de gegeven string niet exact 25 on/off waarden bevat
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
