#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio
import concurrent.futures
import logging
from abc import ABCMeta, abstractmethod
from typing import Union, Callable
from bleak import BleakClient, BleakGATTCharacteristic
from threading import Thread
from .bluetoothprofile.characteristics import Characteristic
from .bluetoothprofile.services import Service

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


class BluetoothServiceNotFound(Exception):
    def __init__(self, client: BleakClient, service: Service):
        available_services = '\n'.join(
            [
                f'  - {gatt_service.description:30}'
                f' ({str(Service.lookup(gatt_service.uuid)):27} uuid={gatt_service.uuid})'
                for gatt_service in client.services
            ]
        )
        super().__init__(
            f'Could not find the service {service} (uuid={service.value})\n'
            f'The available services on this micro:bit are:\n'
            f'{ available_services }\n\n'
            f'Is this micro:bit loaded with the correct ".hex" file?'
        )
        self.service = service


class BluetoothCharacteristicNotFound(Exception):
    def __init__(self, client: BleakClient, service: Service, characteristic: Characteristic):
        available_characteristics = '\n'.join(
            [
                f'  - {gatt_characteristic.description:35}'
                f' ({str(Characteristic.lookup(gatt_characteristic.uuid)):40} uuid={gatt_characteristic.uuid})'
                for gatt_characteristic in client.services.get_service(service.value).characteristics
            ]
        )
        super().__init__(
            f'Could not find the characteristic {characteristic.name} (uuid={characteristic.value})\n'
            f'The available characteristics of the service {service} on this micro:bit are:\n'
            f'{available_characteristics}')
        self.service = service


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

    def read(self, service: Service, characteristic: Characteristic) -> bytearray:
        logger.info("Reading %s %s", service, characteristic)
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        result = self.loop.run_async(self.client.read_gatt_char(gatt_characteristic)).result()
        logger.info("Read %s %s, data=%s", service, characteristic, result)
        return result

    def write(self, service: Service, characteristic: Characteristic, data: ByteData) -> None:
        logger.info("Writing %s %s, data=%s", service, characteristic, data)
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        self.loop.run_async(self.client.write_gatt_char(gatt_characteristic, data)).result()
        logger.info("Written %s %s", service, characteristic)

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

        logger.info("Enable notify %s %s", service, characteristic)
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        self.loop.run_async(self.client.start_notify(gatt_characteristic, wrap_try_catch(callback))).result()
        logger.info("Enabled notify %s %s", service, characteristic)

    def wait_for(self, service: Service, characteristic: Characteristic) -> concurrent.futures.Future[ByteData]:
        gatt_characteristic = self._find_gatt_attribute(service, characteristic)
        asyncio_future = self.loop.create_future()

        def set_result_and_stop_notify(sender, data):
            asyncio_future.set_result(data)
            self.client.stop_notify(gatt_characteristic)
            logger.info("Stopped waiting for notify %s %s data received=%s", service, characteristic, data)

        logger.info("Wait for notify %s %s", service, characteristic)
        self.loop.run_async(self.client.start_notify(gatt_characteristic, set_result_and_stop_notify)).result()

        async def await_future():
            return await asyncio_future

        return self.loop.run_async(await_future())

    def is_service_available(self, service: Service) -> bool:
        return not self._get_gatt_service(service) is None

    def _find_gatt_attribute(self, service: Service, characteristic: Characteristic) -> BleakGATTCharacteristic:
        gatt_service = self._get_gatt_service(service)
        if not gatt_service:
            raise BluetoothServiceNotFound(self.client, service)

        gatt_characteristic = gatt_service.get_characteristic(characteristic.value)
        if not gatt_characteristic:
            raise BluetoothCharacteristicNotFound(self.client, service, characteristic)

        return gatt_characteristic

    def _get_gatt_service(self, service):
        return self.client.services.get_service(service.value)
