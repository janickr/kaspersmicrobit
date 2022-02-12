#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time

from kaspersmicrobit import KaspersMicrobit

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'
# example {


def print_temperature(temperature):
    print(f"Temperature update: {temperature}°C")


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    # you can read the current temperature
    print(f"The temperature is now: {microbit.temperature.read()}")

    # you can check how often temperature updates will occur if you listen to them with notify
    print(f"Listen for temperature updates every {microbit.temperature.read_period()} milliseconds")

    # you can listen for temperature updates
    microbit.temperature.notify(print_temperature)

    time.sleep(5)

    # you can change the update interval
    print("Now slow down updates to 3000 milliseconds")
    microbit.temperature.set_period(3000)

    print(f"Temperature updates will now occur every {microbit.temperature.read_period()} milliseconds")

    time.sleep(15)
# }
