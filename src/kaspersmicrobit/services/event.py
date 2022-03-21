#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from ..bluetoothdevice import ByteData


@dataclass
class Event:
    """
    Een Event is een gebeurtenis die plaatsvindt voor een bepaald toestel of component (device) op de microbit.
    Bijvoorbeeld een data update (event) van de accellerometer (toestel) of een druk (event) op een knop (toestel)

    Zie `kaspersmicrobit.services.v1_events` voor de device ids en de event values voor de microbit v1, en
    `kaspersmicrobit.services.v2_events` voor de ids en valuesvan de microbit v2

    Attributes:
        device_id (int): Het id van van het toestel of de component dat de gebeurtenis meldt
        event_value (int): De waarde van de gebeurtenis voor het gegeven toestel
    """
    device_id: int
    event_value: int = 0

    @staticmethod
    def from_bytes(values: ByteData):
        return Event(
            int.from_bytes(values[0:2], "little"),
            int.from_bytes(values[2:4], "little")
        )

    def to_bytes(self) -> bytes:
        return self.device_id.to_bytes(2, "little") + self.event_value.to_bytes(2, "little")

    @staticmethod
    def list_from_bytes(values: ByteData) -> ['Event']:
        result = []
        for i in range(0, len(values), 4):
            result.append(Event.from_bytes(values[i:i + 4]))

        return result

    @staticmethod
    def list_to_bytes(values: ['Event']) -> bytes:
        result = bytes()
        for event in values:
            result += event.to_bytes()

        return result
