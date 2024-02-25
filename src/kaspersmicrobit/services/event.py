#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from typing import List

from ..bluetoothdevice import ByteData


@dataclass
class Event:
    """
    An Event takes place for a specific device or component (device) on the micro:bit.
    For example, a data update (event) from the accelerometer (device) or a press (event) on a button (device)

    See `kaspersmicrobit.services.v1_events` for the device ids and event values for the micro:bit v1, and
    `kaspersmicrobit.services.v2_events` for the ids and values of the micro:bit v2

    Attributes:
        device_id (int): The ID of the device or component reporting the event
        event_value (int): The value of the event for the given device
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
    def list_from_bytes(values: ByteData) -> List['Event']:
        result = []
        for i in range(0, len(values), 4):
            result.append(Event.from_bytes(values[i:i + 4]))

        return result

    @staticmethod
    def list_to_bytes(values: List['Event']) -> bytes:
        result = bytes()
        for event in values:
            result += event.to_bytes()

        return result
