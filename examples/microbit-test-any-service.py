#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

# example {

from kaspersmicrobit.bluetoothprofile.services import Service
from kaspersmicrobit.services.leddisplay import Image
from kaspersmicrobit import KaspersMicrobit
import platform

with KaspersMicrobit.find_one_microbit() as microbit:
    print(f'Platform: {platform.platform()}')
    print(f'Python version: {platform.python_version()}')
    print("")
    print(f'Bluetooth address: {microbit.address()}')
    print("")

    if microbit.generic_access.is_available():
        print(f'{Service.GENERIC_ACCESS} available')
        print(f"Device name: {microbit.generic_access.read_device_name()}")
    else:
        print(f'{Service.GENERIC_ACCESS} not found')

    print("")
    if microbit.device_information.is_available():
        print(f'{Service.DEVICE_INFORMATION} available')
        print(f"         Model # : {microbit.device_information.read_model_number()}")
        print(f"        Serial # : {microbit.device_information.read_serial_number()}")
        print(f"Firmware revision: {microbit.device_information.read_firmware_revision()}")
    else:
        print(f'{Service.DEVICE_INFORMATION} not found')

    print("")
    if microbit.accelerometer.is_available():
        print(f'{Service.ACCELEROMETER} available')
        print(f"data: {microbit.accelerometer.read()}")
    else:
        print(f'{Service.ACCELEROMETER} not found')

    print("")
    if microbit.buttons.is_available():
        print(f'{Service.BUTTON} available')
        print(f"Button a: {microbit.buttons.read_button_a()}")
        print(f"Button b: {microbit.buttons.read_button_b()}")
    else:
        print(f'{Service.BUTTON} not found')

    print("")
    if microbit.led.is_available():
        print(f'{Service.LED} available')
        microbit.led.show(Image.HAPPY)
    else:
        print(f'{Service.LED} not found')

    print("")
    if microbit.temperature.is_available():
        print(f'{Service.TEMPERATURE} available')
        print(f"The temperature is now: {microbit.temperature.read()}")
    else:
        print(f'{Service.TEMPERATURE} not found')

    print("")
    if microbit.uart.is_available():
        print(f'{Service.UART} available')
        microbit.uart.send_string("Hi\n")
    else:
        print(f'{Service.UART} not found')

    print("")
    if microbit.io_pin.is_available():
        print(f'{Service.IO_PIN} available')
        print(f"io pin configuration: {microbit.io_pin.read_io_configuration()}")
    else:
        print(f'{Service.IO_PIN} not found')

    print("")
    if microbit.magnetometer.is_available():
        print(f'{Service.MAGNETOMETER} available')
        print(f"Current period: {microbit.magnetometer.read_period()}")
        print(f"Data: {microbit.magnetometer.read_data()}")
    else:
        print(f'{Service.MAGNETOMETER} not found')

    print("")
    if microbit.events.is_available():
        print(f'{Service.EVENT} available')
    else:
        print(f'{Service.EVENT} not found')


# }
