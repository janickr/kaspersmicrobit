---
title: Verschillende manieren om een micro:bit the vinden en ermee te verbinden
description: Leer hoe de je een micro:bit via Bluetooth kan vinden en ermee te verbinden via python (aan de hand van een voorbeeld)
---

De API documentatie: 

- [kaspersmicrobit](reference/kaspersmicrobit.md)

## Verbinden met de eerst gevonden micro:bit

<!--codeinclude-->
[](../../../examples/find-microbits.py) inside_block:example-first
<!--/codeinclude-->

## Verbinden met een micro:bit via de naam
Kijk hier als je de naam van je micro:bit niet kent:  

- [How to find the name of your micro:bit](https://support.microbit.org/support/solutions/articles/19000067679-how-to-find-the-name-of-your-micro-bit)

<!--codeinclude-->
[](../../../examples/find-microbits.py) inside_block:example-name
<!--/codeinclude-->

## Verbinden met een micro:bit via het adres
Het Bluetooth adres van je micro:bit vinden:

 - [In Windows](./bluetooth-pairing/windows/pairing-microbit-windows.md#het-bluetooth-adres-zoeken)
 - [In Linux (Gnome)](./bluetooth-pairing/linux/pairing-microbit-linux-gnome.md#het-bluetooth-adres-zoeken)


<!--codeinclude-->
[](../../../examples/find-microbits.py) inside_block:example-address
<!--/codeinclude-->

## Verbinden met meerdere micro:bits

<!--codeinclude-->
[](../../../examples/find-microbits.py) inside_block:example-multiple
<!--/codeinclude-->
