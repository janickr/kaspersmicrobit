# Kasper's microbit
[Nederlands](https://github.com/janickr/kaspersmicrobit/blob/main/README-nl.md)  
A python package to make a connection to a bbc microbit by means of the Bluetooth LE GATT services exposed by the microbit

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

More examples can be found in the [examples](https://github.com/janickr/kaspersmicrobit/tree/main/examples) directory.

# Problem solving
Problems related to connecting to the microbit over bluetooth are often solved by pairing your computer again to your 
microbit

See Also: https://support.microbit.org/helpdesk/attachments/19075694226