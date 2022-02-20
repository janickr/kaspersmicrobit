#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable

from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice


class TemperatureService:
    """
    Deze klasse bevat de functies die je kan aanspreken in verband met de temperatuur sensor van de microbit
    Deze sensor meet de temperatuur van de microbit in graden Celcius.

    Dit zijn alle mogelijkheden aangeboden door de bluetooth temperature service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/temperature-service/
    """

    def __init__(self, device: BluetoothDevice):
        self._device = device

    def notify(self, callback: Callable[[int], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden van de temperatuur. Hoe vaak je gegevens ontvangt
        hangt af van de periode. Standaard is de periode 1 seconde.

        Args:
            callback: een functie die periodiek wordt opgeroepen met de temperatuur als argument
        """
        self._device.notify(Characteristic.TEMPERATURE, lambda sender, data: callback(
            int.from_bytes(data[0:1], 'little', signed=True)))

    def read(self) -> int:
        """
        Leest de teperatuur van de microbit.

        Returns (int):
            de temperatuur in graden Celcius
        """
        return int.from_bytes(self._device.read(Characteristic.TEMPERATURE)[0:1], 'little', signed=True)

    def set_period(self, period: int):
        """
        Stelt het interval in waarmee je de temperatuur ontvangt indien je dat gevraagd hebt via de notify methode
        Standaard is de periode 1 seconde.

        Args:
            period (int): het interval waarmee je temperatuurgegevens ontvangt in milliseconden
        """
        self._device.write(Characteristic.TEMPERATURE_PERIOD, period.to_bytes(2, "little"))

    def read_period(self) -> int:
        """
        Geeft het interval terug waarmee je via notify de temperatuur ontvangt

        Returns (int):
            Het interval in milliseconden
        """
        return int.from_bytes(self._device.read(Characteristic.TEMPERATURE_PERIOD)[0:2], "little")
