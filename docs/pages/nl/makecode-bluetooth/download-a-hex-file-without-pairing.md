---
title: Hex-bestanden die Bluetooth-services op uw micro:bit inschakelen zonder te koppelen
description: Hex-bestanden met Bluetooth-services ingeschakeld zonder koppeling, voor verschillende versies van de micro:bit
---
# Hex-bestanden downloaden (geen koppeling nodig)
Om een .hex-bestand van deze pagina te gebruiken, moet je het downloaden en naar de micro:bit kopiëren

De micro:bit v1 heeft te weinig geheugen om alle Bluetooth-service in te schakelen. Als je ze allemaal probeert in te schakelen, en
het hex bestand naar de micro:bit kopieert, zal het LED-scherm een droevig gezicht laten zien en dan een voorbijrollende 020, 
dit betekent dat de micro:bit geen geheugen meer heeft.
Zie ook: [de micro:bit-foutcodes](https://makecode.microbit.org/device/error-codes)

### De micro:bit v2

#### alle services behalve event service
Het bestand: [alle services zonder event service](../assets/hex/microbit-v2-bluetooth-all-services-without-events-no-pairing.hex)
Bron: [dit makecode-project](https://makecode.microbit.org/_UcFDqJap5Ptz).

Ingeschakelde services: [accelerometer](../accelerometer.md) - [knoppen](../buttons.md) - [led](../led.md) - [temperatuur](../temperature.md) - [io-pin](../io_pin.md) - [magnetometer](../magnetometer.md) - [uart](../uart.md)
 
De hex-bestanden voor de micro:bit v1 kunnen ook worden gebruikt op de micro:bit v2

#### uart en event service
Het bestand: [uart en event service](../assets/hex/microbit-bluetooth-uart-no-pairing.hex)
Bron: [dit makecode-project](https://makecode.microbit.org/_Rhe5vuaVr1FX).

Ingeschakelde services: [uart](../uart.md) - [gebeurtenisservice](../events_v2.md)

### De micro:bit v1
Door het kleinere geheugen op de micro:bit v1 kan maar een deel van alle Bluetooth-services tegelijkertijd worden ingeschakeld.
We bieden er hier een aantal aan, maar je kunt ook je eigen hex-bestand maken met [MakeCode](create-a-makecode-project-with-pairing.md)

#### versnellingsmeter + knoppen + led + temperatuur
Het bestand: [geen magnetometer, geen uart, geen io](../assets/hex/microbit-bluetooth-accel-buttons-led-temp-no-pairing.hex)
Bron: [dit makecode-project](https://makecode.microbit.org/_aRg2pr3V9LVx).

Ingeschakelde services: [accelerometer](../accelerometer.md) - [knoppen](../buttons.md) - [led](../led.md) - [temperatuur](../temperature.md)

#### uart en event service
Het bestand: [uart en event service](../assets/hex/microbit-bluetooth-uart-no-pairing.hex)
Bron: [dit makecode-project](https://makecode.microbit.org/_Rhe5vuaVr1FX).

Ingeschakelde services: [uart](../uart.md) - [event service](../events_v1.md)

#### Alleen magnetometer
Het bestand: [alleen magnetometer](../assets/hex/microbit-bluetooth-magnetometer-no-pairing.hex)
Bron: [dit makecode-project](https://makecode.microbit.org/_8X6DJwMDADeH).

Ingeschakelde services: [magnetometer](../magnetometer.md)