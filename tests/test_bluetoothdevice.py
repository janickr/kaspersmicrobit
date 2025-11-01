#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio
import inspect
import re
from typing import List, Union, Callable, Awaitable
from unittest.mock import patch
from uuid import UUID
from concurrent.futures import TimeoutError

import pytest
from bleak.backends.descriptor import BleakGATTDescriptor
from bleak.backends.service import BleakGATTService

from kaspersmicrobit.bluetoothdevice import BluetoothDevice, ThreadEventLoop
from kaspersmicrobit.errors import BluetoothCharacteristicNotFound, BluetoothServiceNotFound
from kaspersmicrobit.bluetoothprofile.characteristics import Characteristic
from kaspersmicrobit.bluetoothprofile.services import Service
from bleak import BleakGATTCharacteristic, BleakGATTServiceCollection


@pytest.fixture
def client():
    with patch('bleak.BleakClient', autospec=True) as client_type:
        yield client_type.return_value


def test_connect(client):
    client.connect.return_value = None

    BluetoothDevice(client).connect()

    client.connect.assert_called_with()


def test_disconnect(client):
    client.disconnect.return_value = None

    BluetoothDevice(client).disconnect()

    client.disconnect.assert_called_with()


def test_read(client):
    client.read_gatt_char.return_value = b'test device name'
    gatt_characteristic = setup_characteristic(client, Service.DEVICE_INFORMATION, Characteristic.DEVICE_NAME)

    read_result = BluetoothDevice(client).read(Service.DEVICE_INFORMATION, Characteristic.DEVICE_NAME)

    client.read_gatt_char.assert_called_with(gatt_characteristic)

    assert read_result == b'test device name'


def test_write(client):
    client.write_gatt_char.return_value = None
    gatt_characteristic = setup_characteristic(client, Service.DEVICE_INFORMATION, Characteristic.DEVICE_NAME)

    BluetoothDevice(client).write(Service.DEVICE_INFORMATION, Characteristic.DEVICE_NAME, b'test device name')

    client.write_gatt_char.assert_called_with(gatt_characteristic, b'test device name')
    client.write_gatt_char.assert_awaited()


def test_notify(client):
    gatt_characteristic = setup_characteristic(client, Service.TEMPERATURE, Characteristic.TEMPERATURE)

    client.start_notify.return_value = None
    callback_data = None

    def callback(sender, data):
        nonlocal callback_data
        callback_data = data

    device = BluetoothDevice(client)
    device.notify(Service.TEMPERATURE, Characteristic.TEMPERATURE, callback)
    characteristic, new_callback = client.start_notify.call_args.args
    client.start_notify.assert_awaited()

    assert characteristic == gatt_characteristic

    invoke_callback(device, new_callback, sender=characteristic, data=b'the data').result(1)
    assert callback_data == b'the data'


def test_notify_suggests_do_in_tkinter_on_tk_error(client):
    gatt_characteristic = setup_characteristic(client, Service.TEMPERATURE, Characteristic.TEMPERATURE)
    client.start_notify.return_value = None

    def callback(sender, data):
        raise RuntimeError("main thread is not in main loop")

    device = BluetoothDevice(client)
    device.notify(Service.TEMPERATURE, Characteristic.TEMPERATURE, callback)
    characteristic, new_callback = client.start_notify.call_args.args
    client.start_notify.assert_awaited()

    assert characteristic == gatt_characteristic

    with pytest.raises(RuntimeError, match=r"You tried to call tkinter API.*"):
        invoke_callback(device, new_callback, sender=characteristic, data=b'this should fail').result(1)


def test_notify_if_call_on_device_in_callback_it_does_not_block(client):
    gatt_characteristic = setup_characteristic(client, Service.TEMPERATURE, Characteristic.TEMPERATURE)
    client.start_notify.return_value = None

    device = BluetoothDevice(client)

    def callback(sender, data):
        device.read(Service.TEMPERATURE, Characteristic.TEMPERATURE)

    device.notify(Service.TEMPERATURE, Characteristic.TEMPERATURE, callback)
    characteristic, new_callback = client.start_notify.call_args.args
    client.start_notify.assert_awaited()

    assert characteristic == gatt_characteristic

    future = invoke_callback(device, new_callback, sender=characteristic, data=b'this should not block')

    async def should_be_invoked():
        pass

    try:
        device._loop.run_async(should_be_invoked()).result(3)
    except TimeoutError:
        ThreadEventLoop._singleton = None  # throw away the broken eventloop + Thread, so other tests run clean
        pytest.fail('Eventloop was blocked')

    future.result()
    client.read_gatt_char.assert_awaited()
    client.read_gatt_char.assert_called_with(characteristic)


