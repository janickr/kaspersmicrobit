---
title: Enable Bluetooth on a micro:bit
description: Overview on how to enable Bluetooth on a microbit and choose between pairing or no pairing
---

## How to enable the services
Bluetooth first needs to be enabled on a micro:bit to be able to connect to it using Bluetooth.  

This can be done [in MakeCode](create-a-makecode-project-without-pairing.md#disable-pairing) or by copying one of our 
[pre made .hex](download-a-hex-file-without-pairing.md) files to the micro:bit. In MakeCode you can choose which 
services to enable, and combine it with your own custom program.

### The micro:bit v1
The micro:bit v1 has too little memory to enable all bluetooth services. If you try to enable them all, after 
copying the hex the micro:bit, the LED display wil show a sad face and then scroll 020, this means the micro:bit is out of memory.
See also: [the micro:bit error codes](https://makecode.microbit.org/device/error-codes)

## Pairing

A project with [pairing disabled ("No pairing required")](create-a-makecode-project-without-pairing.md#disable-pairing) is the easiest to work with:

- it works on the [widest range of micro:bit versions and operating systems](../index.md#microbit-versions-operating-systems-bluetooth-pairing)
- it doesn't require the extra steps of pairing the micro:bit with your operating system
- it makes the microbit advertise its name, so you can [find it by name](../reference/kaspersmicrobit.md#kaspersmicrobit.kaspersmicrobit.KaspersMicrobit.find_one_microbit)

The disadvantage is that anyone can connect with the micro:bit over Bluetooth, because it is not needed to be paired to it.
