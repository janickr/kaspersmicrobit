#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bleak import BleakClient
import asyncio


MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


async def device_info(address: str):
    async with BleakClient(address) as client:
        for service in client.services:
            print(f"[Service] {service}")
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                        print(
                            f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                        )
                    except Exception as e:
                        print(
                            f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}"
                        )
                else:
                    value = None
                    print(
                        f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                    )
                for descriptor in char.descriptors:
                    try:
                        value = bytes(
                            await client.read_gatt_descriptor(descriptor.handle)
                        )
                        print(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                    except Exception as e:
                        print(f"\t\t[Descriptor] {descriptor}) | Value: {e}")


asyncio.run(device_info(MICROBIT_BLUETOOTH_ADDRESS))
