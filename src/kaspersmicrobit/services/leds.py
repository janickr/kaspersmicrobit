from typing import List, Literal, Union

from src.kaspersmicrobit.bluetoothdevice import ByteData

LedState = Union[Literal[0], Literal[1]]
LedRow = List[LedState, LedState, LedState, LedState, LedState]
LedMatrix = List[LedRow, LedRow, LedRow, LedRow, LedRow]

class Leds:
    def __init__(self, matrix: LedMatrix):
        self._matrix = matrix

    def get_leds(self) -> LedMatrix:
        return self._matrix

    def led(self, row: int, column: int):
        return self._matrix[row-1][column-1]

    def set_led(self, row: int, column: int, state: LedState):
        self._matrix[row-1][column-1] = state

    def to_bytes(self):
        result = bytearray(5)
        for row in self._matrix:
            octet = row[4] \
                    | row[3] << 1 \
                    | row[2] << 2 \
                    | row[1] << 3 \
                    | row[0] << 4
            result.append(octet)

        return result


    @staticmethod
    def from_bytes(value: ByteData):
        result: LedMatrix = []
        for i in range(5):
            octet = value[i]
            row: LedRow = [
                (octet >> 4) & 1,
                (octet >> 3) & 1,
                (octet >> 2) & 1,
                (octet >> 1) & 1,
                octet & 1
            ]
            result.append(row)
        return Leds(result)

    @staticmethod
    def image(string: str, on='#', off='.'):
        image = []
        for s in string:
            if s == on:
                image.append(1)
            elif s == off:
                image.append(0)

        if len(image) != 25:
            raise ValueError("Image should contain 25 LEDs")

        return Leds(image.)


HEART : Leds = Leds.image("""
 . # . # .
 # # # # #
 # # # # #
 . # # # .
 . . # . .
""")