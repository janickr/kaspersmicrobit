# Kasper's microbit

A package to connect to the Bluetooth LE GATT services of paired bbc micro:bit devices

Example:
```python

import time

from kaspersmicrobit import KaspersMicrobit

CHANGE_THIS_TO_YOUR_MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


def pressed(button):
    print(f"button {button} pressed")


with KaspersMicrobit(CHANGE_THIS_TO_YOUR_MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.buttons.on_button_a(press=pressed)
    time.sleep(10)

```