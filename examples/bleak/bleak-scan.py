#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bleak import BleakScanner
import asyncio


async def main(timeout):
    devices = await BleakScanner.discover(timeout)
    for d in devices:
        print(d)


asyncio.run(main(10))
