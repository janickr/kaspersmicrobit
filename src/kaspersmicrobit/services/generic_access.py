#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ..bluetoothdevice import BluetoothDevice
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service


class GenericAccessService:
    """
    This class contains the functions to access the information provided by the Bluetooth generic access service
    to read out
    """

    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Checks whether the generic access Bluetooth service is found on the connected micro:bit.

        Returns:
            true if the generic access service was found, false if not.
        """
        return self._device.is_service_available(Service.GENERIC_ACCESS)

    def read_device_name(self) -> str:
        """
        Reads the name of the micro:bit.

        Returns:
            the name of the micro:bit

        Raises:
            errors.BluetoothServiceNotFound: When the generic access service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the generic access service is running but there was no way
                to read the device name (normally not present)
        """
        return str(self._device.read(Service.GENERIC_ACCESS, Characteristic.DEVICE_NAME), "utf-8")
