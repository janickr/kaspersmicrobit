#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time

from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.magnetometer import MagnetometerData

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


def magnetometer_data(data: MagnetometerData):
    print(f"Magnetometer data: {data}")


def bearing(degrees: int):
    print(f"Bearing {degrees}° from North")


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    # First calibrate the magnetometer
    if microbit.magnetometer.calibrate():
        print("Calibration succes!")
    else:
        print("Calibration failed!")

    # you can read the current magnetometer data and bearing
    print(f"Current magnetometer data: {microbit.magnetometer.read_data()}")
    print(f"Current magnetometer bearing: {microbit.magnetometer.read_bearing()}°")

    # you can check how often magnetometer updates will occur if you listen to them with notify
    print(f"Current period: {microbit.magnetometer.read_period()}")

    # you can listen for magnetometer data updates
    microbit.magnetometer.notify_data(magnetometer_data)
    microbit.magnetometer.notify_bearing(bearing)

    time.sleep(5)

    # you can change the update interval
    print("Now slow down updates to 640 milliseconds")
    microbit.magnetometer.set_period(640)

    print(f"Magnetometer updates will now occur every {microbit.magnetometer.read_period()} milliseconds")

    time.sleep(500)
