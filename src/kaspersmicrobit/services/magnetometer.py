#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from typing import Callable, Literal, Union
from ..characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice, ByteData

MagnetometerPeriod = Union[
    Literal[1], Literal[2], Literal[5], Literal[10], Literal[20], Literal[80], Literal[160], Literal[640]
]
"""
Het interval waarmee de Magnetometer wordt uitgelezen is een integer en drukt het aantal milliseconden uit.
Er is een beperkt aantal geldige periodes: 1, 2, 5, 10, 20, 80, 160, 640
"""

@dataclass
class MagnetometerData:
    """
    De waarden op de 3 assen van een meting van de magnetometer
    """
    x: int
    y: int
    z: int

    @staticmethod
    def from_bytes(values: ByteData):
        return MagnetometerData(
            int.from_bytes(values[0:2], "little", signed=True),
            int.from_bytes(values[2:4], "little", signed=True),
            int.from_bytes(values[4:6], "little", signed=True)
        )


class MagnetometerService:
    """
    Deze klasse bevat de functies die je kan aanspreken in verband met de magnetometor van de microbit.
    Er zijn functies om

        - het magnetisch veld langs 3 assen te meten
        - de hoek in graden ten opzichte van het noorden te meten
        - de magnetometer te calibreren. Het is het best om de magnetometer te calibreren voor je gegevens uitleest,
          zoniet kunnen de gegevens of de hoek in graden verkeerd zijn

    Dit zijn alle mogelijkheden aangeboden door de bluetooth magnetometer service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/magnetometer-service/
    See Also: https://lancaster-university.github.io/microbit-docs/ubit/compass//
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def notify_data(self, callback: Callable[[MagnetometerData], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden van nieuwe magnetometer gegevens. Hoe vaak je
        nieuwe gegevens ontvangt hangt af van de magnetometer periode

        Args:
            callback (Callable[[MagnetometerData], None]): een functie die wordt opgeroepen wanneer er nieuwe gegevens
            zijn van de magnetometer. De nieuwe MagnetometerData worden meegegeven als argument aan deze functie

        Returns:
            None
        """
        self._device.notify(Characteristic.MAGNETOMETER_DATA,
                            lambda sender, data: callback(MagnetometerData.from_bytes(data)))

    def read_data(self) -> MagnetometerData:
        """
        Geeft de gegevens van de magnetometer.

        Returns (MagnetometerData):
            De gegevens van de magnetometer (x, y en z)
        """
        return MagnetometerData.from_bytes(self._device.read(Characteristic.MAGNETOMETER_DATA))

    def set_period(self, period: MagnetometerPeriod):
        """
        Stelt het interval in waarmee de magnetometer metingen doet (in milliseconden).

        Args:
            period (MagnetometerPeriod): het interval waarop de magnetometer metingen doet,
                geldige waarden zijn: 1, 2, 5, 10, 20, 80, 160, 640
        """
        self._device.write(Characteristic.MAGNETOMETER_PERIOD, period.to_bytes(2, "little"))

    def read_period(self) -> int:
        """
        Geeft het interval terug waarmee de magnetometer metingen doet

        Returns (int):
            Het interval in milliseconden
        """
        return int.from_bytes(self._device.read(Characteristic.MAGNETOMETER_PERIOD)[0:2], "little")

    def notify_bearing(self, callback: Callable[[int], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden van de hoek in graden waarin de microbit gericht
        wordt ten opzichte van het noorden.

        Args:
            callback (Callable[[int], None]): een functie die periodiek wordt opgeroepen met de hoek in graden ten
            opzichte van het noorden

        Returns:
            None
        """
        self._device.notify(Characteristic.MAGNETOMETER_BEARING,
                            lambda sender, data: callback(int.from_bytes(data[0:2], "little")))

    def read_bearing(self) -> int:
        """
        Lees de hoek in graden waarin de microbit gericht wordt ten opzichte van het noorden.

        Returns (int):
            de hoek in graden tov het noorden
        """
        return int.from_bytes(self._device.read(Characteristic.MAGNETOMETER_BEARING)[0:2], 'little')

    def calibrate(self, on_success: Callable[[], None] = None, on_error: Callable[[], None] = None) -> None:
        """
        Calibreer de magnetometer. Deze methode start het calibratieproces op de microbit, waarbij je de microbit
        moet kantelen om het LED scherm te vullen. Door het kantelen wordt de magnetometer gecalibreerd

        See Also: https://support.microbit.org/support/solutions/articles/19000008874-calibrating-the-micro-bit-compass

        Args:
            on_success (Callable[[], None]): wordt opgeroepen wanneer de calibratie gelukt is
            on_error (Callable[[], None]): wordt opgeroepen wanneer de calibratie mislukt is
        """
        self._device.write(Characteristic.MAGNETOMETER_CALIBRATION, int.to_bytes(1, 1, 'little'))

        if on_success or on_error:
            def _callback(sender, data):
                result = int.from_bytes(data[0:2], "little")
                if result == 2 and on_success:
                    on_success()
                elif on_error:
                    on_error()

            self._device.notify(Characteristic.MAGNETOMETER_CALIBRATION, _callback)

