# Kasper's microbit

[![Documentation Status](https://readthedocs.org/projects/kaspersmicrobit/badge/?version=latest)](https://kaspersmicrobit.readthedocs.io/en/latest/?badge=latest) 
[![Documentation Status](https://img.shields.io/pypi/v/kaspersmicrobit)](https://img.shields.io/pypi/v/kaspersmicrobit)  

Een python package om een verbinding te kunnen maken met een bbc microbit met behulp van de Bluetooth LE GATT services 
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