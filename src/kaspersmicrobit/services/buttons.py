#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable
from enum import IntEnum
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice

ButtonCallback = Callable[[str], None]
"""
Een functie met 1 argument (de knop "A" of "B")
"""


class ButtonState(IntEnum):
    """
    Alle mogelijke toestanden van een knop:
        - RELEASE: losgelaten
        - PRESS: ingedrukt
        - LONG_PRESS: minstens 2 seconden lang ingedrukt
    """
    RELEASE = 0
    PRESS = 1
    PRESS_LONG = 2


class ButtonService:
    """
    Deze klasse bevat de functies die je kan aanspreken in verband met de A en B knoppen van de microbit

    Dit zijn alle mogelijkheden aangeboden door de bluetooth button service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/button-service/
    """

    def __init__(self, device: BluetoothDevice):
        self._device = device

    @staticmethod
    def _create_button_callback(button: str, press, long_press, up):
        def button_callback(sender, data):
            if ButtonState.RELEASE == data[0] and up:
                up(button)
            elif ButtonState.PRESS == data[0] and press:
                press(button)
            elif ButtonState.PRESS_LONG == data[0] and long_press:
                long_press(button)
            else:
                pass
        return button_callback

    def on_button_a(self, press: ButtonCallback = None, long_press: ButtonCallback = None,
                    release: ButtonCallback = None):
        """
        Deze functie kan je oproepen wanneer je verwittigd wil worden wanneer de A knop van je microbit ingedrukt
        (press), lang ingedrukt (long_press) of losgelaten (release)

        De functies die je kan meegeven als argument zijn functies met 1 string parameter. Deze functies zullen worden
        opgeroepen met de naam van de knop als argument.

        Args:
            press (ButtonCallback): een functie die wordt opgeroepen wanneer er op de A knop gedrukt wordt
            long_press (ButtonCallback): een functie die wordt opgeroepen wanneer er lang (minstens 2 seconden) op
                de A knop gedrukt wordt
            release (ButtonCallback): een functie die wordt opgeroepen wanneer de A knop wordt losgelaten
        """
        self._device.notify(Characteristic.BUTTON_A,
                            ButtonService._create_button_callback('A', press, long_press, release))

    def on_button_b(self, press: ButtonCallback = None, long_press: ButtonCallback = None,
                    release: ButtonCallback = None):
        """
        Deze functie kan je oproepen wanneer je verwittigd wil worden wanneer de B knop van je microbit ingedrukt
        (press), lang ingedrukt (long_press) of losgelaten (release)

        De functies die je kan meegeven als argument zijn functies met 1 string parameter. Deze functies zullen worden
        opgeroepen met de naam van de knop als argument.

        Args:
            press (ButtonCallback): een functie die wordt opgeroepen wanneer er op de B knop gedrukt wordt
            long_press (ButtonCallback): een functie die wordt opgeroepen wanneer er lang (minstens 2 seconden) op
                de B knop gedrukt wordt
            release (ButtonCallback): een functie die wordt opgeroepen wanneer de B knop wordt losgelaten
        """
        self._device.notify(Characteristic.BUTTON_B,
                            ButtonService._create_button_callback('B', press, long_press, release))

    def read_button_a(self):
        """
        Geef de toestand van de A knop

        Returns (ButtonState):
            De toestand van de A knop (RELEASE, PRESS of LONG_PRESS)
        """
        return ButtonState(self._device.read(Characteristic.BUTTON_A)[0])

    def read_button_b(self):
        """
        Geef de toestand van de B knop

        Returns (ButtonState):
            De toestand van de B knop (RELEASE, PRESS of LONG_PRESS)
        """
        return ButtonState(self._device.read(Characteristic.BUTTON_B)[0])
