#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time

from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.magnetometer import MagnetometerData

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'
# example {


def magnetometer_data(data: MagnetometerData):
    print(f"Magnetometer data: {data}")


def bearing(degrees: int):
    print(f"Bearing {degrees}° from North")


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    # First calibrate the magnetometer / Calibreer de magnetometer eerst
    calibration = microbit.magnetometer.calibration()
    print("Calibrating...")

    # Wait for the calibration to finish / Wacht op het einde van de calibratie
    if calibration.wait_for_result():
        print("Calibration succes!")
    else:
        print("Calibration failed!")

    # read the current magnetometer data and bearing / lees de huidige magnetometer data en hoek tov het noorden
    print(f"Current magnetometer data: {microbit.magnetometer.read_data()}")
    print(f"Current magnetometer bearing: {microbit.magnetometer.read_bearing()}°")

    # check how often magnetometer updates will occur if you listen to them with notify
    # / lees hoe vaak magnetometer updates doorgestuurd worden wanneer je hier naar luistert met notify
    print(f"Current period: {microbit.magnetometer.read_period()}")

    # listen for magnetometer data updates / luister naar magnetometer updates
    microbit.magnetometer.notify_data(magnetometer_data)
    microbit.magnetometer.notify_bearing(bearing)

    time.sleep(5)

    # change the update interval / wijzig het update interval
    print("Now slow down updates to 640 milliseconds")
    microbit.magnetometer.set_period(640)

    print(f"Magnetometer updates will now occur every {microbit.magnetometer.read_period()} milliseconds")

    time.sleep(5)
# }
