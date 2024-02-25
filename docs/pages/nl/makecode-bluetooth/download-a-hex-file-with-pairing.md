---
title: Hex-bestanden die Bluetooth-services op je micro:bit inschakelen met koppeling
description: Hex-bestanden met Bluetooth-services ingeschakeld met JustWorks-koppeling, voor verschillende versies van de micro:bit
---
# Hex-bestanden downloaden (JustWorks-koppeling)
Om een .hex-bestand van deze pagina te gebruiken, moet je het downloaden en naar de micro:bit kopiëren.
Voordat je met behulp van deze bestanden verbinding kunt maken met de micro:bit, moet je deze aan je computer koppelen
([windows](../bluetooth-pairing/windows/pairing-microbit-windows.md), [linux](../bluetooth-pairing/linux/pairing-microbit-linux-gnome.md))

De micro:bit v1 heeft te weinig geheugen om alle Bluetooth-service in te schakelen. Als je ze allemaal probeert in te schakelen, en
het hex bestand naar de micro:bit kopieert, zal het LED-scherm een droevig gezicht laten zien en dan een voorbijrollende 020, 
dit betekent dat de micro:bit geen geheugen meer heeft.
Zie ook: [de micro:bit-foutcodes](https://makecode.microbit.org/device/error-codes)

### De micro:bit v2

#### alle services behalve de event service
Het bestand: [alle services zonder eventservice](../assets/hex/microbit-v2-bluetooth-all-services-without-events-pairing.hex)
Bron: [dit makecode-project](https://makecode.microbit.org/_CasTvmavX3dH).

Ingeschakelde services: [accelerometer](../accelerometer.md) - [knoppen](../buttons.md) - [led](../led.md) - [temperatuur](../temperature.md) - [io-pin](../io_pin.md) - [magnetometer](../magnetometer.md) - [uart](../uart.md)
 
De hex-bestanden voor de micro:bit v1 kunnen ook worden gebruikt op de micro:bit v2

#### uart en event service
Het bestand: [uart en event service](../assets/hex/microbit-bluetooth-uart-pairing.hex)
Bron: [dit makecode-project](https://makecode.microbit.org/_YHz6WqMqKA7E).

Ingeschakelde services: [uart](../uart.md) - [event service](../events_v2.md)

### De micro:bit v1
Door het kleinere geheugen op de micro:bit v1 kan maar een deel van alle Bluetooth-services tegelijkertijd worden ingeschakeld.
We bieden er hier een aantal aan, maar je kunt ook je eigen hex-bestand maken met [MakeCode](create-a-makecode-project-with-pairing.md)

#### accelerometer + knoppen + led + temperatuur
Het bestand: [geen magnetometer, geen uart, geen io](../assets/hex/microbit-bluetooth-accel-buttons-led-temp-pairing.hex)
Bron: [dit makecode-project](https://makecode.microbit.org/_e3uVF0frHM20).

Ingeschakelde services: [accelerometer](../accelerometer.md) - [knoppen](../buttons.md) - [led](../led.md) - [temperatuur](../temperature.md)

#### uart en eventservice
Het bestand: [uart en event service](../assets/hex/microbit-bluetooth-uart-pairing.hex)
Bron: [dit makecode-project](https://makecode.microbit.org/_YHz6WqMqKA7E).

Ingeschakelde services: [uart](../uart.md) - [event service](../events_v1.md)

#### Alleen magnetometer
Het bestand: [alleen magnetometer](../assets/hex/microbit-bluetooth-magnetometer-pairing.hex)
Bron: [dit makecode-project](https://makecode.microbit.org/_0DCYLc3MVFMf).

Ingeschakelde services: [magnetometer](../magnetometer.md)