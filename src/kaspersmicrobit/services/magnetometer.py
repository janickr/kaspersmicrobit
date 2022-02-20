#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from concurrent.futures import Future
from dataclasses import dataclass
from typing import Callable, Literal, Union
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothdevice import BluetoothDevice, ByteData

MagnetometerPeriod = Union[
    Literal[1], Literal[2], Literal[5], Literal[10], Literal[20], Literal[80], Literal[160], Literal[640]
]
"""
Het interval waarmee de Magnetometer wordt uitgelezen is een integer en drukt het aantal milliseconden uit.
Er is een beperkt aantal geldige periodes: 1, 2, 5, 10, 20, 80, 160, 640

Opgelet:
    Dit zijn de geldige waarden volgens de specificatie, maar het lijkt erop dat dit niet werkt/klopt zoals ik verwacht
    TODO te onderzoeken
"""


class Calibration:
    """
    Een klasse die je toelaat een calibratie op te volgen
    """
    def __init__(self, future: Future[ByteData]):
        self._future = future
        self._result = None

    def done(self) -> bool:
        """
        Kijk na of de calibratie nog bezig is

        Returns (bool):
            True indien de calibratie gedaan is, False indien het nog bezig is
        """
        return self._future.done()

    def wait_for_result(self) -> bool:
        """
        Wacht op het einde van het calibreren

        Returns (bool):
            True indien de calibratie gelukt is, False indien het mislukt is
        """
        if not self._result:
            self._result = int.from_bytes(self._future.result()[0:2], "little")

        return self._result


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
      zoniet kunnen de gegevens of de hoek in graden verkeerd zijn.

    Opgelet:
        Ik heb gemerkt dat ondanks calibratie, de microbits die ik testte slechte resultaten gaven
        (verder te onderzoeken)

    Dit zijn alle mogelijkheden aangeboden door de bluetooth magnetometer service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/magnetometer-service/

    See Also: https://lancaster-university.github.io/microbit-docs/ubit/compass/
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device
        self._calibration = None

    def notify_data(self, callback: Callable[[MagnetometerData], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden van nieuwe magnetometer gegevens. Hoe vaak je
        nieuwe gegevens ontvangt hangt af van de magnetometer periode

        Opgelet:
            De microbit geeft geen metingen indien er geen calibratie is geweest

        Args:
            callback (Callable[[MagnetometerData], None]): een functie die wordt opgeroepen wanneer er nieuwe gegevens
                zijn van de magnetometer. De nieuwe MagnetometerData worden meegegeven als argument aan deze functie

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

        Opgelet:
            Dit zijn de geldige waarden volgens de specificatie, maar het lijkt erop dat dit niet werkt/klopt zoals ik verwacht
            TODO te onderzoeken
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

        Opgelet:
            De microbit geeft geen metingen indien er geen calibratie is geweest

        Args:
            callback (Callable[[int], None]): een functie die periodiek wordt opgeroepen met de hoek in graden ten
                opzichte van het noorden
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

    def calibrate(self) -> Calibration:
        """
        Calibreer de magnetometer. Deze methode start het calibratieproces op de microbit, waarbij je de microbit
        moet kantelen om het LED scherm te vullen. Door het kantelen wordt de magnetometer gecalibreerd
        Indien er al een calibratie bezig is wordt geen nieuwe calibratie gestart

        Opgelet:
            De microbit geeft geen metingen indien er geen calibratie is geweest

        See Also: https://support.microbit.org/support/solutions/articles/19000008874-calibrating-the-micro-bit-compass

        Returns (Calibration):
            Het de calibratie die bezig is. Je kan hiermee nakijken of het calibreren nog bezig is, of wachten tot
            De calibratie gedaan is.
        """
        if self._calibration and not self._calibration.done():
            return self._calibration

        self._device.write(Characteristic.MAGNETOMETER_CALIBRATION, int.to_bytes(1, 1, 'little'))
        future = self._device.wait_for(Characteristic.MAGNETOMETER_CALIBRATION)
        calibration = Calibration(future)
        self._calibration = calibration
        return calibration
