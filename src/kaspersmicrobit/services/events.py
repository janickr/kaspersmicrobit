#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Callable, List

from ..bluetoothdevice import BluetoothDevice
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service
from .event import Event


def _for_each(events: List[Event], callback: Callable[[Event], None]):
    for event in events:
        callback(event)


class EventService:
    """
    Using this class you can listen to events that take place on the micro:bit.
    The micro:bit reports these events on its internal message bus.

    The device IDs and event IDs differ between the different micro:bit versions.
    See `kaspersmicrobit.services.v1_events` for the ids of the micro:bit v1, and
    `kaspersmicrobit.services.v2_events` for the ids of the micro:bit v2

    The micro:bit itself can also indicate through this service that it is interested in receiving certain events.
    So you can also forward self-made events to the micro:bit.

    These are all options offered by the Bluetooth event service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/event-service/
    """

    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Checks whether the event Bluetooth service is found on the connected micro:bit.

        Returns:
            true if the event service was found, false if not.
        """
        return self._device.is_service_available(Service.EVENT)

    def notify_microbit_requirements(self, callback: Callable[[Event], None]):
        """
        You can call this method when you want to be notified which events the micro:bit would like to receive
        When an event contains an event_value of 0, this means that the micro:bit wants to be informed of each
        event of the given device_id

        You can then use `write_client_event` to keep the micro:bit informed of these events

        Args:
            callback: a function that is called with an Event

        Raises:
            errors.BluetoothServiceNotFound: When the events service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the events service is running but there was no way
                to activate the notifications for the microbit requirements (normally does not occur)
        """
        self._device.notify(Characteristic.MICROBIT_REQUIREMENTS,
                            lambda sender, data: _for_each(Event.list_from_bytes(data), callback))

    def read_microbit_requirements(self) -> List[Event]:
        """
        Reads the list of events that the micro:bit would like to receive from you as they occur
        When an event contains an event_value of 0, this means that the micro:bit wants to be informed of each
        event of the given device_id

        You can then use `write_client_event` to keep the micro:bit informed of these events

        Returns:
            List[Event]: A list of events that you need to notify the micro:bit when they occur

        Raises:
            errors.BluetoothServiceNotFound: When the events service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the events service is running but there was no way
                to read the microbit requirements (normally does not occur)
        """
        return Event.list_from_bytes(self._device.read(Service.EVENT, Characteristic.MICROBIT_REQUIREMENTS))

    def notify_microbit_event(self, callback: Callable[[Event], None]):
        """
        You can call this method when you want to be notified of events that occur on the micro:bit
        You will only be notified of events that you have indicated with `write_client_requirements`
        you want to receive them

        Args:
            callback: a function that is called with an Event

        Raises:
            errors.BluetoothServiceNotFound: When the events service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the events service is running but there was no way
                to activate the notifications for the microbit events (normally does not occur)
        """
        self._device.notify(Service.EVENT, Characteristic.MICROBIT_EVENT,
                            lambda sender, data: _for_each(Event.list_from_bytes(data), callback))

    def read_microbit_event(self) -> List[Event]:
        """
        Reads the list of events that occurred on the micro:bit
        You will only be able to read events for which you have specified with `write_client_requirements`
        you want to receive them

        Returns:
            List[Event]: A list of events that occurred on the micro:bit

        Raises:
            errors.BluetoothServiceNotFound: When the events service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the events service is running but there was no way
                to read the microbit events (normally does not occur)
        """
        return Event.list_from_bytes(self._device.read(Service.EVENT, Characteristic.MICROBIT_EVENT))

    def write_client_requirements(self, *events: Event):
        """
        Using this method you indicate which micro:bit events you are interested in. Then, you'll be able to receive
        these events with `notify_microbit_event` or read out with `read_microbit_event` when they occur.

        When you write an event with an event_value of 0, this means that you want to be informed of each
        event of the given device_id

        Args:
            *events (Event): the events you want to receive from the micro:bit

        Raises:
            errors.BluetoothServiceNotFound: When the events service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the events service is running but there was no way
                to write the client requirements (normally does not occur)
        """
        for event in events:
            self._device.write(Service.EVENT, Characteristic.CLIENT_REQUIREMENTS, event.to_bytes())

    def write_client_event(self, *events: Event):
        """
        With this method you send events to the micro:bit. This allows you to keep the micro:bit informed of events that
        occur in your application. Only send events that the micro:bit has indicated it wants to receive
        by `notify_microbit_requirements` or `read_microbit_requirements`

        Args:
           *events (Event): the events you want to send to the micro:bit

        Raises:
            errors.BluetoothServiceNotFound: When the events service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the events service is running but there was no way
                to write the client events (normally does not occur)
        """
        for event in events:
            self._device.write(Service.EVENT, Characteristic.CLIENT_EVENT, event.to_bytes())
