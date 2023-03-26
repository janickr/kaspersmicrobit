#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Union

from bleak import BleakClient, BleakScanner

from .bluetoothdevice import BluetoothDevice, BluetoothEventLoop, ThreadEventLoop
from .errors import KaspersMicrobitNotFound
from .services.device_information import DeviceInformationService
from .services.generic_access import GenericAccessService
from .services.buttons import ButtonService
from .services.temperature import TemperatureService
from .services.accelerometer import AccelerometerService
from .services.events import EventService
from .services.uart import UartService
from .services.magnetometer import MagnetometerService
from .services.io_pin import IOPinService
from .services.led import LedService


class KaspersMicrobit:
    """
    Dit is de klasse die je kan gebruiken om met een micro:bit te verbinden.
    Je kan hiermee:

    - gegevens over de micro:bit uitlezen
    - gegevens van de sensoren van de micro:bit uitlezen of je laten verwittigen van gegevens van sensoren
    - componenten op de micro:bit aansturen, bvb de LEDs

    Example:
    ```python
    with KaspersMicrobit.find_one_microbit() as microbit:
        microbit.buttons.on_button_a(press=pressed, long_press=pressed_long, up=released)
        microbit.temperature.notify(lambda temp: print(f'{temp}°C'))
        time.sleep(25)
    ```

    ```python
    microbit = KaspersMicrobit.find_one_microbit()
    try:
        microbit.connect()
        microbit.buttons.on_button_a(press=pressed, long_press=pressed_long, up=released)
        microbit.temperature.notify(lambda temp: print(f'{temp}°C'))
        time.sleep(25)
    finally:
        microbit.disconnect()
    ```

    Attributes:
        device_information (DeviceInformationService):
            Om informatie te vragen over de maker van je micro:bit
        generic_access (GenericAccessService):
            Om informatie te vragen over je micro:bit
        buttons (ButtonService):
            Om je te laten verwittigen wanneer een van de twee knoppen van de micro:bit worden ingedrukt (of losgelaten)
        temperature (TemperatureService):
            Om de temperatuur van de omgeving van de micro:bit op te vragen (of je te laten verwittigen)
        accelerometer (AccelerometerService):
            Om je te laten verwittigen van versnelling (beweging, botsing,...) van de micro:bit
        events (EventService):
            Om je in te schrijven op het ontvangen van gebeurtenissen van verschillende componenten van de micro:bit
        uart (UartService):
            Om tekst te sturen naar of te ontvangen van de micro:bit
        io_pin (IOPinService):
            Bestuur, lees, configureer de I/O contacten (pins) op de micro:bit
        led (LedService):
            Bestuur de LEDs van de micro:bit
        magnetometer (MagnetometerService):
            Om de gegevens van de magnetometer uit te lezen, of je ervan te laten verwittigen. De magnetometer meet
            het magnetisch veld in de omgeving van de micro:bit (bvb het magnetisch veld van de aarde)


    See Also: https://makecode.microbit.org/reference/bluetooth

    See Also: https://makecode.microbit.org/device
    """

    def __init__(self, address_or_bluetoothdevice: Union[str, BluetoothDevice]):
        """
        Maak een KaspersMicrobit object met een gegeven bluetooth address.

        Args:
            address_or_bluetoothdevice: het bluetooth adres van de micro:bit
        """
        if isinstance(address_or_bluetoothdevice, BluetoothDevice):
            self._device = address_or_bluetoothdevice
        else:
            self._device = BluetoothDevice(BleakClient(address_or_bluetoothdevice))

        self.device_information = DeviceInformationService(self._device)
        self.generic_access = GenericAccessService(self._device)
        self.buttons = ButtonService(self._device)
        self.temperature = TemperatureService(self._device)
        self.accelerometer = AccelerometerService(self._device)
        self.events = EventService(self._device)
        self.uart = UartService(self._device)
        self.io_pin = IOPinService(self._device)
        self.led = LedService(self._device)
        self.magnetometer = MagnetometerService(self._device)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self) -> None:
        """
        Connecteer met de micro:bit. Dit brengt een verbinding tot stand. Je micro:bit mag nog geen (andere)
        verbinding hebben.

        Troubleshooting:
            First try turning the micro:bit off and on again.

            If you are not using the "with"-block, but calling .connect() yourself, always make sure that in any case
            you call .disconnect() when you don't need the connection anymore
            (for instance when you exit your application)

            - In case you are using "No pairing required":
              Make sure the micro:bit is not paired to your computer, if it was, remove it from the paired bluetooth
              devices
            - In case you are using "Just works pairing":
              Try to remove the micro:bit from the paired bluetooth devices and pairing it your computer again.

        See Also: https://support.microbit.org/helpdesk/attachments/19075694226
        """
        self._device.connect()

    def disconnect(self) -> None:
        """
        Verbreek de verbinding met de micro:bit.
        Je moet verbonden zijn met deze micro:bit om deze methode succesvol te kunnen oproepen.
        """
        self._device.disconnect()

    def address(self) -> str:
        """
        Geeft het Bluetooth adres van deze micro:bit

        Returns:
            Het adres van de micro:bit
        """
        return self._device.address()

    @staticmethod
    def find_microbits(timeout: int = 3, loop: BluetoothEventLoop = None) -> List['KaspersMicrobit']:
        """
        Scant naar bluetooth toestellen. Geeft een lijst van micro:bits die gevonden werd binnen de timeout

        Args:
             timeout: hoe lang er maximaal gescand wordt (in seconden)
             loop (BluetoothEventLoop): dit mag je leeg laten, dit bepaalt welke thread de communicatie met de micro:bit
                  uitvoert.

        Returns:
            List[KaspersMicrobit]: Een lijst van gevonden micro:bits, deze kan ook leeg zijn,
                  als er geen micro:bits gevonden werden

        """

        loop = loop if loop else ThreadEventLoop.single_thread()
        devices = loop.run_async(BleakScanner.discover(timeout)).result()
        name_filter = KaspersMicrobit._name_filter()
        return [
            KaspersMicrobit(BluetoothDevice(BleakClient(d), loop))
            for d in devices
            if name_filter(d.name)
        ]

    @staticmethod
    def find_one_microbit(microbit_name: str = None, timeout: int = 3, loop: BluetoothEventLoop = None) -> 'KaspersMicrobit':
        """
        Scant naar bluetooth toestellen. Geeft exact 1 micro:bit terug als er een gevonden wordt. Je kan optioneel
        een naam opgeven waarop er moet gezocht worden. Als er geen naam gegeven wordt, en er zijn meerdere micro:bits
        actief dan wordt er willekeurig een micro:bit gevonden.

        Warning:
            Enkel wanneer de micro:bit werkt met "No pairing required" adverteert de micro:bit een naam. Dus enkel in
            het geval je hex bestanden gebruikt met "No pairing required" is het nuttig om de 'microbit_name' parameter
            te gebruiken.
            Bij een micro:bit die gepaird is werkt dit niet.

        Args:
             microbit_name: de naam van de micro:bit. Dit is een naam van 5 letters zoals bvb 'tupaz' of 'gatug' ofzo
                  Dit is optioneel.
             timeout: hoe lang er maximaal gescand wordt (in seconden)
             loop (BluetoothEventLoop): dit mag je leeg laten, dit bepaalt welke thread de communicatie met de micro:bit
                  uitvoert.

        Returns:
            KaspersMicrobit: De gevonden micro:bit

        Raises:
            KaspersMicrobitNotFound: indien er geen micro:bit werd
        """
        loop = loop if loop else ThreadEventLoop.single_thread()

        def name_filter(d, ad):
            return KaspersMicrobit._name_filter(microbit_name)(ad.local_name)

        device = loop.run_async(BleakScanner.find_device_by_filter(filterfunc=name_filter, timeout=timeout)).result()
        if device:
            return KaspersMicrobit(BluetoothDevice(BleakClient(device), loop))
        else:
            raise KaspersMicrobitNotFound(microbit_name, loop.run_async(BleakScanner.discover(timeout)).result())

    @staticmethod
    def _name_filter(microbit_name: str = None):
        return lambda \
            device_name: device_name == f'BBC micro:bit [{microbit_name.strip()}]' \
            if microbit_name \
            else device_name and device_name.startswith('BBC micro:bit')
