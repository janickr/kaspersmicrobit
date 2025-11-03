#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging

from kaspersmicrobit import KaspersMicrobit

logging.basicConfig(level=logging.INFO)

# example-first {

# Look for a micro:bit and connect to it
# / Zoek een willekeurige micro:bit en verbind ermee
with KaspersMicrobit.find_one_microbit() as a_microbit:
    print(f'Bluetooth address: {a_microbit.address()}')
    print(f'Device name: {a_microbit.name()}')

# }
# example-multiple {

# Look for all active micro:bits and connect to them one after another
# / zoek alle micro:bits en verbind er om de beurt mee
multiple_microbits = KaspersMicrobit.find_microbits()
for microbit in multiple_microbits:
    with microbit:
        print(f'Bluetooth address: {microbit.address()}')
        print(f'Device name: {microbit.name()}')

# }
# example-name {

# Look for the micro:bit with the name 'tupaz' and connect to it
# (this does not work with pairing)
# / zoek de micro:bit met de naam 'tupaz' en verbind ermee
# (dit werkt niet met pairing)
with KaspersMicrobit.find_one_microbit(microbit_name='tupaz') as tupaz:
    print(f'Bluetooth address: {tupaz.address()}')
    print(f'Device name: {tupaz.name()}')

# }
# example-address {

# Connect to the micro:bit with the address 'E3:7E:99:0D:C1:BA'
# / Maak een verbinding met de micro:bit met het adres 'E3:7E:99:0D:C1:BA'
with KaspersMicrobit('E3:7E:99:0D:C1:BA') as addressed:
    print(f'Bluetooth address: {addressed.address()}')
    print(f'Device name: {addressed.name()}')
# }
