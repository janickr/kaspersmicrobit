#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from .leddisplay import LedDisplay
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service
from ..bluetoothdevice import BluetoothDevice


class LedService:
    """
    Met de functies in deze klasse kan je leds aan of uit zetten, of een korte tekst laten scrollen op het scherm
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Kijkt na of de led bluetooth service gevonden wordt op de geconnecteerde micro:bit.

        Returns:
            true als de led service gevonden werd, false indien niet.
        """
        return self._device.is_service_available(Service.LED)

    def show(self, led_display: LedDisplay):
        """
        Zet de leds op de micro:bit aan zoals de leds parameter aangeeft

        Args:
            led_display: de aan/uit staat van de leds

        Raises:
            BluetoothServiceNotFound: Wanneer de led service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de led service actief is, maar er geen manier was
                om de led display te schrijven (komt normaal gezien niet voor)
        """
        self._device.write(Service.LED, Characteristic.LED_MATRIX_STATE, led_display.to_bytes())

    def read(self) -> LedDisplay:
        """
        Lees de aan/uit waarden van de micro:bit led display

        Returns:
            de aan/uit staat van de leds

        Raises:
            BluetoothServiceNotFound: Wanneer de led service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de led service actief is, maar er geen manier was
                om de led display te lezen (komt normaal gezien niet voor)
        """
        return LedDisplay.from_bytes(self._device.read(Service.LED, Characteristic.LED_MATRIX_STATE))

    def show_text(self, text: str):
        """
        Laat de gegeven tekst voorbij scrollen op het led scherm van de micro:bit. De snelheid van het scrollen kan je
        instellen via de scrolling delay.

        Args:
            text: De te tonen tekst (maximum 20 tekens)

        Raises:
            ValueError: indien text meer dan 20 tekens bevat
            BluetoothServiceNotFound: Wanneer de led service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de led service actief is, maar er geen manier was
                om de led text te schrijven (komt normaal gezien niet voor)
        """
        octets = text.encode("utf-8")
        if len(octets) > 20:
            raise ValueError('Text too long, maximum 20 characters allowed')

        self._device.write(Service.LED, Characteristic.LED_TEXT, octets)

    def set_scrolling_delay(self, delay_in_millis: int):
        """
        Stel in hoe snel een tekst voorbijrolt op het led scherm.

        Args:
            delay_in_millis:  de tijd die 1 letter er over doet om over het scherm voorbij te komen in milliseconden

        Raises:
            BluetoothServiceNotFound: Wanneer de led service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de led service actief is, maar er geen manier was
                om de scrolling delay te schrijven (komt normaal gezien niet voor)
        """
        self._device.write(Service.LED, Characteristic.SCROLLING_DELAY, delay_in_millis.to_bytes(2, 'little'))

    def get_scrolling_delay(self) -> int:
        """
        Lees de hoe snel een tekst voorbijscrolt over het scherm

        Returns:
             de tijd die 1 letter er over doet om over het scherm voorbij te komen in milliseconden

        Raises:
            BluetoothServiceNotFound: Wanneer de led service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de led service actief is, maar er geen manier was
                om de scrolling delay te lezen (komt normaal gezien niet voor)
        """
        return int.from_bytes(self._device.read(Service.LED, Characteristic.SCROLLING_DELAY)[0:2], 'little')
