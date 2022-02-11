# Kasper's microbit
[Nederlands](https://github.com/janickr/kaspersmicrobit/blob/main/README-nl.md)  

[![Documentation Status](https://readthedocs.org/projects/kaspersmicrobit/badge/?version=latest)](https://kaspersmicrobit.readthedocs.io/en/latest/?badge=latest) 
[![Documentation Status](https://img.shields.io/pypi/v/kaspersmicrobit)](https://img.shields.io/pypi/v/kaspersmicrobit)  

A python package to make a connection to a bbc microbit by means of the Bluetooth LE GATT services exposed by the microbit

## Installation
```bash
$ pip install kaspersmicrobit
```

## Example
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

More examples can be found in the [examples](https://github.com/janickr/kaspersmicrobit/tree/main/examples) directory.

## Api documentation
https://kaspersmicrobit.readthedocs.io

## Troubleshooting
Problems related to connecting to the microbit over bluetooth are often solved by pairing your computer again to your 
microbit

See also: https://support.microbit.org/helpdesk/attachments/19075694226