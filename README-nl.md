# Kasper's microbit
Heb je [Programmeren met Python](https://www.visualsteps.nl/programmerenpython/) uitgelezen? Zou het niet geweldig zijn
om je [bbc micro:bit](https://microbit.org/) als **wireless gamecontroller** te gebruiken voor je zelf gemaakte games? 
Dat kan je doen met dit python package! Pair je [micro:bit](https://microbit.org/) met bluetooth aan je computer en 
**gebruik de A en B knoppen of de accelerometer om je spel te besturen**.


[![Documentation Status](https://readthedocs.org/projects/kaspersmicrobit/badge/?version=latest)](https://kaspersmicrobit.readthedocs.io/en/latest/?badge=latest) 
[![PyPi](https://img.shields.io/pypi/v/kaspersmicrobit)](https://pypi.org/project/kaspersmicrobit/) 
[![Nederlands](https://img.shields.io/badge/translation-English-blue)](https://github.com/janickr/kaspersmicrobit/blob/main/README.md)

Kasper's microbit is een python package om een verbinding te kunnen maken met een bbc microbit met behulp van de Bluetooth LE GATT services 
die de microbit aanbiedt.

## Installatie
```bash
$ pip install kaspersmicrobit
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

Je kan meer voorbeelden vinden in de [examples](https://github.com/janickr/kaspersmicrobit/tree/main/examples)  folder.

## Api documentatie
https://kaspersmicrobit.readthedocs.io

## Probleemoplossing
Problemen in verband met bluetooth connecties met de microbit kunnen vaak verholpen worden door je computer
opnieuw te pairen met je microbit.

Zie ook: https://support.microbit.org/helpdesk/attachments/19075694226