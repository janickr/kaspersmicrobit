#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Union
from bleak import BleakClient
import asyncio
from threading import Thread
from .characteristics import Characteristic

ByteData = Union[bytes, bytearray, memoryview]


class ThreadEventLoop:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        Thread(target=ThreadEventLoop._start_background_loop, args=(self.loop,), daemon=True).start()

    @staticmethod
    def _start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def run_async(self, coroutine):
        return asyncio.run_coroutine_threadsafe(coroutine, self.loop)


class BluetoothEventLoop:
    _single_thread = ThreadEventLoop()

    @staticmethod
    def single_thread():
        return BluetoothEventLoop._single_thread


class BluetoothDevice:

    def __init__(self, address: str, loop=BluetoothEventLoop.single_thread()):
        self.loop = loop
        self.client = BleakClient(address)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self) -> None:
        print("connecting")
        self.loop.run_async(self.client.connect()).result()
        print("connected")

    def disconnect(self) -> None:
        print("disconnecting")
        self.loop.run_async(self.client.disconnect()).result()
        print("disconnected")

    def read(self, characteristic: Characteristic) -> bytearray:
        print("reading")
        result = self.loop.run_async(self.client.read_gatt_char(characteristic.value)).result()
        print("read")
        return result

    def write(self, characteristic: Characteristic, data: ByteData) -> None:
        print("writing")
        self.loop.run_async(self.client.write_gatt_char(characteristic.value, data)).result()
        print("written")

    def notify(self, characteristic: Characteristic, callback) -> None:
        self.loop.run_async(self.client.start_notify(characteristic.value, callback)).result()
        print("notify")
