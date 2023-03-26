#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import time

from kaspersmicrobit import KaspersMicrobit

logging.basicConfig(level=logging.INFO)

# example {


def print_temperature(temperature):
    print(f"Temperature update: {temperature}°C")


with KaspersMicrobit.find_one_microbit() as microbit:
    # read the current temperature / lees de huidige temperatuur
    print(f"The temperature is now: {microbit.temperature.read()}")

    # check how often temperature updates will occur if you listen to them with notify
    # / lees hoe vaak temperatuur updates doorgestuurd worden wanneer je er naar luistert met notify
    print(f"Listen for temperature updates every {microbit.temperature.read_period()} milliseconds")

    # listen for temperature updates / luister naar updates van de thermometer
    microbit.temperature.notify(print_temperature)

    time.sleep(5)

    # change the update interval / wijzig het update interval
    print("Now slow down updates to 3000 milliseconds")
    microbit.temperature.set_period(3000)

    print(f"Temperature updates will now occur every {microbit.temperature.read_period()} milliseconds")

    time.sleep(15)
# }
