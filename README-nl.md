# Kasper's micro:bit
Heb je [Programmeren met Python](https://www.visualsteps.nl/programmerenpython/) uitgelezen? Zou het niet geweldig zijn
om je [BBC micro:bit](https://microbit.org/) als **wireless gamecontroller** te gebruiken voor je zelf gemaakte games? 
Dat kan je doen met dit python package! Pair je [micro:bit](https://microbit.org/) met bluetooth aan je computer en 
**gebruik de A en B knoppen of de accelerometer om je spel te besturen**. Like it? Geef ons een ster op github

[![Lint and Test](https://github.com/janickr/kaspersmicrobit/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/janickr/kaspersmicrobit/actions/workflows/lint_and_test.yml)
[![Documentation Status](https://readthedocs.org/projects/kaspersmicrobit/badge/?version=stable)](https://kaspersmicrobit.readthedocs.io/nl/stable/?badge=stable) 
[![PyPi](https://img.shields.io/pypi/v/kaspersmicrobit)](https://pypi.org/project/kaspersmicrobit/) 
[![Nederlands](https://img.shields.io/badge/translation-English-blue)](https://github.com/janickr/kaspersmicrobit/blob/main/README.md)

Kasper's microbit is een python package om een verbinding te kunnen maken met een BBC micro:bit met behulp van de Bluetooth LE GATT services 
die de micro:bit aanbiedt.

[![Video of games created with kaspersmicrobit](https://kaspersmicrobit.readthedocs.io/en/latest/kaspersmicrobit-youtube.gif)](https://www.youtube.com/watch?v=t3JARVPQE9Q)
  
Bekijk de volledige video [op youtube](https://www.youtube.com/watch?v=t3JARVPQE9Q)

## Hoe te starten
Installeer kaspersmicrobit:
```bash
$ pip install kaspersmicrobit
```
Kopieer [dit hex bestand](https://kaspersmicrobit.readthedocs.io/nl/latest/hex/microbit-bluetooth-accel-buttons-led-temp-no-pairing.hex)
naar de micro:bit en start je eerste programma:
```python
import time

from kaspersmicrobit import KaspersMicrobit


def pressed(button):
    print(f"button {button} pressed")

with KaspersMicrobit.find_one_microbit() as microbit:
    microbit.buttons.on_button_a(press=pressed)
    time.sleep(10)
```

## Leer meer
Bezoek https://kaspersmicrobit.readthedocs.io:

 - Probeer de [accelerometer](https://kaspersmicrobit.readthedocs.io/nl/stable/accelerometer/), of de [led display](https://kaspersmicrobit.readthedocs.io/nl/stable/led/)
 - [Leer](https://kaspersmicrobit.readthedocs.io/nl/stable/makecode-bluetooth/create-a-makecode-project-without-pairing/) je eigen .hex bestanden te maken
 - [Eenvoudige voorbeelden](https://kaspersmicrobit.readthedocs.io/nl/stable/buttons/), leer hoe je iedere Bluetooth service van de micro:bit kan gebruiken 
 - [Volledige Api documentatie](https://kaspersmicrobit.readthedocs.io/nl/stable/reference/kaspersmicrobit/)
 - Combineer KaspersMicrobit [met tkinter](https://kaspersmicrobit.readthedocs.io/nl/stable/tkinter/use_buttons_to_move_rectangle/)
   of [met pygame](https://kaspersmicrobit.readthedocs.io/nl/stable/pygame/use_buttons_to_move_rectangle/)


Of neem een kijkje in de [voorbeelden](https://github.com/janickr/kaspersmicrobit/tree/main/examples).

## Micro:bit versies, operating systems, Bluetooth pairing

In de onderstaande tabellen zie je welke combinatie van besturingssystemen en micro:bit versies werken.

| micro:bit v2.x | No pairing required | Just works pairing |
|----------------|---------------------|--------------------|
| Windows        | :heavy_check_mark:  | :heavy_check_mark: |
| Linux          | :heavy_check_mark:  | :heavy_check_mark: |
| MacOS          | :heavy_check_mark:  | :grey_question:    |


Ik heb geen mac om kaspersmicrobit op te testen. Laat me [hier (#5)](https://github.com/janickr/kaspersmicrobit/issues/5) weten 
of het werkt of niet!
Bedankt [@RyanNorge](https://github.com/RyanNorge) om een micro:bit v2.x op MacOS in "No pairing required" mode te testen.


| micro:bit v1.x | No pairing required | Just works pairing |
|----------------|---------------------|--------------------|
| Windows        | :heavy_check_mark:  | :x:                |
| Linux          | :heavy_check_mark:  | :heavy_check_mark: |
| MacOS          | :grey_question:     | :grey_question:    |


## Troubleshooting
### Upgrade naar de laatste versie
```bash
$  pip install --upgrade kaspersmicrobit  
```
### Bluetooth connectie
Schakel je micro:bit eerst een keer uit en aan.

Kijk ook na: indien je de "with"-blok niet gebruikt, maar in de plaats daarvan zelf .connect() oproept, zorg er dan voor 
dat je in elk geval ook .disconnect() oproept wanneer je de connectie niet meer nodig hebt (bijvoorbeeld wanneer je 
programma eindigt)

#### No pairing required
Als het .hex bestand gemaakt werd met de instelling ["No pairing required"](https://kaspersmicrobit.readthedocs.io/nl/stable/makecode-bluetooth/create-a-makecode-project-without-pairing/#disable-pairing)
dan mag de micro:bit niet gepaired zijn met je besturingssysteem

#### Just works pairing 
Gebruik geen pairing bij een micro:bit v1 en windows, gebruik  ["No pairing required"](https://kaspersmicrobit.readthedocs.io/nl/stable/makecode-bluetooth/create-a-makecode-project-without-pairing/#disable-pairing)
in de plaats.  

Voor andere versies: verwijder de micro:bit van de lijst met gepairde Bluetooth toestellen en pair het opnieuw met je computer.

Zie ook: https://support.microbit.org/helpdesk/attachments/19075694226

### De micro:bit toont een droevige smiley en fout 020
Dit betekent dat de micro:bit een tekort aan geheugen heeft. Je hebt waarschijnlijk te veel Bluetooth services geactiveerd
in MakeCode. Of misschien is je MakeCode programma te groot. Omdat de micro:bit v1 minder geheugen heeft dan de v2, is 
de kans groter dat deze fout zich voordoet bij v1 micro:bits.
Zie ook: [the micro:bit error codes](https://makecode.microbit.org/device/error-codes)

### tkinter "main thread is not in main loop"
Wanneer je kaspersmicrobit combineert met tkinter (de window module die gebruikt wordt in [Programmeren met Python](https://www.visualsteps.nl/programmerenpython/))
kan je de TK fout "main thread is not in main loop" tegenkomen. Dit is waarschijnlijk omdat je TK code oproept vanuit
een callback functie die je meegegeven hebt om omgeroepen te worden wanneer een druk op de knop gebeurt of wanneer
er nieuwe accelerometer gegevens zijn (of iets anders). Deze callback wordt uitgevoerd op een andere thread en tkinter
wil dit niet. Hier zijn minstens 2 oplossingen voor:  

  - roep geen tkinter code op in een callback
  - omsluit de callback met `kaspersmicrobit.tkinter.do_in_tkinter(tk, jouw_callback)` dit zorgt ervoor dat je callback
    uitgevoerd zal worden op de tk thread, dit vermijdt het probleem
