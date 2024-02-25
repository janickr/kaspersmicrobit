---
title: Maak een MakeCode-project met Bluetooth zonder dat koppeling nodig is
description: Hoe maak je een micro:bit MakeCode-project, schakel je de Bluetooth-extensie in en schakel je het koppelen uit
---
# Uw eigen MakeCode-project (geen koppeling nodig)


Je kan zelf een [MakeCode](https://makecode.microbit.org)-project met Bluetooth maken.
Hieronder vind je de gedetailleerde instructies om een micro:bit MakeCode-project te maken, en de Bluetooth-extensie in te schakelen
zonder dat koppelen nodig is. Een project met [koppelen uitgeschakeld ("Geen koppeling vereist")](#disable-pairing) is het gemakkelijkst om mee te werken:

- het werkt op [de meeste micro:bit-versies en besturingssystemen] (../index.md#microbit-versions-operating-systems-bluetooth-pairing)
- er zijn geen extra stappen nodig om de micro:bit aan je besturingssysteem te koppelen
- het zorgt ervoor dat de microbit zijn naam bekendmaakt, zodat je hem [op naam kunt vinden](../reference/kaspersmicrobit.md#kaspersmicrobit.kaspersmicrobit.KaspersMicrobit.find_one_microbit)

Het nadeel is dat iedereen via Bluetooth verbinding kan maken met de micro:bit, omdat er geen koppeling nodig is.

## Maak een project
Selecteer in MakeCode voor micro:bit "Nieuw project"

![Start een nieuw project](../assets/images/makecode-bluetooth/makecode-new-project.png)
  
Voer een naam in:

![Project aanmaken: geef uw project een naam](../assets/images/makecode-bluetooth/makecode-create-project-give-name.png)


## Voeg de Bluetooth-extensie toe
Je moet de Bluetooth-extensie toevoegen.
Selecteer "Geavanceerd"

![MakeCode projectblokken: selecteer geavanceerd](../assets/images/makecode-bluetooth/makecode-project-blocks-select-advanced.png)

Selecteer "Extensies"

![MakeCode projectblokken: selecteer extensie](../assets/images/makecode-bluetooth/makecode-project-blocks-select-extensions.png)

Zoek naar Bluetooth en selecteer de Bluetooth-extensie

![Extensies: zoek en selecteer Bluetooth](../assets/images/makecode-bluetooth/makecode-project-extensions-select-bluetooth.png)

Er verschijnt een pop-up waarin staat dat de extensie "radio" wordt verwijderd als je Bluetooth toevoegt.
Selecteer "Verwijder extensie en voeg Bluetooth toe", dit geldt alleen voor dit project.

![Verwijder de radio-extensies en voeg Bluetooth toe](../assets/images/makecode-bluetooth/makecode-remove-radio-and-add-bluetooth.png)


## Koppeling uitschakelen

Klik rechtsboven op het tandwielpictogram en selecteer projectinstellingen. Schakel de optie "No pairing required: anyone can 
connect via Bluetooth" in. Sla de instellingen op.

![Selecteer Geen koppeling vereist in projectinstellingen](../assets/images/makecode-bluetooth/makecode-project-settings-microbit-no-pairing.png)


## Voeg Bluetooth-services toe

Nu kan je blokken selecteren op het Bluetooth-tabblad:

![Selecteer Bluetooth-blokken](../assets/images/makecode-bluetooth/makecode-project-blocks-select-bluetooth.png)

Sleep de services die je wil inschakelen in een 'Bij opstarten'-blok

![Sleep Bluetooth-services naar "Bij opstarten"](../assets/images/makecode-bluetooth/makecode-project-drag-services-in-onstart.png)

De micro:bit v1 heeft te weinig geheugen om alle Bluetooth-service in te schakelen. Als je ze allemaal probeert in te schakelen, en
het hex bestand naar de micro:bit kopieert, zal het LED-scherm een droevig gezicht laten zien en dan een voorbijrollende 020, 
dit betekent dat de micro:bit geen geheugen meer heeft.
Zie ook: [de micro:bit-foutcodes](https://makecode.microbit.org/device/error-codes)

## Download het hex-bestand

Download het hex-bestand en kopieer het naar uw micro:bit!