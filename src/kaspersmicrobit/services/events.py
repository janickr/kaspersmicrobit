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
    Met behulp van deze klasse kan je luisteren naar gebeurtenissen (events) die plaatsvinden op de micro:bit.
    De micro:bit meldt deze gebeurtenissen op zijn interne messagebus.

    De device ids en event ids verschillen tussen de verschillende micro:bit versies.
    Zie `kaspersmicrobit.services.v1_events` voor de ids van de micro:bit v1, en
    `kaspersmicrobit.services.v2_events` voor de ids van de micro:bit v2

    Ook de micro:bit zelf kan via deze service aangeven dat hij geïnteresseerd is om bepaalde events te onvangen.
    Je kan dus ook zelfgemaakte events naar de micro:bit doorsturen.

    Dit zijn alle mogelijkheden aangeboden door de bluetooth event service

    See Also: https://lancaster-university.github.io/microbit-docs/ble/event-service/
    """

    def __init__(self, device: BluetoothDevice):
        self._device = device

    def is_available(self) -> bool:
        """
        Kijkt na of de event bluetooth service gevonden wordt op de geconnecteerde micro:bit.

        Returns:
            true als de event service gevonden werd, false indien niet.
        """
        return self._device.is_service_available(Service.EVENT)

    def notify_microbit_requirements(self, callback: Callable[[Event], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden welke events de micro:bit zou willen ontvangen
        Wanneer een event een event_waarde van 0 bevat betekent dit dat de micro:bit geinformeerd wil worden van elke
        event van het gegeven device_id

        Je kan dan met `write_client_event` de micro:bit op de hoogte houden van deze gebeurtenissen

        Args:
            callback: een functie die wordt opgeroepen met een Event

        Raises:
            BluetoothServiceNotFound: Wanneer de events service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de events service actief is, maar er geen manier was
                om de notificaties voor de microbit requirements te activeren (komt normaal gezien niet voor)
        """
        self._device.notify(Characteristic.MICROBIT_REQUIREMENTS,
                            lambda sender, data: _for_each(Event.list_from_bytes(data), callback))

    def read_microbit_requirements(self) -> List[Event]:
        """
        Leest de lijst van events die de micro:bit zou willen ontvangen van jou wanneer ze zich voordoen
        Wanneer een event een event_waarde van 0 bevat betekent dit dat de micro:bit geinformeerd wil worden van elke
        event van het gegeven device_id

        Je kan dan met `write_client_event` de micro:bit op de hoogte houden van deze gebeurtenissen

        Returns:
            List[Event]: Een lijst van events waarvan je de micro:bit moet verwittigen wanneer ze zich voordoen

        Raises:
            BluetoothServiceNotFound: Wanneer de events service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de events service actief is, maar er geen manier was
                om de microbit requirements te lezen (komt normaal gezien niet voor)
        """
        return Event.list_from_bytes(self._device.read(Service.EVENT, Characteristic.MICROBIT_REQUIREMENTS))

    def notify_microbit_event(self, callback: Callable[[Event], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden van events die zich voordoen op de micro:bit
        Je zal enkel verwittigd worden van events waarvan je met `write_client_requirements` hebt aangegeven dat
        je ze wil ontvangen

        Args:
            callback: een functie die wordt opgeroepen met een Event

        Raises:
            BluetoothServiceNotFound: Wanneer de events service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de events service actief is, maar er geen manier was
                om de notificaties voor de microbit events te activeren (komt normaal gezien niet voor)
        """
        self._device.notify(Service.EVENT, Characteristic.MICROBIT_EVENT,
                            lambda sender, data: _for_each(Event.list_from_bytes(data), callback))

    def read_microbit_event(self) -> List[Event]:
        """
        Leest de lijst van events die zich hebben voorgedaan op de micro:bit
        Je zal enkel events kunnen uitlezen waarvan je met `write_client_requirements` hebt aangegeven dat
        je ze wil ontvangen

        Returns:
            List[Event]: Een lijst van events die zich hebben voorgedaan op de micro:bit

        Raises:
            BluetoothServiceNotFound: Wanneer de events service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de events service actief is, maar er geen manier was
                om de microbit events te lezen (komt normaal gezien niet voor)
        """
        return Event.list_from_bytes(self._device.read(Service.EVENT, Characteristic.MICROBIT_EVENT))

    def write_client_requirements(self, *events: Event):
        """
        Met deze methode geeft je aan in welke events van de micro:bit je geïnteresseerd bent. Deze events kan je dan
        ontvangen met `notify_microbit_event` of uitlezen met `read_microbit_event` als ze zich voordoen.

        Wanneer je een event met een event_waarde van 0 schrijft betekent dit dat je geinformeerd wil worden van elke
        event van het gegeven device_id

        Args:
            *events (Event): de events die je wil ontvangen van de micro:bit

        Raises:
            BluetoothServiceNotFound: Wanneer de events service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de events service actief is, maar er geen manier was
                om de client requirements te schrijven (komt normaal gezien niet voor)
        """
        for event in events:
            self._device.write(Service.EVENT, Characteristic.CLIENT_REQUIREMENTS, event.to_bytes())

    def write_client_event(self, *events: Event):
        """
        Met deze methode zend je events naar de micro:bit. Hiermee kan je de micro:bit op de hoogte houden van events die
        zich voordoen in je applicatie. Zend enkel events waarvan de micro:bit heeft aangegeven ze te willen ontvangen
        door `notify_microbit_requirements` of `read_microbit_requirements`

        Args:
           *events (Event): de events die je wil verzenden naar de micro:bit

        Raises:
            BluetoothServiceNotFound: Wanneer de events service niet actief is op de micro:bit
            BluetoothCharacteristicNotFound: Wanneer de events service actief is, maar er geen manier was
                om de client events te schrijven (komt normaal gezien niet voor)
        """
        for event in events:
            self._device.write(Service.EVENT, Characteristic.CLIENT_EVENT, event.to_bytes())
