#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Callable, List

from ..bluetoothdevice import BluetoothDevice
from ..bluetoothprofile.characteristics import Characteristic
from .event import Event


def _for_each(events: List[Event], callback: Callable[[Event], None]):
    for event in events:
        callback(event)


class EventService:
    """
    Met behulp van deze klasse kan je luisteren naar gebeurtenissen (events) die plaatsvinden op de microbit.
    De microbit meldt deze gebeurtenissen op zijn interne messagebus.

    De device ids en event ids verschillen tussen de verschillende microbit versies.
    Zie `kaspersmicrobit.services.v1_events` voor de ids van de microbit v1, en
    `kaspersmicrobit.services.v2_events` voor de ids van de microbit v2

    Ook de microbit zelf kan via deze service aangeven dat hij geïnteresseerd is om bepaalde events te onvangen.
    Je kan dus ook zelfgemaakte events naar de microbit doorsturen.

    Dit zijn alle mogelijkheden aangeboden door de bluetooth event service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/event-service/
    """

    def __init__(self, device: BluetoothDevice):
        self._device = device

    def notify_microbit_requirements(self, callback: Callable[[Event], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden welke events de microbit zou willen ontvangen
        Wanneer een event een event_waarde van 0 bevat betekent dit dat de microbit geinformeerd wil worden van elke
        event van het gegeven device_id

        Je kan dan met `write_client_event` de microbit op de hoogte houden van deze gebeurtenissen

        Args:
            callback: een functie die wordt opgeroepen met een Event
        """
        self._device.notify(Characteristic.MICROBIT_REQUIREMENTS,
                            lambda sender, data: _for_each(Event.list_from_bytes(data), callback))

    def read_microbit_requirements(self) -> [Event]:
        """
        Leest de lijst van events die de microbit zou willen ontvangen van jou wanneer ze zich voordoen
        Wanneer een event een event_waarde van 0 bevat betekent dit dat de microbit geinformeerd wil worden van elke
        event van het gegeven device_id

        Je kan dan met `write_client_event` de microbit op de hoogte houden van deze gebeurtenissen

        Returns ([Event]):
            Een lijst van events waarvan je de microbit moet verwittigen wanneer ze zich voordoen
        """
        return Event.list_from_bytes(self._device.read(Characteristic.MICROBIT_REQUIREMENTS))

    def notify_microbit_event(self, callback: Callable[[Event], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden van events die zich voordoen op de microbit
        Je zal enkel verwittigd worden van events waarvan je met `write_client_requirements` hebt aangegeven dat
        je ze wil ontvangen

        Args:
            callback: een functie die wordt opgeroepen met een Event
        """
        self._device.notify(Characteristic.MICROBIT_EVENT,
                            lambda sender, data: _for_each(Event.list_from_bytes(data), callback))

    def read_microbit_event(self) -> [Event]:
        """
        Leest de lijst van events die zich hebben voorgedaan op de microbit
        Je zal enkel events kunnen uitlezen waarvan je met `write_client_requirements` hebt aangegeven dat
        je ze wil ontvangen

        Returns ([Event]):
            Een lijst van events die zich hebben voorgedaan op de microbit
        """
        return Event.list_from_bytes(self._device.read(Characteristic.MICROBIT_EVENT))

    def write_client_requirements(self, *events: Event):
        """
        Met deze methode geeft je aan in welke events van de microbit je geïnteresseerd bent. Deze events kan je dan
        ontvangen met `notify_microbit_event` of uitlezen met `read_microbit_event` als ze zich voordoen.

        Wanneer je een event met een event_waarde van 0 schrijft betekent dit dat je geinformeerd wil worden van elke
        event van het gegeven device_id

        Args:
            *events (Event): de events die je wil ontvangen van de microbit
        """
        for event in events:
            self._device.write(Characteristic.CLIENT_REQUIREMENTS, event.to_bytes())

    def write_client_event(self, *events: Event):
        """
        Met deze methode zend je events naar de microbit. Hiermee kan je de microbit op de hoogte houden van events die
        zich voordoen in je applicatie. Zend enkel events waarvan de microbit heeft aangegeven ze te willen ontvangen
        door `notify_microbit_requirements` of `read_microbit_requirements`

        Args:
           *events (Event): de events die je wil verzenden naar de microbit
        """
        for event in events:
            self._device.write(Characteristic.CLIENT_EVENT, event.to_bytes())
