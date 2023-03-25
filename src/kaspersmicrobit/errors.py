#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from bleak import BLEDevice, BleakClient

from kaspersmicrobit.bluetoothprofile.characteristics import Characteristic
from kaspersmicrobit.bluetoothprofile.services import Service


class KaspersMicrobitNotFound(Exception):
    """
    Wordt gegooid wanneer geen micro:bit gevonden werd, terwijl dit wel verwacht werd.

    Attributes:
        name (str):
            De naam van de micro:bit waar naar gezocht werd
        devices (List[BLEDevice]):
            De lijst van toestellen die wel gevonden werden
    """

    def __init__(self, name: str, devices: List[BLEDevice]):
        found_devices = '\n'.join([f'  - {device.address} {device.name}' for device in devices])
        super().__init__(
            f'Could not find the micro:bit with name "{name}"\n'
            f'The following devices were detected:\n'
            f'{ found_devices }\n\n'
            f'Is the micro:bit loaded with the correct ".hex" file and powered on?'
        )
        self.name = name
        self.devices = devices


class BluetoothCharacteristicNotFound(Exception):
    """
        Wordt gegooid wanneer een Bluetooth GATT characteristic niet gevonden werd, terwijl dit wel verwacht werd.

        Attributes:
            service (Service):
                De micro:bit bluetooth service waarin de characteristic gezocht werd
            characteristic (Characteristic):
                De characteristic die niet gevonden werd
        """
    def __init__(self, client: BleakClient, service: Service, characteristic: Characteristic):
        available_characteristics = '\n'.join(
            [
                f'  - {gatt_characteristic.description:35}'
                f' ({str(Characteristic.lookup(gatt_characteristic.uuid)):40} uuid={gatt_characteristic.uuid})'
                for gatt_characteristic in client.services.get_service(service.value).characteristics
            ]
        )
        super().__init__(
            f'Could not find the characteristic {characteristic.name} (uuid={characteristic.value})\n'
            f'The available characteristics of the service {service} on this micro:bit are:\n'
            f'{available_characteristics}')
        self.service = service
        self.characteristic = characteristic


class BluetoothServiceNotFound(Exception):
    """
        Wordt gegooid wanneer een Bluetooth service niet gevonden werd, terwijl dit wel verwacht werd.

        Attributes:
            service (Service):
                De micro:bit bluetooth service die niet gevonden werd
        """
    def __init__(self, client: BleakClient, service: Service):
        available_services = '\n'.join(
            [
                f'  - {gatt_service.description:30}'
                f' ({str(Service.lookup(gatt_service.uuid)):27} uuid={gatt_service.uuid})'
                for gatt_service in client.services
            ]
        )
        super().__init__(
            f'Could not find the service {service} (uuid={service.value})\n'
            f'The available services on this micro:bit are:\n'
            f'{ available_services }\n\n'
            f'Is this micro:bit loaded with the correct ".hex" file?'
        )
        self.service = service
