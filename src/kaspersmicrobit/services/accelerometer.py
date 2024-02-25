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
The interval at which the Accelerometer is read is an integer and expresses the number of milliseconds.
There is a limited number of valid periods: 1, 2, 5, 10, 20, 80, 160, 640

Warning:
    These are the valid values according to the specification, but it seems that this does not work as I expect
    TODO to investigate
"""


@dataclass
class AccelerometerData:
    """
    The values of the 3 axes of an accelerometer measurement, in milli-g. (with g the gravitational acceleration on Earth)

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
        return AccelerometerData(
            int.from_bytes(values[0:2], "little", signed=True),
            int.from_bytes(values[2:4], "little", signed=True),
            int.from_bytes(values[4:6], "little", signed=True)
        )


class AccelerometerService:
    """
    This class contains the functions that can be used related to the accelerometer of the micro:bit

    The accelerometer measures force/acceleration along 3 axes:

    - x: horizontal (from left to right)
    - y: horizontal (from back to front)
    - z: vertical (from bottom to top)

    The values of x, y and z are integers and are values in milli-g, where 1 g, so 1000 milli-g, is equal to the
    gravitational acceleration on earth. In free fall the values along the axes will be approximately 0:

        AccelerometerData(x=0, y=0, z=0)

    When the micro:bit is directly in front of you with the buttons visible and the pins facing you,
    then a reading from the accelerometer will give (approximately) the following:

        AccelerometerData(x=-50, y=-50, z=-1024)

    That z is approximately -1000 (instead of 1000 as you might have expected) can be explained by measuring the force
    that stops the micro:bit (e.g. when you hold the micro:bit: the force that your arm exerts, and that
    prevents the micro:bit from falling)

    If you tilt the micro:bit towards you from this starting position,
    then y and z increase in value and x remains approximately the same:

        AccelerometerData(x=-28, y=972, z=-56)

    If you tilt the micro:bit away from you from the starting position,
    then y decreases, z increases in value and x remains approximately the same:

        AccelerometerData(x=-104, y=-960, z=124)

    Tilt the micro:bit from the starting position to the left
    then x decreases, z increases in value and y remains approximately the same:

        AccelerometerData(x=-1108, y=72, z=-160)

    Tilt the micro:bit from the starting position to the right
    then x and z increase in value and y remains approximately the same:

        AccelerometerData(x=960, y=60, z=0)

    Turn the micro:bit completely upside down
    then z increases approximately to 1000 and x and y remain approximately the same:

        AccelerometerData(x=-56, y=-36, z=1024)

    These are all options offered by the accelerometer Bluetooth service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/accelerometer-service/

    See Also: https://lancaster-university.github.io/microbit-docs/ubit/accelerometer/
    """
    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Checks whether the accelerometer Bluetooth service is found on the connected micro:bit.

        Returns:
            true if the accelerometer was found, false if not.
        """
        return self._device.is_service_available(Service.ACCELEROMETER)

    def notify(self, callback: Callable[[AccelerometerData], None]):
        """
        You can call this method when you want to be notified of new accelerometer data. How often you
        receive new data depends on the accelerometer period

        Args:
            callback (Callable[[AccelerometerData], None]): a function that is called when there is new data
                from the accelerometer. The new AccelerometerData is passed as an argument to this function

        Raises:
            errors.BluetoothServiceNotFound: When the accelerometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the accelerometer service is running but there was no way to
                activate accelerometer data notifications (normally does not occur)
        """
        self._device.notify(Service.ACCELEROMETER, Characteristic.ACCELEROMETER_DATA,
                            lambda sender, data: callback(AccelerometerData.from_bytes(data)))

    def read(self) -> AccelerometerData:
        """
        Reads the accelerometer data.

        Returns:
            The accelerometer data (x, y and z)

        Raises:
            errors.BluetoothServiceNotFound: When the accelerometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the accelerometer service is running but there was no way to
                read accelerometer data (normally does not occur)
        """
        return AccelerometerData.from_bytes(self._device.read(Service.ACCELEROMETER, Characteristic.ACCELEROMETER_DATA))

    def set_period(self, period: AccelerometerPeriod):
        """
        Sets the interval at which the accelerometer takes measurements (in milliseconds).

        Args:
            period (AccelerometerPeriod): the interval at which the accelerometer takes measurements,
                valid values are: 1, 2, 5, 10, 20, 80, 160, 640

        Raises:
            errors.BluetoothServiceNotFound: When the accelerometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the accelerometer service is running but there was no way to
                change accelerometer period (normally does not occur)

        Warning:
            These are the valid values according to the specification, but it seems that this does not work as I expect
            TODO to investigate
        """
        self._device.write(Service.ACCELEROMETER, Characteristic.ACCELEROMETER_PERIOD, period.to_bytes(2, "little"))

    def read_period(self) -> int:
        """
        Returns the interval at which the accelerometer takes measurements

        Returns:
            The interval in milliseconds

        Raises:
            errors.BluetoothServiceNotFound: When the accelerometer service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the accelerometer service is running but there was no way to
                accelerometer period to be read (normally does not occur)
        """
        return int.from_bytes(self._device.read(Service.ACCELEROMETER, Characteristic.ACCELEROMETER_PERIOD)[0:2], "little")
