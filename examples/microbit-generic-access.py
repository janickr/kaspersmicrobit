#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging

from src.kaspersmicrobit import KaspersMicrobit

logging.basicConfig(level=logging.INFO)

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'

with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    print(f"Device name: {microbit.generic_access.read_device_name()}")
