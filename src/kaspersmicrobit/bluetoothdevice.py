#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio
import concurrent.futures
import logging
from abc import ABCMeta, abstractmethod
from typing import Union, Callable
from bleak import BleakClient
from threading import Thread
from .bluetoothprofile.characteristics import Characteristic

logger = logging.getLogger(__name__)

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
        logger.info("Connecting...")
        self.loop.run_async(self.client.connect()).result()
        logger.info("Connected")

    def disconnect(self) -> None:
        logger.info("Disconnecting...")
        self.loop.run_async(self.client.disconnect()).result()
        logger.info("Disconnected")

    def read(self, characteristic: Characteristic) -> bytearray:
        logger.info("Reading %s", characteristic)
        result = self.loop.run_async(self.client.read_gatt_char(characteristic.value)).result()
        logger.info("Read %s, data=%s", characteristic, result)
        return result

    def write(self, characteristic: Characteristic, data: ByteData) -> None:
        logger.info("Writing %s, data=%s", characteristic, data)
        self.loop.run_async(self.client.write_gatt_char(characteristic.value, data)).result()
        logger.info("Written %s", characteristic)

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

        logger.info("Enable notify %s", characteristic)
        self.loop.run_async(self.client.start_notify(characteristic.value, wrap_try_catch(callback))).result()
        logger.info("Enabled notify %s", characteristic)

    def wait_for(self, characteristic: Characteristic) -> concurrent.futures.Future[ByteData]:
        asyncio_future = self.loop.create_future()

        def set_result_and_stop_notify(sender, data):
            asyncio_future.set_result(data)
            self.client.stop_notify(characteristic.value)
            logger.info("Stopped waiting for notify %s data received=%s", characteristic, data)

        logger.info("Wait for notify %s", characteristic)
        self.loop.run_async(self.client.start_notify(characteristic.value, set_result_and_stop_notify)).result()

        async def await_future():
            return await asyncio_future

        return self.loop.run_async(await_future())
