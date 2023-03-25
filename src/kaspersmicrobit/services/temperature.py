#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable

from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service
from ..bluetoothdevice import BluetoothDevice


class TemperatureService:
    """
    Deze klasse bevat de functies die je kan aanspreken in verband met de temperatuur sensor van de micro:bit
    Deze sensor meet de temperatuur van de micro:bit in graden Celcius.

    Dit zijn alle mogelijkheden aangeboden door de bluetooth temperature service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/temperature-service/
    """

    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Kijkt na of de temperatuur bluetooth service gevonden wordt op de geconnecteerde micro:bit.

        Returns:
            true als de temperatuur service gevonden werd, false indien niet.
        """
        return self._device.is_service_available(Service.TEMPERATURE)

    def notify(self, callback: Callable[[int], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden van de temperatuur. Hoe vaak je gegevens ontvangt
        hangt af van de periode. Standaard is de periode 1 seconde.

        Args:
            callback: een functie die periodiek wordt opgeroepen met de temperatuur als argument

        Raises:
            BluetoothServiceNotFound: Wanneer de temperatuur service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de temperatuur service actief is, maar er geen manier was
                om de notificaties van temperatuur data te activeren (komt normaal gezien niet voor)
        """
        self._device.notify(Service.TEMPERATURE, Characteristic.TEMPERATURE,
                            lambda sender, data: callback(int.from_bytes(data[0:1], 'little', signed=True)))

    def read(self) -> int:
        """
        Leest de teperatuur van de micro:bit.

        Returns:
            de temperatuur in graden Celcius

        Raises:
            BluetoothServiceNotFound: Wanneer de temperatuur service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de temperatuur service actief is, maar er geen manier was
                om de temperatuur te lezen (komt normaal gezien niet voor)
        """
        return int.from_bytes(
            self._device.read(Service.TEMPERATURE, Characteristic.TEMPERATURE)[0:1], 'little', signed=True)

    def set_period(self, period: int):
        """
        Stelt het interval in waarmee je de temperatuur ontvangt indien je dat gevraagd hebt via de notify methode
        Standaard is de periode 1 seconde.

        Args:
            period (int): het interval waarmee je temperatuurgegevens ontvangt in milliseconden

        Raises:
            BluetoothServiceNotFound: Wanneer de temperatuur service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de temperatuur service actief is, maar er geen manier was
                om de temperatuur periode te schrijven (komt normaal gezien niet voor)
        """
        self._device.write(Service.TEMPERATURE, Characteristic.TEMPERATURE_PERIOD, period.to_bytes(2, "little"))

    def read_period(self) -> int:
        """
        Geeft het interval terug waarmee je via notify de temperatuur ontvangt

        Returns:
            Het interval in milliseconden

        Raises:
            BluetoothServiceNotFound: Wanneer de temperatuur service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de temperatuur service actief is, maar er geen manier was
                om de temperatuur periode te lezen (komt normaal gezien niet voor)
        """
        return int.from_bytes(
            self._device.read(Service.TEMPERATURE, Characteristic.TEMPERATURE_PERIOD)[0:2], "little")
