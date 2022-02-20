#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import concurrent.futures
from abc import ABCMeta, abstractmethod
from typing import Union, Callable
from bleak import BleakClient
import asyncio
from threading import Thread
from .bluetoothprofile.characteristics import Characteristic

ByteData = Union[bytes, bytearray, memoryview]


class BluetoothEventLoop(metaclass=ABCMeta):
    @abstractmethod
    def run_async(self, coroutine) -> concurrent.futures.Future:
        pass

    @abstractmethod
    def create_future(self) -> asyncio.Future:
        pass


class ThreadEventLoop(BluetoothEventLoop):
    _singleton = None

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        Thread(target=ThreadEventLoop._start_background_loop, args=(self.loop,), daemon=True).start()

    @staticmethod
    def _start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def run_async(self, coroutine) -> concurrent.futures.Future:
        return asyncio.run_coroutine_threadsafe(coroutine, self.loop)

    def create_future(self) -> asyncio.Future:
        return self.loop.create_future()

    @staticmethod
    def single_thread():
        if not ThreadEventLoop._singleton:
            ThreadEventLoop._singleton = ThreadEventLoop()

        return ThreadEventLoop._singleton


class BluetoothDevice:

    def __init__(self, address: str, loop: BluetoothEventLoop = None):
        self.loop = loop if loop else ThreadEventLoop.single_thread()
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

    def notify(self, characteristic: Characteristic, callback: Callable[[int, bytearray], None]) -> None:
        def wrap_try_catch(fn: Callable[[int, bytearray], None]):
            def suggest_do_in_tkinter(sender: int, data: bytearray):
                try:
                    fn(sender, data)
                except RuntimeError as e:
                    message, = e.args
                    if message == "main thread is not in main loop":
                        raise RuntimeError(
                            """You tried to call tkinter API from within a KaspersMicrobit notification callback.
                            This is probably not what you want. If your really want to do this wrap your callback in
                            kaspersmicrobit.tkinter.do_in_tkinter(tk, your_callback)""") from e
                    raise e
            return suggest_do_in_tkinter

        self.loop.run_async(self.client.start_notify(characteristic.value, wrap_try_catch(callback))).result()
        print("notify")

    def wait_for(self, characteristic: Characteristic) -> concurrent.futures.Future[ByteData]:
        future = self.loop.create_future()

        print("wait-for notify")
        self.loop.run_async(self.client.start_notify(characteristic.value,
                                                     lambda sender, data: future.set_result(data))).result()

        async def await_future():
            return await future

        print("wait-for future")
        return self.loop.run_async(await_future())
