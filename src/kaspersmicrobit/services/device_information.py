#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ..bluetoothdevice import BluetoothDevice
from ..bluetoothprofile.characteristics import Characteristic


class DeviceInformationService:
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def read_model_number(self) -> str:
        """
        Leest het modelnummer van de microbit.

        Returns (str):
            het modelnummer van de microbit
        """
        return str(self._device.read(Characteristic.MODEL_NUMBER_STRING), "utf-8")

    def read_serial_number(self) -> str:
        """
        Leest het serienummer van de microbit.

        Returns (str):
            het serienummer van de microbit
        """
        return str(self._device.read(Characteristic.SERIAL_NUMBER_STRING), "utf-8")

    def read_firmware_revision(self) -> str:
        """
        Leest de firmware versie string van de microbit.

        Returns (str):
            de firmware versie string van de microbit
        """
        return str(self._device.read(Characteristic.FIRMWARE_REVISION_STRING), "utf-8")

    def read_hardware_revision(self) -> str:
        """
        Leest de hardware versie string van de microbit.

        Opgelet:
            Hoewel het lezen van de harware revisie vermeld wordt in het bluetooth profiel van de microbit, kon ik deze
            niet opvragen op de microbits die ik heb kunnen testen.

        Returns (str):
            de hardware versie string van de microbit
        """
        return str(self._device.read(Characteristic.HARDWARE_REVISION_STRING), "utf-8")

    def read_manufacturer_name(self) -> str:
        """
        Leest de naam van de fabrikant van de microbit.

        Opgelet:
            Hoewel het lezen van de naam van de fabrikant vermeld wordt in het bluetooth profiel van de microbit, kon
            ik deze niet opvragen op de microbits die ik heb kunnen testen.

        Returns (str):
            de naam van de fabrikant van de microbit
        """
        return str(self._device.read(Characteristic.MANUFACTURER_NAME_STRING), "utf-8")
