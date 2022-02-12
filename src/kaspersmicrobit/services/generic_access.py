#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ..bluetoothdevice import BluetoothDevice
from ..bluetoothprofile.characteristics import Characteristic


class GenericAccessService:
    """
    Deze klasse bevat de functies om de informatie aangeboden door de bluetooth generic access service
    uit te lezen
    """

    def __init__(self, device: BluetoothDevice):
        self._device = device

    def read_device_name(self) -> str:
        """
        Leest de naam van de microbit.

        Returns (str):
            de naam van de microbit
        """
        return str(self._device.read(Characteristic.DEVICE_NAME), "utf-8")
