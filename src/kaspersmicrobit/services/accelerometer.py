#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service
from ..bluetoothdevice import BluetoothDevice, ByteData
from typing import Union, Literal, Callable
from dataclasses import dataclass


AccelerometerPeriod = Union[
    Literal[1], Literal[2], Literal[5], Literal[10], Literal[20], Literal[80], Literal[160], Literal[640]
]
"""
Het interval waarmee de Accelerometer wordt uitgelezen is een integer en drukt het aantal milliseconden uit.
Er is een beperkt aantal geldige periodes: 1, 2, 5, 10, 20, 80, 160, 640

Warning:
    Dit zijn de geldige waarden volgens de specificatie, maar het lijkt erop dat dit niet werkt/klopt zoals ik verwacht
    TODO te onderzoeken
"""


@dataclass
class AccelerometerData:
    """
    De waarden van de 3 assen van een meting van de accelerometer, in milli-g. (met g de valversnelling op aarde)

    Attributes:
        x (int): horizontaal (van links naar rechts)
        y (int): horizontaal (van achter naar voor)
        z (int): verticaal (van onder naar boven)
    """
    x: int
    y: int
    z: int

    @staticmethod
    def from_bytes(values: ByteData):
        return AccelerometerData(
            int.from_bytes(values[0:2], "little", signed=True),
            int.from_bytes(values[2:4], "little", signed=True),
            int.from_bytes(values[4:6], "little", signed=True)
        )


class AccelerometerService:
    """
    Deze klasse bevat de functies die je kan aanspreken in verband met de accelerometer van de micro:bit

    De accelerometer meet kracht/versnelling langs 3 assen:

    - x: horizontaal (van links naar rechts)
    - y: horizontaal (van achter naar voor)
    - z: verticaal (van onder naar boven)

    De waarden van x, y en z zijn integers en zijn waarden in milli-g, waarbij 1 g, dus 1000 milli-g gelijk is aan de
    valversnelling op aarde. In vrije val zullen de waarden langs de assen ongeveer 0 zijn:

        AccelerometerData(x=0, y=0, z=0)

    Wanneer de micro:bit recht voor je met de knoppen zichtbaar en de pins naar je toe ligt,
    dan zal een meting van de accelerometer (ongeveer) het volgende geven:

        AccelerometerData(x=-50, y=-50, z=-1024)

    dat z ongeveer -1000 (ipv 1000 zoals je misschien verwacht zou hebben) valt te verklaren door dat je de kracht meet
    die de micro:bit tegenhoudt (bvb wanneer je de micro:bit vasthoudt: de kracht die je arm uitoefent, en die
    de micro:bit weerhoudt van te vallen)

    Kantel je de micro:bit vanuit deze startpositie naar je toe,
    dan stijgen y en z in waarde en blijft x ongeveer gelijk:

        AccelerometerData(x=-28, y=972, z=-56)

    Kantel je de micro:bit vanuit de startpositie van je weg,
    dan daalt y, en stijgt z in waarde en blijft x ongeveer gelijk:

        AccelerometerData(x=-104, y=-960, z=124)

    Kantel je de micro:bit vanuit de startpositie naar links
    dan daalt x, en stijgt z in waarde en blijft y ongeveer gelijk:

        AccelerometerData(x=-1108, y=72, z=-160)

    Kantel je de micro:bit vanuit de startpositie naar rechts
    dan stijgen x en z in waarde en blijft y ongeveer gelijk:

        AccelerometerData(x=960, y=60, z=0)

    Draai je de micro:bit helemaal ondersteboven
    dan stijgt z ongeveer tot 1000 en blijven x en y ongeveer gelijk:

        AccelerometerData(x=-56, y=-36, z=1024)

    Dit zijn alle mogelijkheden aangeboden door de accelerometer bluetooth service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/accelerometer-service/

    See Also: https://lancaster-university.github.io/microbit-docs/ubit/accelerometer/
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Kijkt na of de accelerometer bluetooth service gevonden wordt op de geconnecteerde micro:bit.

        Returns:
            true als de accelerometer gevonden werd, false indien niet.
        """
        return self._device.is_service_available(Service.ACCELEROMETER)

    def notify(self, callback: Callable[[AccelerometerData], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden van nieuwe accelerometer gegevens. Hoe vaak je
        nieuwe gegevens ontvangt hangt af van de accelerometer periode

        Args:
            callback (Callable[[AccelerometerData], None]): een functie die wordt opgeroepen wanneer er nieuwe gegevens
                zijn van de accelerometer. De nieuwe AccelerometerData worden meegegeven als argument aan deze functie

        Raises:
            BluetoothServiceNotFound: Wanneer de accelerometer service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de accelerometer service actief is, maar er geen manier was om de
                accelerometer data notificaties te activeren (komt normaal gezien niet voor)
        """
        self._device.notify(Service.ACCELEROMETER, Characteristic.ACCELEROMETER_DATA,
                            lambda sender, data: callback(AccelerometerData.from_bytes(data)))

    def read(self) -> AccelerometerData:
        """
        Geeft de gegevens van de accelerometer.

        Returns:
            De gegevens van de accelerometer (x, y en z)

        Raises:
            BluetoothServiceNotFound: Wanneer de accelerometer service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de accelerometer service actief is, maar er geen manier was om de
                accelerometer data te lezen (komt normaal gezien niet voor)
        """
        return AccelerometerData.from_bytes(self._device.read(Service.ACCELEROMETER, Characteristic.ACCELEROMETER_DATA))

    def set_period(self, period: AccelerometerPeriod):
        """
        Stelt het interval in waarmee de accelerometer metingen doet (in milliseconden).

        Args:
            period (AccelerometerPeriod): het interval waarop de accelerometer metingen doet,
                geldige waarden zijn: 1, 2, 5, 10, 20, 80, 160, 640

        Raises:
            BluetoothServiceNotFound: Wanneer de accelerometer service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de accelerometer service actief is, maar er geen manier was om de
                accelerometer periode te wijzigen (komt normaal gezien niet voor)

        Warning:
            Dit zijn de geldige waarden volgens de specificatie, maar het lijkt erop dat dit niet werkt/klopt zoals ik verwacht
            TODO te onderzoeken
        """
        self._device.write(Service.ACCELEROMETER, Characteristic.ACCELEROMETER_PERIOD, period.to_bytes(2, "little"))

    def read_period(self) -> int:
        """
        Geeft het interval terug waarmee de accelerometer metingen doet

        Returns:
            Het interval in milliseconden

        Raises:
            BluetoothServiceNotFound: Wanneer de accelerometer service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de accelerometer service actief is, maar er geen manier was om de
                accelerometer periode te lezen (komt normaal gezien niet voor)
        """
        return int.from_bytes(self._device.read(Service.ACCELEROMETER, Characteristic.ACCELEROMETER_PERIOD)[0:2], "little")
