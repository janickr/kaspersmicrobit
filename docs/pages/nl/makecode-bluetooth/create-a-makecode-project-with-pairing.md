---
title: Maak een MakeCode-project met Bluetooth aan met JustWorks-pairing
description: Hoe maak je een micro:bit MakeCode-project, schakel je de Bluetooth-extensie in en activeer je JustWorks-pairing
---
# Je eigen MakeCode-project (met koppeling)

Je kan zelf een [MakeCode](https://makecode.microbit.org)-project met Bluetooth maken.
Hieronder vind je de gedetailleerde instructies om een micro:bit MakeCode-project te maken, en de Bluetooth-extensie in te schakelen
met JustWorks-koppeling. Een project met [koppeling ingeschakeld](#koppelen-inschakelen) zorgt ervoor dat alleen die
apparaten/computers die eraan zijn gekoppeld, ermee kunnen verbinden.

Het heeft echter ook een paar nadelen

- het werkt niet [voor een micro:bit v1.x op Windows](../index.md#microbit-versies-operating-systems-bluetooth-pairing)
- het heeft de extra stappen van het koppelen van de micro:bit met je [besturings-](../bluetooth-pairing/windows/pairing-microbit-windows.md)[systeem](../bluetooth-pairing/linux/pairing-microbit-linux-gnome.md) nodig
- Een gekoppelde micro:bit maakt zijn naam niet bekend, dus je kan hem niet op naam vinden



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


## Koppelen inschakelen

Klik rechtsboven op het tandwielpictogram en selecteer projectinstellingen. Activeer de optie "JustWorks pairing (default): 
Pairing is automatic once the pairing is initiated". Sla de instellingen op.

![Selecteer JustWorks-koppeling in projectinstellingen](../assets/images/makecode-bluetooth/makecode-project-settings-microbit-just-works-pairing.png)


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