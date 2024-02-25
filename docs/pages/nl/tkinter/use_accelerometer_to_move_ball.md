---
title: Verplaats een bal in tkinter met de accelerometer van de micro:bit
description: Teken een bal op een tkinter-canvas in Python en verplaats deze door een micro:bit te kantelen
---

In dit voorbeeld wordt de callback `accelerometer_data` geregistreerd voor de accelerometergegevens met
`microbit.accelerometer.notify`

Dit gebeurt wanneer de micro:bit nieuwe accelerometergegevens aanbiedt:

 - de `accelerometer_data` callback wordt aangeroepen met de nieuwe gegevens als argument
 - de callback registreert de gegevens als de balrichting
- `tk.main_loop()` roept `redraw` aan, waardoor de bal op het canvas beweegt in de richting die eerder is ingesteld door de callback


Zie ook de API-documentatie:

- [kaspersmicrobit.services.accelerometer](../reference/services/accelerometer.md)
- [kaspersmicrobit](../reference/kaspersmicrobit.md)


<!--codeinclude-->
[](../../../../examples/tkinter/tk-use-accelerometer-to-move-ball.py) inside_block:example
<!--/codeinclude-->