#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from concurrent.futures import Future
from dataclasses import dataclass
from typing import Callable, Literal, Union
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service
from ..bluetoothdevice import BluetoothDevice, ByteData

MagnetometerPeriod = Union[
    Literal[1], Literal[2], Literal[5], Literal[10], Literal[20], Literal[80], Literal[160], Literal[640]
]
"""
The interval at which the Magnetometer is read is an integer and expresses the number of milliseconds.
There is a limited number of valid periods: 1, 2, 5, 10, 20, 80, 160, 640

Warning:
    These are the valid values according to the specification, but it seems that this does not work as I expect
    TODO to investigate
"""


class Calibration:
    """
    A class that allows you to follow up on a calibration
    """
    def __init__(self, future: Future[ByteData]):
        self._future = future
        self._result = None

    def done(self) -> bool:
        """
        Check whether the calibration is still in progress

        Returns:
            True if the calibration is done, False if it is still in progress
        """
        return self._future.done()

    def wait_for_result(self, timeout=None) -> bool:
        """
        Wait for the end of the calibration process
        Args:
            timeout: the maximum number of seconds you want to wait for a result

        Returns:
            True if the calibration was successful, False if it was unsuccessful
        """
        if not self._result:
            self._result = int.from_bytes(self._future.result(timeout=timeout)[0:2], "little")

        return self._result


@dataclass
class MagnetometerData:
    """
    The values on the 3 axes of a magnetometer measurement

    Attributes:
        x (int): horizontal (left to right)
        y (int): horizontal (from back to front)
        z (int): vertical (from bottom to top)
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
    This class contains the functions that you can use related to the magnetometor of the micro:bit.
    There are functions to

    - measure the magnetic field along 3 axes
    - measure the angle in degrees relative to north
    - calibrate the magnetometer. It is best to calibrate the magnetometer before reading data,
      otherwise the data or angle in degrees may be wrong.

    Warning:
        I noticed that despite calibration, the microbits I tested gave poor results
        (to be further investigated)

    These are all options offered by the Bluetooth magnetometer service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/magnetometer-service/

    See Also: https://lancaster-university.github.io/microbit-docs/ubit/compass/
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device
        self._calibration = None

    def is_available(self) -> bool:
        """
        Checks whether the magnetometer Bluetooth service is found on the connected micro:bit.

        Returns:
            true if the magnetometer was found, false if not.
        """
        return self._device.is_service_available(Service.MAGNETOMETER)

    def notify_data(self, callback: Callable[[MagnetometerData], None]):
        """
        You can call this method when you want to be notified of new magnetometer data. How often you
        receive new data depends on the magnetometer period

        Warning:
            The micro:bit will not provide any measurements if there has been no calibration

        Args:
            callback (Callable[[MagnetometerData], None]): a function that is called when there is new data
                are of the magnetometer. The new MagnetometerData is passed as an argument to this function

        Raises:
            errors.BluetoothServiceNotFound: When the magnetometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the magnetometer service is active but there was no way
                to activate magnetometer data notifications (normally does not occur)
        """
        self._device.notify(Service.MAGNETOMETER, Characteristic.MAGNETOMETER_DATA,
                            lambda sender, data: callback(MagnetometerData.from_bytes(data)))

    def read_data(self) -> MagnetometerData:
        """
        Returns the magnetometer data.

        Returns:
            The magnetometer data (x, y and z)

        Raises:
            errors.BluetoothServiceNotFound: When the magnetometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the magnetometer service is active but there was no way
                to read the magnetometer data (normally does not occur)
        """
        return MagnetometerData.from_bytes(self._device.read(Service.MAGNETOMETER, Characteristic.MAGNETOMETER_DATA))

    def set_period(self, period: MagnetometerPeriod):
        """
        Sets the interval at which the magnetometer takes measurements (in milliseconds).

        Args:
            period (MagnetometerPeriod): the interval at which the magnetometer takes measurements,
                valid values are: 1, 2, 5, 10, 20, 80, 160, 640

        Warning:
            These are the valid values according to the specification, but it seems that this does not work as I expect
            TODO to investigate

        Raises:
            errors.BluetoothServiceNotFound: When the magnetometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the magnetometer service is active but there was no way
                to write the magnetometer period (normally does not occur)
        """
        self._device.write(Service.MAGNETOMETER, Characteristic.MAGNETOMETER_PERIOD, period.to_bytes(2, "little"))

    def read_period(self) -> int:
        """
        Returns the interval at which the magnetometer takes measurements

        Returns:
            The interval in milliseconds

        Raises:
            errors.BluetoothServiceNotFound: When the magnetometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the magnetometer service is active but there was no way
                to read the magnetometer period (normally does not occur)
        """
        return int.from_bytes(
            self._device.read(Service.MAGNETOMETER, Characteristic.MAGNETOMETER_PERIOD)[0:2], "little")

    def notify_bearing(self, callback: Callable[[int], None]):
        """
        You can call this method if you want to be informed of the angle in degrees at which the micro:bit is oriented
        is compared to the north.

        Warning:
            The micro:bit will not provide any measurements if there has been no calibration

        Args:
            callback (Callable[[int], None]): a function that is called periodically with the angle in degrees
                compared to the north

        Raises:
            errors.BluetoothServiceNotFound: When the magnetometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the magnetometer service is active but there was no way
                to activate magnetometer bearing notifications (normally does not occur)
        """
        self._device.notify(Service.MAGNETOMETER, Characteristic.MAGNETOMETER_BEARING,
                            lambda sender, data: callback(int.from_bytes(data[0:2], "little")))

    def read_bearing(self) -> int:
        """
        Read the angle in degrees at which the micro:bit is pointed relative to north.

        Returns:
            the angle in degrees with respect to north

        Raises:
            errors.BluetoothServiceNotFound: When the magnetometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the magnetometer service is active but there was no way
                to read the magnetometer bearing (normally does not occur)
        """
        return int.from_bytes(
            self._device.read(Service.MAGNETOMETER, Characteristic.MAGNETOMETER_BEARING)[0:2], 'little')

    def calibrate(self) -> Calibration:
        """
        Calibrate the magnetometer. This method starts the calibration process on the micro:bit, you will be asked
        to tilt the micro:bit until all LEDs on the LED display are on. The magnetometer is calibrated by tilting
        If a calibration is already in progress, a new calibration will not be started

        Warning:
            The micro:bit will not provide any measurements if there has been no calibration

        See Also: https://support.microbit.org/support/solutions/articles/19000008874-calibrating-the-micro-bit-compass

        Returns:
            It is the calibration in progress. You can use this to check whether the calibration is still in progress,
            or wait until the calibration is done.

        Raises:
            errors.BluetoothServiceNotFound: When the magnetometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the magnetometer service is active but there was no way
                to activate or monitor the magnetometer calibration (normally does not occur)
        """
        if self._calibration and not self._calibration.done():
            return self._calibration

        future = self._device.wait_for(Service.MAGNETOMETER, Characteristic.MAGNETOMETER_CALIBRATION)
        self._device.write(Service.MAGNETOMETER, Characteristic.MAGNETOMETER_CALIBRATION, int.to_bytes(1, 1, 'little'))
        calibration = Calibration(future)
        self._calibration = calibration
        return calibration
