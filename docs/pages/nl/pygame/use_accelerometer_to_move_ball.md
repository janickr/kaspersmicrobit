---
title: Beweeg een bal in pygame met de accelerometer van de micro:bit
description: Teken een bal met pygame in Python en verplaats deze door een micro:bit te kantelen
---

In dit voorbeeld wordt de callback `accelerometer_data` geregistreerd voor de accelerometergegevens met
`microbit.accelerometer.notify`

Dit gebeurt wanneer de micro:bit nieuwe accelerometergegevens aanbiedt:

 - de `accelerometer_data` callback wordt aangeroepen met de nieuwe gegevens als argument
 - de callback registreert de gegevens als de player_direction
 - de lus `while running:` werkt de spelerspositie bij en tekent de bal opnieuw


Zie ook de API-documentatie:

- [kaspersmicrobit.services.accelerometer](../reference/services/accelerometer.md)
- [kaspersmicrobit](../reference/kaspersmicrobit.md)


<!--codeinclude-->
[](../../../../examples/pygame/pygame-use-accelerometer-to-move-ball.py) inside_block:example
<!--/codeinclude-->