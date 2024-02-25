#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable
from enum import IntEnum
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service
from ..bluetoothdevice import BluetoothDevice

ButtonCallback = Callable[[str], None]
"""
A function with 1 argument (te button "A" or "B")
"""


class ButtonState(IntEnum):
    """
    All possible states of a button:

    - RELEASE: released
    - PRESS: pressed
    - LONG_PRESS: pressed for at least 2 seconds
    """
    RELEASE = 0
    PRESS = 1
    PRESS_LONG = 2


class ButtonService:
    """
    This class contains the functions that you can access related to the A and B buttons of the micro:bit

    These are all options offered by the Bluetooth button service

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

    def is_available(self) -> bool:
        """
        Checks whether the Bluetooth service button is found on the connected micro:bit.

        Returns:
            true if the button service was found, false if not.
        """
        return self._device.is_service_available(Service.BUTTON)

    def on_button_a(self, press: ButtonCallback = None, long_press: ButtonCallback = None,
                    release: ButtonCallback = None):
        """
        You can call this function if you want to be notified when the A button of your micro:bit is pressed
        (press), long pressed (long_press) or released (release)

        A function that you can pass as an argument is a function with 1 string parameter. This function will be
        called with the button name as argument.

        Args:
            press (ButtonCallback): a function called when the A button is pressed
            long_press (ButtonCallback): a function that is called when pressed for a long time (at least 2 seconds).
                the A button is pressed
            release (ButtonCallback): a function called when the A button is released

        Raises:
            errors.BluetoothServiceNotFound: When the button service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the button service is running but there was no way to get the
                activate notifications for button A (normally does not occur)
        """
        self._device.notify(Service.BUTTON, Characteristic.BUTTON_A,
                            ButtonService._create_button_callback('A', press, long_press, release))

    def on_button_b(self, press: ButtonCallback = None, long_press: ButtonCallback = None,
                    release: ButtonCallback = None):
        """
        You can call this function if you want to be notified when the B button of your micro:bit is pressed
        (press), long pressed (long_press) or released (release)

        A function that you can pass as an argument is a function with 1 string parameter. This function will be
        called with the button name as argument.

        Args:
            press (ButtonCallback): a function called when the B button is pressed
            long_press (ButtonCallback): a function that is called when pressed for a long time (at least 2 seconds).
                the B button is pressed
            release (ButtonCallback): a function called when the B button is released

        Raises:
            errors.BluetoothServiceNotFound: When the button service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the button service is running but there was no way to get the
                activate notifications for button B (normally does not occur)
        """
        self._device.notify(Service.BUTTON, Characteristic.BUTTON_B,
                            ButtonService._create_button_callback('B', press, long_press, release))

    def read_button_a(self) -> ButtonState:
        """
        Returns the state of the A button

        Returns:
            The state of the A button (RELEASE, PRESS or LONG_PRESS)

        Raises:
            errors.BluetoothServiceNotFound: When the button service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the button service is running but there was no way to
                read the state of button A (normally does not occur)
        """
        return ButtonState(self._device.read(Service.BUTTON, Characteristic.BUTTON_A)[0])

    def read_button_b(self) -> ButtonState:
        """
        Returns the state of the B button

        Returns(ButtonState):
            The state of the B button (RELEASE, PRESS or LONG_PRESS)

        Raises:
            errors.BluetoothServiceNotFound: When the button service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the button service is running but there was no way to
                read the state of button B (normally does not occur)
        """
        return ButtonState(self._device.read(Service.BUTTON, Characteristic.BUTTON_B)[0])
