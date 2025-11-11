# Kasper's micro:bit
So you finished [Python for kids](https://nostarch.com/pythonforkids)? Wouldn't it be awesome to use your
[BBC micro:bit](https://microbit.org/) as a **wireless game controller** for your own DIY games? You can do it with 
this python package! Pair your [micro:bit](https://microbit.org/) to your computer with bluetooth and **use buttons A 
and B or the accelerometer to control your game**. Like it? Give us a :star: on github!

[![Lint and Test](https://github.com/janickr/kaspersmicrobit/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/janickr/kaspersmicrobit/actions/workflows/lint_and_test.yml)
[![Documentation Status](https://readthedocs.org/projects/kaspersmicrobit/badge/?version=stable)](https://kaspersmicrobit.readthedocs.io/en/stable/?badge=stable) 
[![PyPi](https://img.shields.io/pypi/v/kaspersmicrobit)](https://pypi.org/project/kaspersmicrobit/)
[![Nederlands](https://img.shields.io/badge/vertaling-Nederlands-blue)](https://kaspersmicrobit.readthedocs.io/nl/stable/)

Kasper's microbit is a python package to make a connection to a BBC micro:bit by means of the Bluetooth LE GATT services
exposed by the micro:bit.

[![Video of games created with kaspersmicrobit](https://kaspersmicrobit.readthedocs.io/en/latest/assets/images/kaspersmicrobit-youtube.gif)](https://www.youtube.com/watch?v=t3JARVPQE9Q)

Watch the full video [on youtube](https://www.youtube.com/watch?v=t3JARVPQE9Q)

## Getting started
Install kaspersmicrobit:
```bash
$ pip install kaspersmicrobit
```
Copy [this hex file](https://kaspersmicrobit.readthedocs.io/en/latest/assets/hex/microbit-bluetooth-accel-buttons-led-temp-no-pairing.hex) 
to the micro:bit and run your first program:
```python
import time

from kaspersmicrobit import KaspersMicrobit


def pressed(button):
    print(f"button {button} pressed")

with KaspersMicrobit.find_one_microbit() as microbit:
    microbit.buttons.on_button_a(press=pressed)
    time.sleep(10)
```

## Learn more
Visit https://kaspersmicrobit.readthedocs.io:

 - Try the [accelerometer](https://kaspersmicrobit.readthedocs.io/en/stable/accelerometer/), or the [led display](https://kaspersmicrobit.readthedocs.io/en/stable/led/)
 - [Learn](https://kaspersmicrobit.readthedocs.io/en/stable/makecode-bluetooth/create-a-makecode-project-without-pairing/) to make your own .hex files
 - [Simple examples](https://kaspersmicrobit.readthedocs.io/en/stable/buttons/), learn how to use each service offered by the micro:bit 
 - [Full Api documentation](https://kaspersmicrobit.readthedocs.io/en/stable/reference/kaspersmicrobit/)
 - Combining KaspersMicrobit [with tkinter](https://kaspersmicrobit.readthedocs.io/en/stable/tkinter/use_buttons_to_move_rectangle/) 
   or [with pygame](https://kaspersmicrobit.readthedocs.io/en/stable/pygame/use_buttons_to_move_rectangle/)

Or take a look at the [examples](https://github.com/janickr/kaspersmicrobit/tree/main/examples) directory.

## Micro:bit versions, operating systems, Bluetooth pairing

Below you can find which combinations of operating systems and microbit versions have been known to work.


| micro:bit v2.x | No pairing required | Just works pairing |
|----------------|---------------------|--------------------|
| Windows        | :heavy_check_mark:  | :heavy_check_mark: |
| Linux          | :heavy_check_mark:  | :heavy_check_mark: |
| MacOS          | :heavy_check_mark:  | :x:                |

| micro:bit v1.x | No pairing required  | Just works pairing |
|----------------|----------------------|--------------------|
| Windows        | :heavy_check_mark:   | :x:                |
| Linux          | :heavy_check_mark:   | :heavy_check_mark: |
| MacOS          | :heavy_check_mark: * | :x:                |

\* Magnetometer calibration of micro:bit v1 on MacOS fails with the micro:bit not responding or going out of memory (error 020 + sad face)

## Troubleshooting
### Upgrade to the latest version
```bash
$  pip install --upgrade kaspersmicrobit  
```
### Bluetooth connection
First try turning the micro:bit off and on again.

If you are not using the "with"-block, but calling `.connect()` yourself, always make sure that in any case you 
call `.disconnect()` when you don't need the connection anymore (for instance when you exit your application)

#### No pairing required
If the hex file was created with the setting ["No pairing required"](https://kaspersmicrobit.readthedocs.io/en/stable/makecode-bluetooth/create-a-makecode-project-without-pairing/#disable-pairing)
then the micro:bit should not be paired with the operating system

#### Just works pairing 
Don't use pairing with a micro:bit v1 on windows, use  ["No pairing required"](https://kaspersmicrobit.readthedocs.io/en/stable/makecode-bluetooth/create-a-makecode-project-without-pairing/#disable-pairing)
 instead.  

For other versions: try to remove the micro:bit from the paired Bluetooth devices and pairing it your computer again.

See also: [The micro:bit Bluetooth troubleshooting guide](https://support.microbit.org/helpdesk/attachments/19075694226) (.docx word file download)

### What is the name of my micro:bit?
See: [How to find the name of your micro:bit](https://support.microbit.org/support/solutions/articles/19000067679-how-to-find-the-name-of-your-micro-bit)

### The micro:bit shows a sad face and error 020
This means the micro:bit is out of memory. You probably have enabled too many Bluetooth services in MakeCode. Or maybe
your MakeCode program is too large. Because the micro:bit v1 has less memory than the v2, this has a higher chance to
occur on v1 micro:bits.  
See also: [the micro:bit error codes](https://makecode.microbit.org/device/error-codes)

### tkinter "main thread is not in main loop"
When combining kaspersmicrobit with tkinter (the window library used in [Python for kids](https://nostarch.com/pythonforkids))
you could bump into the TK error "main thread is not in main loop". This is probably because you call TK code from 
within a callback function that you registered to be called when a button press occurs or new accelerometer data is 
present (or some other notification). The callback is executed on a different thread and tkinter does not like this. 
There are at least 2 solutions for this:

 - don't call tkinter code in a callback
 - wrap the callback with `kaspersmicrobit.tkinter.do_in_tkinter(tk, your_callback)` this makes sure that your callback 
   will be executed on the tk thread, avoiding the error
