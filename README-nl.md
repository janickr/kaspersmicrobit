# Kasper's micro:bit
Heb je [Programmeren met Python](https://www.visualsteps.nl/programmerenpython/) uitgelezen? Zou het niet geweldig zijn
om je [BBC micro:bit](https://microbit.org/) als **wireless gamecontroller** te gebruiken voor je zelf gemaakte games? 
Dat kan je doen met dit python package! Pair je [micro:bit](https://microbit.org/) met bluetooth aan je computer en 
**gebruik de A en B knoppen of de accelerometer om je spel te besturen**. Like it? Geef ons een ster op github

[![Lint and Test](https://github.com/janickr/kaspersmicrobit/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/janickr/kaspersmicrobit/actions/workflows/lint_and_test.yml)
[![Documentation Status](https://readthedocs.org/projects/kaspersmicrobit/badge/?version=stable)](https://kaspersmicrobit.readthedocs.io/en/stable/?badge=stable) 
[![PyPi](https://img.shields.io/pypi/v/kaspersmicrobit)](https://pypi.org/project/kaspersmicrobit/) 
[![Nederlands](https://img.shields.io/badge/translation-English-blue)](https://github.com/janickr/kaspersmicrobit/blob/main/README.md)

Kasper's microbit is een python package om een verbinding te kunnen maken met een BBC micro:bit met behulp van de Bluetooth LE GATT services 
die de micro:bit aanbiedt.

[![Video of games created with kaspersmicrobit](https://kaspersmicrobit.readthedocs.io/en/latest/kaspersmicrobit-youtube.gif)](https://www.youtube.com/watch?v=t3JARVPQE9Q)
  
Bekijk de volledige video [op youtube](https://www.youtube.com/watch?v=t3JARVPQE9Q)

## Installatie
```bash
$ pip install kaspersmicrobit
```

Of upgrade naar de laatste versie met:
```bash
$  pip install --upgrade kaspersmicrobit  
```

## Een voorbeeld
```python

import time

from kaspersmicrobit import KaspersMicrobit

VERANDER_DIT_NAAR_JOUW_MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


def ingedrukt(knop):
    print(f"knop {knop} ingedrukt")


with KaspersMicrobit(VERANDER_DIT_NAAR_JOUW_MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.buttons.on_button_a(press=ingedrukt)
    time.sleep(10)

```

## Connecteren
Om met je micro:bit te kunnen verbinden moet je de [bluetooth services](https://kaspersmicrobit.readthedocs.io/en/stable/makecode-bluetooth/enable-bluetooth/) 
die je wil gebruiken op je micro:bit aanzetten, en je micro:bit [pairen](https://kaspersmicrobit.readthedocs.io/en/stable/bluetooth-pairing/windows/pairing-microbit-windows/) 
met je computer. 

Om de Bluetooth services aan te zetten kan je [MakeCode](https://makecode.microbit.org) gebruiken of 
[een hex bestand](https://kaspersmicrobit.readthedocs.io/en/stable/makecode-bluetooth/enable-bluetooth/)
naar je micro:bit kopi??ren.

Voor meer gedetailleerde instructies zie [Getting started - Enable Bluetooth](https://kaspersmicrobit.readthedocs.io/en/stable/makecode-bluetooth/enable-bluetooth/)

## Api documentatie
Op https://kaspersmicrobit.readthedocs.io, vind je het volgende:

 - Eenvoudige voorbeelden die tonen hoe je de functies van iedere service aangeboden door de micro:bit gebruikt
 - Volledige Api documentation
 - Voorbeelden van kaspersmicrobit in combinatie met tkinter 


De code van alle voorbeelden kan je vinden in de [examples](https://github.com/janickr/kaspersmicrobit/tree/main/examples) folder.

## Probleemoplossing

### Bluetooth connection
Problemen in verband met bluetooth connecties met de micro:bit kunnen vaak verholpen worden door je computer
opnieuw te pairen met je micro:bit.

Zie ook: https://support.microbit.org/helpdesk/attachments/19075694226

Kijk ook na: indien je de "with"-blok niet gebruikt, maar in de plaats daarvan zelf .connect() oproept, zorg er dan voor 
dat je in elk geval ook .disconnect() oproept wanneer je de connectie niet meer nodig hebt (bijvoorbeeld wanneer je 
programma eindigt)


### De micro:bit V1 en Microsoft Windows
Om kaspersmicrobit te gebruiken moet je micro:bit gepaired zijn met je computer, maar niet "verbonden". We hebben
gemerkt dat onze micro:bit V1 zich altijd verbindt met windows wanneer hij gepaired is. Dit zorgt ervoor dat
kaspersmicrobit er niet mee kan verbinden. Onder linux gedraagt de V1 zich wel correct. De micro:bit V2 
werkt wel correct op zowel Windows als linux.

### tkinter "main thread is not in main loop"
Wanneer je kaspersmicrobit combineert met tkinter (de window module die gebruikt wordt in [Programmeren met Python](https://www.visualsteps.nl/programmerenpython/))
kan je de TK fout "main thread is not in main loop" tegenkomen. Dit is waarschijnlijk omdat je TK code oproept vanuit
een callback functie die je meegegeven hebt om omgeroepen te worden wanneer een druk op de knop gebeurt of wanneer
er nieuwe accelerometer gegevens zijn (of iets anders). Deze callback wordt uitgevoerd op een andere thread en tkinter
wil dit niet. Hier zijn minstens 2 oplossingen voor:  

  - roep geen tkinter code op in een callback
  - omsluit de callback met `kaspersmicrobit.tkinter.do_in_tkinter(tk, jouw_callback)` dit zorgt ervoor dat je callback
    uitgevoerd zal worden op de tk thread, dit vermijdt het probleem
