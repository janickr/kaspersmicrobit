#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from kaspersmicrobit import KaspersMicrobit

logging.basicConfig(level=logging.INFO)


with KaspersMicrobit.find_one_microbit() as microbit:
    print(f"         Model # : {microbit.device_information.read_model_number()}")
    print(f"        Serial # : {microbit.device_information.read_serial_number()}")
    print(f"Firmware revision: {microbit.device_information.read_firmware_revision()}")

    # Although the hardware revision and manufacturer name are specified in the micro:bit bluetooth profile,
    # they were not present on the micro:bits I tested
    # print(f"Hardware revision: {microbit.device_information.read_hardware_revision()}")
    # print(f"Manufacturer name: {microbit.device_information.read_manufacturer_name()}")
