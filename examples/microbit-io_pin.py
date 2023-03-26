#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import time

from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.io_pin import PinIOConfiguration, Pin, PinIO, PinADConfiguration, PinAD

logging.basicConfig(level=logging.INFO)

# example {


def print_pin_data(data):
    print(f"pin data update: {data}")


with KaspersMicrobit.find_one_microbit() as microbit:
    # set P5 (Button A) and P11 (Button B) as INPUT pins / configureer P5 (Knop A) en P11 (Knop B) als INPUT pins
    io_config = PinIOConfiguration()
    io_config[Pin.P5] = PinIO.INPUT
    io_config[Pin.P11] = PinIO.INPUT
    microbit.io_pin.write_io_configuration(io_config)

    # read the IO pin configuration / lees de IO pin configuration
    print(f"io pin configuration: {microbit.io_pin.read_io_configuration()}")

    # set P5 (Button A) and P11 (Button B) as DIGITAL pins / configureer P5 (Knop A) en P11 (Knop B) als DIGITAL pins
    ad_config = PinADConfiguration()
    ad_config[Pin.P5] = PinAD.DIGITAL
    ad_config[Pin.P11] = PinAD.DIGITAL
    microbit.io_pin.write_ad_configuration(ad_config)

    # read the AD pin configuration / lees de AD pin configuration
    print(f"ad pin configuration: {microbit.io_pin.read_ad_configuration()}")

    # Read the pin data (gets the data for all input pins: P5 and P11)
    # / Lees de pin data (geeft data voor alle input pins: P5 en P11)
    pin_data = microbit.io_pin.read_data()
    print(f"pin data: {pin_data}")

    # listen for input pin events / luister naar input pin wijzigingen
    microbit.io_pin.notify_data(print_pin_data)
    print("Push buttons A or B, and watch the changes in P5 and P11")

    time.sleep(10)

# }
