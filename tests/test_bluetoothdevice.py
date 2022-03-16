#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

import pytest
from kaspersmicrobit.bluetoothdevice import BluetoothDevice, ThreadEventLoop
from kaspersmicrobit.bluetoothprofile.characteristics import Characteristic


@pytest.fixture
def client():
    with patch('kaspersmicrobit.bluetoothdevice.BleakClient', autospec=True) as client_type:
        yield client_type.return_value


def test_connect(client):
    client.connect.return_value = None

    BluetoothDevice("address").connect()

    client.connect.assert_called_with()


def test_disconnect(client):
    client.disconnect.return_value = None

    BluetoothDevice("address").disconnect()

    client.disconnect.assert_called_with()


def test_read(client):
    client.read_gatt_char.return_value = b'test device name'

    read_result = BluetoothDevice("address").read(Characteristic.DEVICE_NAME)

    client.read_gatt_char.assert_called_with(Characteristic.DEVICE_NAME.value)

    assert read_result == b'test device name'


def test_write(client):
    client.write_gatt_char.return_value = None
    BluetoothDevice("address").write(Characteristic.DEVICE_NAME, b'test device name')

    client.write_gatt_char.assert_called_with(Characteristic.DEVICE_NAME.value, b'test device name')
    client.write_gatt_char.assert_awaited()


def test_notify(client):
    client.start_notify.return_value = None
    callback_data = None

    def callback(sender, data):
        nonlocal callback_data
        callback_data = data

    BluetoothDevice("address").notify(Characteristic.TEMPERATURE, callback)
    characteristic, new_callback = client.start_notify.call_args.args
    client.start_notify.assert_awaited()

    assert characteristic == Characteristic.TEMPERATURE.value

    new_callback(sender=-1, data=b'the data')
    assert callback_data == b'the data'


def test_notify_suggests_do_in_tkinter_on_tk_error(client):
    client.start_notify.return_value = None

    def callback(sender, data):
        raise RuntimeError("main thread is not in main loop")

    BluetoothDevice("address").notify(Characteristic.TEMPERATURE, callback)
    characteristic, new_callback = client.start_notify.call_args.args
    client.start_notify.assert_awaited()

    assert characteristic == Characteristic.TEMPERATURE.value

    with pytest.raises(RuntimeError, match=r"You tried to call tkinter API.*"):
        new_callback(sender=-1, data=b'this should fail')


def test_wait_for_calls_notify_and_blocks_until_first_notification(client):
    client.start_notify.return_value = None
    future = BluetoothDevice("address").wait_for(Characteristic.MAGNETOMETER_CALIBRATION)
    characteristic, callback = client.start_notify.call_args.args
    client.start_notify.assert_awaited()

    assert characteristic == Characteristic.MAGNETOMETER_CALIBRATION.value
    assert not future.done()

    async def call():
        callback(sender=-1, data=b'the data you were waiting for')

    ThreadEventLoop.single_thread().run_async(call())

    assert future.result() == b'the data you were waiting for'


def test_wait_for_unsubscribes_after_result_available(client):
    client.start_notify.return_value = None
    client.stop_notify.return_value = None
    future = BluetoothDevice("address").wait_for(Characteristic.MAGNETOMETER_CALIBRATION)
    characteristic, callback = client.start_notify.call_args.args

    assert characteristic == Characteristic.MAGNETOMETER_CALIBRATION.value
    client.stop_notify.assert_not_called()

    async def call():
        callback(sender=-1, data=b'the data you were waiting for')

    ThreadEventLoop.single_thread().run_async(call())

    future.result()
    client.stop_notify.assert_called_with(Characteristic.MAGNETOMETER_CALIBRATION.value)
