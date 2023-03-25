#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ..bluetoothdevice import BluetoothDevice
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service


class GenericAccessService:
    """
    Deze klasse bevat de functies om de informatie aangeboden door de bluetooth generic access service
    uit te lezen
    """

    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Kijkt na of de generic access bluetooth service gevonden wordt op de geconnecteerde micro:bit.

        Returns:
            true als de generic access service gevonden werd, false indien niet.
        """
        return self._device.is_service_available(Service.GENERIC_ACCESS)

    def read_device_name(self) -> str:
        """
        Leest de naam van de micro:bit.

        Returns:
            de naam van de micro:bit

        Raises:
            BluetoothServiceNotFound: Wanneer de generic access service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de generic acces service actief is, maar er geen manier was
                om de device naam te lezen (komt normaal gezien niet voor)
        """
        return str(self._device.read(Service.GENERIC_ACCESS, Characteristic.DEVICE_NAME), "utf-8")
