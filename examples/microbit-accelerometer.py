#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time

from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.accelerometer import AccelerometerData

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'
# example {

def accelerometer_data(data: AccelerometerData):
    print(f"Accelerometer data: {data}")


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    # you can read the current accelerometer data
    print(f"Current accelerometer reading: {microbit.accelerometer.read()}")

    # you can check how often accelerometer updates will occur if you listen to them with notify
    print(f"Current period: {microbit.accelerometer.read_period()}")

    # you can listen for accelerometer data updates
    microbit.accelerometer.notify(accelerometer_data)

    time.sleep(5)

    # you can change the update interval
    print("Now slow down updates to 160 milliseconds")
    microbit.accelerometer.set_period(160)

    print(f"Accelerometer updates will now occur every {microbit.accelerometer.read_period()} milliseconds")

    time.sleep(5)
# }
