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
        Checks whether the device information Bluetooth service is found on the connected micro:bit.

        Returns:
            true if the device information service was found, false if not.
        """
        return self._device.is_service_available(Service.DEVICE_INFORMATION)

    def read_model_number(self) -> str:
        """
        Reads the model number of the micro:bit.

        Returns:
            the model number of the micro:bit

        Raises:
            errors.BluetoothServiceNotFound: When the device information service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the device information button is active, but there was no way
                to read the model number (normally not present)
        """
        return str(self._device.read(Service.DEVICE_INFORMATION, Characteristic.MODEL_NUMBER_STRING), "utf-8")

    def read_serial_number(self) -> str:
        """
        Reads the serial number of the micro:bit.

        Returns:
            the serial number of the micro:bit

        Raises:
            errors.BluetoothServiceNotFound: When the device information service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the device information button is active, but there was no way
                to read the serial number (normally does not occur)
        """
        return str(self._device.read(Service.DEVICE_INFORMATION, Characteristic.SERIAL_NUMBER_STRING), "utf-8")

    def read_firmware_revision(self) -> str:
        """
        Reads the firmware version string from the micro:bit.

        Returns:
            the firmware version string of the micro:bit

        Raises:
            errors.BluetoothServiceNotFound: When the device information service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the device information button is active, but there was no way
                to read the firmware version (normally not present)
        """
        return str(self._device.read(Service.DEVICE_INFORMATION, Characteristic.FIRMWARE_REVISION_STRING), "utf-8")

    def read_hardware_revision(self) -> str:
        """
        Reads the hardware version string from the micro:bit.

        Attention:
            Although reading the hardware revision is mentioned in the bluetooth profile of the micro:bit, I was not
            successful in doing this on the micro:bits I had available for testing

        Returns:
            the hardware version string of the micro:bit

        Raises:
            errors.BluetoothServiceNotFound: When the device information service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the device information button is active, but there was no way
                to read the hardware version (normally not present)
        """
        return str(self._device.read(Service.DEVICE_INFORMATION, Characteristic.HARDWARE_REVISION_STRING), "utf-8")

    def read_manufacturer_name(self) -> str:
        """
        Reads the name of the manufacturer of the micro:bit.

        Attention:
            Although reading the manufacturer's name is listed in the micro:bit's Bluetooth profile,I was not
            successful in doing this on the micro:bits I had available for testing

        Returns:
            the name of the manufacturer of the micro:bit

        Raises:
            errors.BluetoothServiceNotFound: When the device information service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the device information button is active, but there was no way
                to read the manufacturer's name (normally not found)
        """
        return str(self._device.read(Service.DEVICE_INFORMATION, Characteristic.MANUFACTURER_NAME_STRING), "utf-8")
