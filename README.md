# Kasper's microbit
So you finished [Python for kids](https://nostarch.com/pythonforkids)? Wouldn't it be awesome to use your
[bbc micro:bit](https://microbit.org/) as a **wireless game controller** for your own DIY games? You can do this with 
this python package! Pair your [micro:bit](https://microbit.org/) to your computer with bluetooth and **use buttons A 
and B or the accelerometer to control your game**. Like it? Give us a :star: on github!

[![Lint and Test](https://github.com/janickr/kaspersmicrobit/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/janickr/kaspersmicrobit/actions/workflows/lint_and_test.yml)
[![Documentation Status](https://readthedocs.org/projects/kaspersmicrobit/badge/?version=latest)](https://kaspersmicrobit.readthedocs.io/en/latest/?badge=latest) 
[![PyPi](https://img.shields.io/pypi/v/kaspersmicrobit)](https://pypi.org/project/kaspersmicrobit/)
[![Nederlands](https://img.shields.io/badge/vertaling-Nederlands-blue)](https://github.com/janickr/kaspersmicrobit/blob/main/README-nl.md)

Kasper's microbit is a python package to make a connection to a bbc microbit by means of the Bluetooth LE GATT services
exposed by the microbit.

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

## Connecting
To connect to your microbit you'll have to enable the [bluetooth services](https://kaspersmicrobit.readthedocs.io/en/stable/makecode-bluetooth/enable-bluetooth/) 
you want to use, and [pair](https://kaspersmicrobit.readthedocs.io/en/stable/bluetooth-pairing/windows/pairing-microbit-windows/) your microbit 
to your computer.  

To enable the services you can use [MakeCode](https://makecode.microbit.org) or copy
[a hex file](https://kaspersmicrobit.readthedocs.io/en/stable/makecode-bluetooth/enable-bluetooth/)
to your microbit.

For detailed instructions take a look in [Getting started - Enable Bluetooth](https://kaspersmicrobit.readthedocs.io/en/stable/makecode-bluetooth/enable-bluetooth/)

## Documentation
On https://kaspersmicrobit.readthedocs.io you can find:

 - Simple examples, showing how to use the functions of each service offered by the microbit 
 - Full Api documentation
 - Examples that show kaspersmicrobit in combination with tkinter 


The source code of all examples from the documentation can be found in the [examples](https://github.com/janickr/kaspersmicrobit/tree/main/examples) directory.


## Troubleshooting

### Bluetooth connection
Problems related to connecting to the microbit over bluetooth are often solved by pairing your computer again to your 
microbit

See also: https://support.microbit.org/helpdesk/attachments/19075694226

Also, if you are not using the "with"-block, but calling .connect() yourself, always make sure that in any case you 
call .disconnect() when you don't need the connection anymore (for instance when you exit your application)

### Microbit V1 and Microsoft Windows
To use kaspersmicrobit, your microbit should be paired with your computer, but not "connected". We noticed that 
our microbit V1 always connects to Windows when it is paired. This prevents kaspersmicrobit to connect to it. On linux 
it behaves correctly. The microbit V2 worked on both Windows and linux.

### tkinter "main thread is not in main loop"
When combining kaspersmicrobit with tkinter (the window library used in [Python for kids](https://nostarch.com/pythonforkids))
you could bump into the TK error "main thread is not in main loop". This is probably because you call TK code from 
within a callback function that you registered to be called when a button press occurs or new accelerometer data is 
present (or some other notification). The callback is executed on a different thread and tkinter does not like this. 
There are at least 2 solutions for this:

 - don't call tkinter code in a callback
 - wrap the callback with `kaspersmicrobit.tkinter.do_in_tkinter(tk, your_callback)` this makes sure that your callback 
   will be executed on the tk thread, avoiding the error
