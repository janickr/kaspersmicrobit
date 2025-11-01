---
title: Different ways to find and connect to a micro:bit
description: Learn how to find and connect to the bluetooth services of a micro:bit from python (by example)
---

The API documentation: 

- [kaspersmicrobit](reference/kaspersmicrobit.md)

## Connect to the first micro:bit found

<!--codeinclude-->
[](../../../examples/find-microbits.py) inside_block:example-first
<!--/codeinclude-->

## Find a micro:bit by name
Look here if you don't know the name of your micro:bit:  

- [How to find the name of your micro:bit](https://support.microbit.org/support/solutions/articles/19000067679-how-to-find-the-name-of-your-micro-bit)

<!--codeinclude-->
[](../../../examples/find-microbits.py) inside_block:example-name
<!--/codeinclude-->

## Connect to a micro:bit by address
Find the Bluetooth address of your micro:bit:

 - [On Windows](./bluetooth-pairing/windows/pairing-microbit-windows.md#finding-the-bluetooth-address)
 - [On Linux (Gnome)](./bluetooth-pairing/linux/pairing-microbit-linux-gnome.md#finding-the-bluetooth-address)

<!--codeinclude-->
[](../../../examples/find-microbits.py) inside_block:example-address
<!--/codeinclude-->

## Connect to multiple micro:bits

<!--codeinclude-->
[](../../../examples/find-microbits.py) inside_block:example-multiple
<!--/codeinclude-->
