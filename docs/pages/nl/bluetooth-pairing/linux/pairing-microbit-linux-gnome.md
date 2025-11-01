---
title: Koppel een micro:bit in Linux
description: Gedetailleerde instructies voor het koppelen van uw micro:bit in Linux (gnome)
---

Na het volgen van onderstaande algemene koppelingsinstructies, ga naar de
[Kasper's microbit-overzichtspagina](../../index.md) en begin met het maken van je eerste game!

[![Video van games gemaakt met kaspersmicrobit](../../assets/images/kaspersmicrobit-youtube-small.gif)](../../index.md)

## Stap voor stap instructies

Eerst moet je je micro:bit in de "koppelmodus" zetten:

  - Houd de knoppen A, B en reset tegelijkertijd ingedrukt.
  - Laat de resetknop los, maar houd de knoppen A en B nog steeds ingedrukt.
  - Het LED-scherm wordt gevuld en je zou dan het Bluetooth-logo moeten zien, gevolgd door een koppelingspatroon.
  - Nu kan je de knoppen A en B loslaten

Je micro:bit bevindt zich in de koppelingsmodus en is detecteerbaar door Linux

Klik op het Bluetooth-pictogram in uw systeemstatusgebied.
Klik op "Bluetooth-instelling"

![klik op het Bluetooth-pictogram in de status balk](../../assets/images/bluetooth-pairing/linux/linux-bluetooth-system-status-area.png)

Het scherm "Bluetooth-instellingen" wordt geopend. Linux zal scannen naar Bluetooth-apparaten, je micro:bit zou in de lijst moeten verschijnen
Klik op het micro:bit-apparaat in de lijst, Linux zal koppelen met de micro:bit

![Bluetooth-instellingen - scannen](../../assets/images/bluetooth-pairing/linux/linux-bluetooth-settings-scanning.png)

Goed gedaan! Je micro:bit is gekoppeld in Linux!

## Het Bluetooth-adres zoeken

Als je niet de [eenvoudigere verbindingsmethoden](../../how-to-connect.md) gebruikt, maar in plaats daarvan wil
[verbinden met een micro:bit via het adres](../../how-to-connect.md#verbinden-met-een-microbit-via-het-adres), dan zijn dit
de instructies om het adres op te zoeken in gnome.

Wanneer de micro:bit is gekoppeld, klik dan nogmaals om de details van de micro:bit te bekijken

![Bluetooth-instellingen - gekoppeld](../../assets/images/bluetooth-pairing/linux/linux-bluetooth-settings-paired.png)

Er verschijnt een detailvenster. ***Schrijf het Bluetooth-adres van uw micro:bit op.***

![Bluetooth-instellingen - details](../../assets/images/bluetooth-pairing/linux/linux-bluetooth-settings-details.png)

## Maak je eerste spel

[Kasper's microbit](../../index.md) is een python pakket om verbinding te maken met een BBC micro:bit door middel van de actieve Bluetooth LE GATT-services
de micro:bit.

[![Video van games gemaakt met kaspersmicrobit](../../assets/images/kaspersmicrobit-youtube.gif)](../../index.md)