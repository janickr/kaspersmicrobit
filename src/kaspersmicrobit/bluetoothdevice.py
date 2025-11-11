#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio
import concurrent.futures
import logging
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Union, Callable
from bleak import BleakClient, BleakGATTCharacteristic
from threading import Thread
from .bluetoothprofile.characteristics import Characteristic
from .bluetoothprofile.services import Service
from .errors import BluetoothCharacteristicNotFound, BluetoothServiceNotFound

logger = logging.getLogger(__name__)

ByteData = Union[bytes, bytearray, memoryview]


class BluetoothEventLoop(metaclass=ABCMeta):
    @abstractmethod
    def run_async(self, coroutine) -> concurrent.futures.Future:
        pass

    @abstractmethod
    def wrap_future(self, future: concurrent.futures.Future) -> asyncio.Future:
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

    def wrap_future(self, future: concurrent.futures.Future) -> asyncio.Future:
        return asyncio.wrap_future(future, loop=self.loop)

    def create_future(self) -> asyncio.Future:
        return self.loop.create_future()

    @staticmethod
    def single_thread():
        if not ThreadEventLoop._singleton:
            ThreadEventLoop._singleton = ThreadEventLoop()

        return ThreadEventLoop._singleton


class BluetoothDevice:
    _callback_executor = ThreadPoolExecutor()

    def __init__(self, client: BleakClient, loop: BluetoothEventLoop = None):
        self._loop = loop if loop else ThreadEventLoop.single_thread()
        self._client = client

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self) -> None:
        logger.info("(%s) Connecting...", self._client.address)
        self._loop.run_async(self._client.connect()).result()
        logger.info("(%s) Connected", self._client.address)

    def disconnect(self) -> None:
        logger.info("(%s) Disconnecting...", self._client.address)
        self._loop.run_async(self._client.disconnect()).result()
        logger.info("(%s) Disconnected", self._client.address)

    def read(self, service: Service, characteristic: Characteristic) -> bytearray:
        logger.info("(%s) Reading %s %s", self._client.address, service, characteristic)
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        result = self._loop.run_async(self._client.read_gatt_char(gatt_characteristic)).result()
        logger.info("(%s) Read %s %s, data=%s", self._client.address, service, characteristic, result)
        return result

    def write(self, service: Service, characteristic: Characteristic, data: ByteData) -> None:
        logger.info("(%s) Writing %s %s, data=%s", self._client.address, service, characteristic, data)
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        self._loop.run_async(self._client.write_gatt_char(gatt_characteristic, data)).result()
        logger.info("(%s) Written %s %s", self._client.address, service, characteristic)

    def notify(self, service: Service, characteristic: Characteristic,
               callback: Callable[[BleakGATTCharacteristic, bytearray], None]) -> None:
        def wrap_try_catch(fn: Callable[[BleakGATTCharacteristic, bytearray], None]):
            def suggest_do_in_tkinter(sender: BleakGATTCharacteristic, data: bytearray) -> None:
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

        def do_on_callback_executor(fn: Callable[[BleakGATTCharacteristic, bytearray], None]):
            async def submit_to_executor(sender: BleakGATTCharacteristic, data: bytearray):
                await self._loop.wrap_future(BluetoothDevice._callback_executor.submit(fn, sender, data))

            return submit_to_executor

        logger.info("(%s) Enable notify %s %s", self._client.address, service, characteristic)
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        self._loop.run_async(
            self._client.start_notify(gatt_characteristic, do_on_callback_executor(wrap_try_catch(callback)))
        ).result()
        logger.info("(%s) Enabled notify %s %s", self._client.address, service, characteristic)

    def wait_for(self, service: Service, characteristic: Characteristic) -> concurrent.futures.Future[ByteData]:
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        asyncio_future = self._loop.create_future()
        address = self._client.address

        def set_result_and_stop_notify(sender, data):
            asyncio_future.set_result(data)
            logger.info("(%s) %s %s data received=%s", address, service, characteristic, data)

        logger.info("(%s) Wait for notify %s %s", address, service, characteristic)
        self._loop.run_async(self._client.start_notify(gatt_characteristic, set_result_and_stop_notify)).result()

        async def await_future_and_stop_notify():
            future = await asyncio_future
            await self._client.stop_notify(gatt_characteristic)
            logger.info("(%s) Stopped waiting for notify %s %s", self._client.address, service, characteristic)
            return future

        return self._loop.run_async(await_future_and_stop_notify())

    def is_service_available(self, service: Service) -> bool:
        return not self._get_gatt_service(service) is None

    def address(self) -> str:
        return self._client.address

    def name(self) -> str:
        return self._client.name

    def _find_gatt_attribute(self, service: Service, characteristic: Characteristic) -> BleakGATTCharacteristic:
        gatt_service = self._get_gatt_service(service)
        if not gatt_service:
            raise BluetoothServiceNotFound(self._client, service)

        gatt_characteristic = gatt_service.get_characteristic(characteristic.value)
        if not gatt_characteristic:
            raise BluetoothCharacteristicNotFound(self._client, service, characteristic)

        return gatt_characteristic

    def _get_gatt_service(self, service):
        return self._client.services.get_service(service.value)
