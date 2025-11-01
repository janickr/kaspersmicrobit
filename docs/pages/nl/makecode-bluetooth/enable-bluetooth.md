---
title: Schakel Bluetooth in op een micro:bit
description: Overzicht van hoe je Bluetooth op een microbit inschakelt en kiest tussen koppelen of niet koppelen
---

## Hoe de services inschakelen
Bluetooth moet eerst worden ingeschakeld op een micro:bit om er via Bluetooth verbinding mee te kunnen maken.

Dit kan gedaan worden [in MakeCode](create-a-makecode-project-without-pairing.md) of door een van onze
[vooraf gemaakte .hex](download-a-hex-file-without-pairing.md) bestanden naar de micro:bit te kopiëren. In MakeCode kun je zelf
kiezen welke services je activeert en combineert met je zelfgemaakt programma..

### De micro:bit v1
De micro:bit v1 heeft te weinig geheugen om alle Bluetooth-service in te schakelen. Als je ze allemaal probeert in te schakelen, en
het hex bestand naar de micro:bit kopieert, zal het LED-scherm een droevig gezicht laten zien en dan een voorbijrollende 020, 
dit betekent dat de micro:bit geen geheugen meer heeft.
Zie ook: [de micro:bit-foutcodes](https://makecode.microbit.org/device/error-codes)

## Koppelen

Een project [zonder koppeling ("No pairing required")](create-a-makecode-project-without-pairing.md#koppeling-uitschakelen) is het eenvoudigst om mee te werken:

- het werkt op [de meeste micro:bit-versies en besturingssystemen](../index.md#microbit-versies-operating-systems-bluetooth-pairing)
- er zijn geen extra stappen nodig om de micro:bit aan het besturingssysteem te koppelen
- het zorgt ervoor dat de microbit zijn naam bekendmaakt, zodat je hem [op naam kunt vinden](../reference/kaspersmicrobit.md#kaspersmicrobit.kaspersmicrobit.KaspersMicrobit.find_one_microbit)

Het nadeel is dat iedereen via Bluetooth verbinding kan maken met de micro:bit, omdat deze er niet aan gekoppeld hoeft te worden.