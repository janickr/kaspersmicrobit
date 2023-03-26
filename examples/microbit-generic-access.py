#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging

from kaspersmicrobit import KaspersMicrobit

logging.basicConfig(level=logging.INFO)

with KaspersMicrobit.find_one_microbit() as microbit:
    print(f"Device name: {microbit.generic_access.read_device_name()}")
