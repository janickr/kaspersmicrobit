---
title: Koppel een micro:bit in Windows
description: Gedetailleerde instructies voor het koppelen van uw micro:bit in Windows
---

Na het volgen van onderstaande algemene koppelingsinstructies, ga naar de
[Kasper's microbit-overzichtspagina](../../index.md) en begin met het maken van je eerste game!

[![Video van games gemaakt met kaspersmicrobit](../../assets/images/kaspersmicrobit-youtube-small.gif)](../../index.md)
  
## Stap voor stap instructies

Klik op het Bluetooth-pictogram in uw systeemvak.
Klik op 'Bluetooth-apparaten weergeven'

![klik op het Bluetooth-pictogram in het systeemvak](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-icon-system-tray.png)

Het scherm "Bluetooth en andere apparaten" wordt geopend, klik op "Bluetooth of ander apparaat toevoegen"

![Bluetooth- en andere apparaten scherm](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-devices-screen.png)

Het scherm 'Een apparaat toevoegen' verschijnt. Nu moet je je micro:bit in de "koppelmodus" zetten:

  - Houd de knoppen A, B en reset tegelijkertijd ingedrukt.
  - Laat de resetknop los, maar houd de knoppen A en B nog steeds ingedrukt.
  - Het LED-scherm wordt gevuld en je zou dan het Bluetooth-logo moeten zien, gevolgd door een koppelingspatroon.
  - Nu kan ja de knoppen A en B loslaten

Je micro:bit bevindt zich in de koppelingsmodus en is detecteerbaar door Windows

Klik nu op "Bluetooth"

![Een apparaat toevoegen](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-add-a-device.png)

Windows scant naar Bluetooth-apparaten, je micro:bit zou in de lijst moeten verschijnen

![Apparaten ontdekken](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-discover-devices.png)

Klik op het micro:bit-apparaat in de lijst. Windows zal koppelen met de micro:bit

![Koppelen met micro:bit](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-pair-with-with-microbit.png)

U kunt op "Gereed" klikken, uw micro:bit is gekoppeld in Windows!

## Het Bluetooth-adres zoeken
Als je niet de [eenvoudigere verbindingsmethoden](../../how-to-connect.md) gebruikt, maar in plaats daarvan wil
[verbinden met een micro:bit via het adres](../../how-to-connect.md#verbinden-met-een-microbit-via-het-adres), dan zijn dit
de instructies om het adres op te zoeken in Windows.
 
Terug op het scherm Bluetooth en andere apparaten selecteer je je micro:bit en klik je op "Meer Bluetooth-opties"

![Bluetooth en andere apparaten](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-devices-more-options.png)

Het Bluetooth-instellingenvenster verschijnt. Selecteer op het tabblad "Hardware" uw micro:bit en klik op "Eigenschappen"

![Bluetooth-instellingen](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-devices-hardware-tab.png)

Het micro:bit-eigenschappenvenster verschijnt. Selecteer op het tabblad "Details" de eigenschap "Associatie-eindpuntadres".
De waarde van deze eigenschap is het Bluetooth-adres van uw micro:bit. ***Schrijf dit adres ergens op*** je
hebt het nodig om verbinding te maken met je micro:bit.

![Micro:bit eigenschappen](../../assets/images/bluetooth-pairing/windows/windows-bluetooth-devices-hardware-address.png)

## Maak je eerste spel

[Kasper's microbit](../../index.md) is een python pakket om verbinding te maken met een BBC micro:bit door middel van de actieve Bluetooth LE GATT-services
de micro:bit.

[![Video van games gemaakt met kaspersmicrobit](../../assets/images/kaspersmicrobit-youtube.gif)](../../index.md)