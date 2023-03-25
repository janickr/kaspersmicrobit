#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ..bluetoothdevice import BluetoothDevice
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service


class DeviceInformationService:
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Kijkt na of de device information bluetooth service gevonden wordt op de geconnecteerde micro:bit.

        Returns:
            true als de device information service gevonden werd, false indien niet.
        """
        return self._device.is_service_available(Service.DEVICE_INFORMATION)

    def read_model_number(self) -> str:
        """
        Leest het modelnummer van de micro:bit.

        Returns:
            het modelnummer van de micro:bit

        Raises:
            BluetoothServiceNotFound: Wanneer de device information service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de button device information actief is, maar er geen manier was
                om het modelnummer te lezen (komt normaal gezien niet voor)
        """
        return str(self._device.read(Service.DEVICE_INFORMATION, Characteristic.MODEL_NUMBER_STRING), "utf-8")

    def read_serial_number(self) -> str:
        """
        Leest het serienummer van de micro:bit.

        Returns:
            het serienummer van de micro:bit

        Raises:
            BluetoothServiceNotFound: Wanneer de device information service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de button device information actief is, maar er geen manier was
                om het serienummer te lezen (komt normaal gezien niet voor)
        """
        return str(self._device.read(Service.DEVICE_INFORMATION, Characteristic.SERIAL_NUMBER_STRING), "utf-8")

    def read_firmware_revision(self) -> str:
        """
        Leest de firmware versie string van de micro:bit.

        Returns:
            de firmware versie string van de micro:bit

        Raises:
            BluetoothServiceNotFound: Wanneer de device information service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de button device information actief is, maar er geen manier was
                om de firmware versie te lezen (komt normaal gezien niet voor)
        """
        return str(self._device.read(Service.DEVICE_INFORMATION, Characteristic.FIRMWARE_REVISION_STRING), "utf-8")

    def read_hardware_revision(self) -> str:
        """
        Leest de hardware versie string van de micro:bit.

        Opgelet:
            Hoewel het lezen van de harware revisie vermeld wordt in het bluetooth profiel van de micro:bit, kon ik deze
            niet opvragen op de microbits die ik heb kunnen testen.

        Returns:
            de hardware versie string van de micro:bit

        Raises:
            BluetoothServiceNotFound: Wanneer de device information service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de button device information actief is, maar er geen manier was
                om de hardware versie te lezen (komt normaal gezien niet voor)
        """
        return str(self._device.read(Service.DEVICE_INFORMATION, Characteristic.HARDWARE_REVISION_STRING), "utf-8")

    def read_manufacturer_name(self) -> str:
        """
        Leest de naam van de fabrikant van de micro:bit.

        Opgelet:
            Hoewel het lezen van de naam van de fabrikant vermeld wordt in het bluetooth profiel van de micro:bit, kon
            ik deze niet opvragen op de microbits die ik heb kunnen testen.

        Returns:
            de naam van de fabrikant van de micro:bit

        Raises:
            BluetoothServiceNotFound: Wanneer de device information service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de button device information actief is, maar er geen manier was
                om de naam van de fabrikant te lezen (komt normaal gezien niet voor)
        """
        return str(self._device.read(Service.DEVICE_INFORMATION, Characteristic.MANUFACTURER_NAME_STRING), "utf-8")
