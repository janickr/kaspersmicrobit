#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re
from typing import List, Union
from unittest.mock import patch
from uuid import UUID

import pytest
from bleak.backends.descriptor import BleakGATTDescriptor
from bleak.backends.service import BleakGATTService

from kaspersmicrobit.bluetoothdevice import BluetoothDevice, ThreadEventLoop
from kaspersmicrobit.errors import BluetoothCharacteristicNotFound, BluetoothServiceNotFound
from kaspersmicrobit.bluetoothprofile.characteristics import Characteristic
from kaspersmicrobit.bluetoothprofile.services import Service
from bleak import BleakGATTCharacteristic, BleakGATTServiceCollection


class StubBleakGATTService(BleakGATTService):
    def __init__(self, handle: int, service: Service):
        super().__init__(service)
        self._handle = handle
        self._uuid = service.value
        self._characteristics = []

    @property
    def handle(self) -> int:
        return self._handle

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def characteristics(self) -> List[BleakGATTCharacteristic]:
        return self._characteristics

    def add_characteristic(self, characteristic: BleakGATTCharacteristic):
        self._characteristics.append(characteristic)


class StubBleakGATTCharacteristic(BleakGATTCharacteristic):
    def __init__(self, characteristic: Characteristic):
        super().__init__(characteristic, 0)
        self._uuid = characteristic.value

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def service_uuid(self) -> str:
        pass

    @property
    def service_handle(self) -> int:
        pass

    @property
    def handle(self) -> int:
        pass

    @property
    def properties(self) -> List[str]:
        pass

    @property
    def descriptors(self) -> List[BleakGATTDescriptor]:
        pass

    def get_descriptor(self, specifier: Union[int, str, UUID]) -> Union[BleakGATTDescriptor, None]:
        pass

    def add_descriptor(self, descriptor: BleakGATTDescriptor):
        pass


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

    BluetoothDevice(client).notify(Service.TEMPERATURE, Characteristic.TEMPERATURE, callback)
    characteristic, new_callback = client.start_notify.call_args.args
    client.start_notify.assert_awaited()

    assert characteristic == gatt_characteristic

    new_callback(sender=-1, data=b'the data')
    assert callback_data == b'the data'


def test_notify_suggests_do_in_tkinter_on_tk_error(client):
    gatt_characteristic = setup_characteristic(client, Service.TEMPERATURE, Characteristic.TEMPERATURE)
    client.start_notify.return_value = None

    def callback(sender, data):
        raise RuntimeError("main thread is not in main loop")

    BluetoothDevice(client).notify(Service.TEMPERATURE, Characteristic.TEMPERATURE, callback)
    characteristic, new_callback = client.start_notify.call_args.args
    client.start_notify.assert_awaited()

    assert characteristic == gatt_characteristic

    with pytest.raises(RuntimeError, match=r"You tried to call tkinter API.*"):
        new_callback(sender=-1, data=b'this should fail')


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
    gatt_characteristic = StubBleakGATTCharacteristic(characteristic)
    gatt_service = StubBleakGATTService(1, service)
    gatt_service.add_characteristic(gatt_characteristic)
    collection = BleakGATTServiceCollection()
    collection.add_service(gatt_service)
    client.services = collection
    return gatt_characteristic
