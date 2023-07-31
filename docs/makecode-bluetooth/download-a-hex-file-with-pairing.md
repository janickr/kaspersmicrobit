---
title: Hex files that enable Bluetooth services on your micro:bit with pairing
description: Hex files with Bluetooth services enabled with JustWorks pairing for various versions of the micro:bit
---
# Download hex files (JustWorks pairing)
To use a .hex file from this page you need to download it and copy it to the micro:bit.
Before you can connect to the micro:bit using these files, you need to pair it with your computer
([windows](../bluetooth-pairing/windows/pairing-microbit-windows.md), [linux](../bluetooth-pairing/linux/pairing-microbit-linux-gnome.md))

The micro:bit v1 has too little memory to enable all bluetooth services. If you try to enable them all, after 
copying the hex the micro:bit, the LED display wil show a sad face and then scroll 020, this means the micro:bit is out of memory.
See also: [the micro:bit error codes](https://makecode.microbit.org/device/error-codes)

### The micro:bit v2

#### all services except event service
The file: [all services without eventservice](../hex/microbit-v2-bluetooth-all-services-witout-events-pairing.hex)  
Source: [this makecode project](https://makecode.microbit.org/_CasTvmavX3dH).

Enabled services: [accelerometer](../accelerometer.md) - [buttons](../buttons.md) - [led](../led.md) - [temperature](../temperature.md) - [io-pin](../io_pin.md) - [magnetometer](../magnetometer.md) - [uart](../uart.md)
 
The hex files for the micro:bit v1 can also be used on the micro:bit v2

#### uart and event service
The file: [uart and event service](../hex/microbit-bluetooth-uart-pairing.hex)  
Source: [this makecode project](https://makecode.microbit.org/_YHz6WqMqKA7E).

Enabled services: [uart](../uart.md) - [event service](../events_v2.md)

### The micro:bit v1
Because of the smaller memory on the micro:bit v1, only subsets of all Bluetooth services can be enabled at the same time.
We provide a few here, but you could also create your own hex file with [MakeCode](create-a-makecode-project-with-pairing.md)

#### accelerometer + buttons + led + temperature
The file: [no magnetometer, no uart, no io](../hex/microbit-bluetooth-accel-buttons-led-temp-pairing.hex)  
Source: [this makecode project](https://makecode.microbit.org/_e3uVF0frHM20).

Enabled services: [accelerometer](../accelerometer.md) - [buttons](../buttons.md) - [led](../led.md) - [temperature](../temperature.md)

#### uart and event service
The file: [uart and event service](../hex/microbit-bluetooth-uart-pairing.hex)  
Source: [this makecode project](https://makecode.microbit.org/_YHz6WqMqKA7E).

Enabled services: [uart](../uart.md) - [event service](../events_v1.md)

#### magnetometer only
The file: [magnetometer only](../hex/microbit-bluetooth-magnetometer-pairing.hex)  
Source: [this makecode project](https://makecode.microbit.org/_0DCYLc3MVFMf).

Enabled services: [magnetometer](../magnetometer.md)