def invoke_callback(
        device: BluetoothDevice,
        fn: Callable[[BleakGATTCharacteristic, bytearray], Union[None, Awaitable[None]]],
        sender: BleakGATTCharacteristic, data: bytes):

    async def call_the_callback(fn, sender, data):
        if inspect.iscoroutinefunction(fn):
            f = asyncio.ensure_future(fn(sender, data), loop=device._loop.loop)
            await asyncio.wait_for(f, 3)
        else:
            fn(sender, data)

    return device._loop.run_async(call_the_callback(fn, sender, bytearray(data)))


def test_wait_for_calls_notify_and_blocks_until_first_notification(client):
    gatt_characteristic = setup_characteristic(client, Service.MAGNETOMETER, Characteristic.MAGNETOMETER_CALIBRATION)
    client.start_notify.return_value = None
    client.stop_notify.return_value = None
    future = BluetoothDevice(client).wait_for(Service.MAGNETOMETER, Characteristic.MAGNETOMETER_CALIBRATION)
    characteristic, callback = client.start_notify.call_args.args
    client.start_notify.assert_awaited()

    assert characteristic == gatt_characteristic
    assert not future.done()

    async def call():
        callback(sender=-1, data=b'the data you were waiting for')

    ThreadEventLoop.single_thread().run_async(call())

    assert future.result() == b'the data you were waiting for'


def test_wait_for_unsubscribes_after_result_available(client):
    gatt_characteristic = setup_characteristic(client, Service.MAGNETOMETER, Characteristic.MAGNETOMETER_CALIBRATION)
    client.start_notify.return_value = None
    client.stop_notify.return_value = None
    future = BluetoothDevice(client).wait_for(Service.MAGNETOMETER, Characteristic.MAGNETOMETER_CALIBRATION)
    characteristic, callback = client.start_notify.call_args.args

    assert characteristic == gatt_characteristic
    client.stop_notify.assert_not_called()

    async def call():
        callback(sender=-1, data=b'the data you were waiting for')

    ThreadEventLoop.single_thread().run_async(call())

    future.result()
    client.stop_notify.assert_called_with(gatt_characteristic)


def test_service_not_available(client):
    setup_characteristic(client, Service.DEVICE_INFORMATION, Characteristic.DEVICE_NAME)

    with pytest.raises(BluetoothServiceNotFound,
                       match=re.escape(
                           'Could not find the service '
                           'Service.TEMPERATURE (uuid=e95d6100-251d-470a-a062-fa1922dfa9a8)\n'
                           'The available services on this micro:bit are:\n'
                           '  - Device Information             '
                           '(Service.DEVICE_INFORMATION  uuid=0000180a-0000-1000-8000-00805f9b34fb)\n\n'
                           'Is this micro:bit loaded with the correct ".hex" file?'
                       )):
        BluetoothDevice(client).read(Service.TEMPERATURE, Characteristic.TEMPERATURE)


def test_characteristic_not_found(client):
    setup_characteristic(client, Service.DEVICE_INFORMATION, Characteristic.DEVICE_NAME)

    with pytest.raises(BluetoothCharacteristicNotFound,
                       match=re.escape(
                           'Could not find the characteristic '
                           'FIRMWARE_REVISION_STRING (uuid=00002a26-0000-1000-8000-00805f9b34fb)\n'
                           'The available characteristics of the service '
                           'Service.DEVICE_INFORMATION on this micro:bit are:\n'
                           '  - Device Name                         '
                           '(Characteristic.DEVICE_NAME               uuid=00002a00-0000-1000-8000-00805f9b34fb)'
                       )):
        BluetoothDevice(client).read(Service.DEVICE_INFORMATION, Characteristic.FIRMWARE_REVISION_STRING)


def test_is_service_available(client):
    setup_characteristic(client, Service.DEVICE_INFORMATION, Characteristic.DEVICE_NAME)

    device = BluetoothDevice(client)

    assert device.is_service_available(Service.DEVICE_INFORMATION)
    assert not device.is_service_available(Service.ACCELEROMETER)


def setup_characteristic(client, service, characteristic):
    gatt_service = BleakGATTService(service, 1, service.value)
    gatt_characteristic = BleakGATTCharacteristic(characteristic, 0, characteristic.value, [],  lambda: 0, gatt_service)
    gatt_service.add_characteristic(gatt_characteristic)
    collection = BleakGATTServiceCollection()
    collection.add_service(gatt_service)
    client.services = collection
    return gatt_characteristic
