#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from .leddisplay import LedDisplay
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service
from ..bluetoothdevice import BluetoothDevice


class LedService:
    """
    Using the functions in this class you can turn LEDs on or off, or scroll a short text on the screen
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Checks whether the LED Bluetooth service is found on the connected micro:bit.

        Returns:
            true if the LED service was found, false if not.
        """
        return self._device.is_service_available(Service.LED)

    def show(self, led_display: LedDisplay):
        """
        Turn on the LEDs on the micro:bit as indicated in the LEDs parameter

        Args:
            led_display: the on/off state of the LEDs

        Raises:
            errors.BluetoothServiceNotFound: When the LED service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the led service is active but there was no way
                to write the LED display (normally does not occur)
        """
        self._device.write(Service.LED, Characteristic.LED_MATRIX_STATE, led_display.to_bytes())

    def read(self) -> LedDisplay:
        """
        Read the on/off values from the micro:bit LED display

        Returns:
            the on/off state of the LEDs

        Raises:
            errors.BluetoothServiceNotFound: When the LED service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the led service is active but there was no way
                to read the LED display (normally not present)
        """
        return LedDisplay.from_bytes(self._device.read(Service.LED, Characteristic.LED_MATRIX_STATE))

    def show_text(self, text: str):
        """
        Let the given text scroll by on the LED screen of the micro:bit. You can control the speed of scrolling
        through the scrolling delay methods.

        Args:
            text: The text to be displayed (maximum 20 characters)

        Raises:
            ValueError: if text contains more than 20 characters
            errors.BluetoothServiceNotFound: When the LED service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the led service is active but there was no way
                to write the LED text (normally does not occur)
        """
        octets = text.encode("utf-8")
        if len(octets) > 20:
            raise ValueError('Text too long, maximum 20 characters allowed')

        self._device.write(Service.LED, Characteristic.LED_TEXT, octets)

    def set_scrolling_delay(self, delay_in_millis: int):
        """
        Adjust how quickly text scrolls by on the LED screen.

        Args:
            delay_in_millis: the time it takes for 1 letter to pass across the screen in milliseconds

        Raises:
            errors.BluetoothServiceNotFound: When the LED service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the led service is active but there was no way
                to write the scrolling delay (normally does not occur)
        """
        self._device.write(Service.LED, Characteristic.SCROLLING_DELAY, delay_in_millis.to_bytes(2, 'little'))

    def get_scrolling_delay(self) -> int:
        """
        Return how quickly a text scrolls past the screen

        Returns:
             the time it takes for 1 letter to pass across the screen in milliseconds

        Raises:
            errors.BluetoothServiceNotFound: When the LED service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the led service is active but there was no way
                to read the scrolling delay (normally does not occur)
        """
        return int.from_bytes(self._device.read(Service.LED, Characteristic.SCROLLING_DELAY)[0:2], 'little')
