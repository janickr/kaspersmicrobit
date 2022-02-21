from unittest.mock import patch, ANY

import pytest
from kaspersmicrobit.bluetoothdevice import BluetoothDevice, ThreadEventLoop
from kaspersmicrobit.bluetoothprofile.characteristics import Characteristic


def test_client_is_created_with_address():
    device = BluetoothDevice("address")

    assert device.client.address == "address"


@patch('kaspersmicrobit.bluetoothdevice.BleakClient.connect', autospec=True)
def test_connect(connect):
    BluetoothDevice("address").connect()

    connect.assert_called_with(ANY)


@patch('kaspersmicrobit.bluetoothdevice.BleakClient.disconnect', autospec=True)
def test_disconnect(disconnect):
    BluetoothDevice("address").disconnect()

    disconnect.assert_called_with(ANY)


@patch('kaspersmicrobit.bluetoothdevice.BleakClient.read_gatt_char', autospec=True, return_value=b'test device name')
def test_read(read_gatt_char):
    read_result = BluetoothDevice("address").read(Characteristic.DEVICE_NAME)

    read_gatt_char.assert_called_with(ANY, Characteristic.DEVICE_NAME.value)
    assert read_result == b'test device name'


@patch('kaspersmicrobit.bluetoothdevice.BleakClient.write_gatt_char', autospec=True)
def test_write(write_gatt_char):
    BluetoothDevice("address").write(Characteristic.DEVICE_NAME, b'test device name')

    write_gatt_char.assert_called_with(ANY, Characteristic.DEVICE_NAME.value, b'test device name')


@patch('kaspersmicrobit.bluetoothdevice.BleakClient.start_notify', autospec=True)
def test_notify(notify):
    callback_data = None

    def callback(sender, data):
        nonlocal callback_data
        callback_data = data

    BluetoothDevice("address").notify(Characteristic.TEMPERATURE, callback)
    client, characteristic, new_callback = notify.call_args.args

    assert characteristic == Characteristic.TEMPERATURE.value

    new_callback(sender=-1, data=b'the data')
    assert callback_data == b'the data'


@patch('kaspersmicrobit.bluetoothdevice.BleakClient.start_notify', autospec=True)
def test_notify_suggests_do_in_tkinter_on_tk_error(notify):
    def callback(sender, data):
        raise RuntimeError("main thread is not in main loop")

    BluetoothDevice("address").notify(Characteristic.TEMPERATURE, callback)
    client, characteristic, new_callback = notify.call_args.args

    assert characteristic == Characteristic.TEMPERATURE.value

    with pytest.raises(RuntimeError, match=r"You tried to call tkinter API.*"):
        new_callback(sender=-1, data=b'this should fail')


@patch('kaspersmicrobit.bluetoothdevice.BleakClient.start_notify', autospec=True)
def test_wait_for_calls_notify_and_blocks_until_first_notification(start_notify):
    future = BluetoothDevice("address").wait_for(Characteristic.MAGNETOMETER_CALIBRATION)
    client, characteristic, callback = start_notify.call_args.args

    assert characteristic == Characteristic.MAGNETOMETER_CALIBRATION.value
    assert not future.done()

    async def call():
        callback(sender=-1, data=b'the data you were waiting for')

    ThreadEventLoop.single_thread().run_async(call())

    assert future.result() == b'the data you were waiting for'


@patch('kaspersmicrobit.bluetoothdevice.BleakClient.start_notify', autospec=True)
@patch('kaspersmicrobit.bluetoothdevice.BleakClient.stop_notify', autospec=True)
def test_wait_for_unsubscribes_after_result_available(stop_notify, start_notify):
    future = BluetoothDevice("address").wait_for(Characteristic.MAGNETOMETER_CALIBRATION)
    client, characteristic, callback = start_notify.call_args.args

    assert characteristic == Characteristic.MAGNETOMETER_CALIBRATION.value
    stop_notify.assert_not_called()

    async def call():
        callback(sender=-1, data=b'the data you were waiting for')

    ThreadEventLoop.single_thread().run_async(call())

    future.result()
    stop_notify.assert_called_with(ANY, Characteristic.MAGNETOMETER_CALIBRATION.value)
