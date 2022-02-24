#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from .leddisplay import LedDisplay
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice


class LedService:
    """
    Met de functies in deze klasse kan je leds aan of uit zetten, of een korte tekst laten scrollen op het scherm
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def show(self, led_display: LedDisplay):
        """
        Zet de leds op de microbit aan zoals de leds parameter aangeeft
        Args:
            led_display: de aan/uit staat van de leds
        """
        self._device.write(Characteristic.LED_MATRIX_STATE, led_display.to_bytes())

    def read(self) -> LedDisplay:
        return LedDisplay.from_bytes(self._device.read(Characteristic.LED_MATRIX_STATE))

    def show_text(self, text: str):
        """
        Laat de gegeven tekst voorbij scrollen op het led scherm van de microbit. De snelheid van het scrollen kan je
        instellen via de scrolling delay.

        Args:
            text: De te tonen tekst (maximum 20 tekens)

        Raises:
            ValueError: indien text meer dan 20 tekens bevat
        """
        octets = text.encode("utf-8")
        if len(octets) > 20:
            raise ValueError('Text too long, maximum 20 characters allowed')

        self._device.write(Characteristic.LED_TEXT, octets)

    def set_scrolling_delay(self, delay_in_milis: int):
        """
        Stel in hoe snel een tekst voorbijrolt op het led scherm.

        Args:
            delay_in_milis:  de tijd die 1 letter er over doet om over het scherm voorbij te komen in milliseconden
        """
        self._device.write(Characteristic.SCROLLING_DELAY, delay_in_milis.to_bytes(2, 'little'))

    def get_scrolling_delay(self) -> int:
        """
        Lees de hoe snel een tekst voorbijscrolt over het scherm

        Returns (int):
             de tijd die 1 letter er over doet om over het scherm voorbij te komen in milliseconden
        """
        return int.from_bytes(self._device.read(Characteristic.SCROLLING_DELAY)[0:2], 'little')
