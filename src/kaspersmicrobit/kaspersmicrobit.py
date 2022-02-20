#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from .bluetoothdevice import BluetoothDevice, BluetoothEventLoop
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
    Dit is de klasse die je kan gebruiken om met een microbit te verbinden.
    Door middel van deze klasse kan je onder meer

    - gegevens over de microbit uitlezen
    - gegevens van de sensoren van de microbit uitlezen of je laten verwittigen van gegevens van sensoren
    - componenten op de microbit aansturen, bvb de LEDs

    Example:
    ```python
    with KaspersMicrobit("MICROBIT_BLUETOOTH_ADDRESS") as microbit:
        microbit.buttons.on_button_a(press=pressed, long_press=pressed_long, up=released)
        microbit.buttons.on_button_b(press=pressed, long_press=pressed_long, up=released)
        microbit.temperature.notify(lambda temp: print(f'{temp}°C'))
        print(microbit.accelerometer.read())
        microbit.uart.send_string("Hello kasper, this is working out very well\\n")
        time.sleep(25)
    ```

    ```python
    microbit = KaspersMicrobit("MICROBIT_BLUETOOTH_ADDRESS")
    try:
        microbit.connect()
        microbit.buttons.on_button_a(press=pressed, long_press=pressed_long, up=released)
        microbit.buttons.on_button_b(press=pressed, long_press=pressed_long, up=released)
        microbit.temperature.notify(lambda temp: print(f'{temp}°C'))
        print(microbit.accelerometer.read())
        microbit.uart.send_string("Hello kasper, this is working out very well\\n")
        time.sleep(25)
    finally:
        microbit.disconnect()
    ```

    Attributes:
        device_information (DeviceInformationService):
            Om informatie te vragen over de maker van je microbit
        generic_access (GenericAccessService):
            Om informatie te vragen over je microbit
        buttons (ButtonService):
            Om je te laten verwittigen wanneer een van de twee knoppen van de microbit worden ingedrukt (of losgelaten)
        temperature (TemperatureService):
            Om de temperatuur van de omgeving van de microbit op te vragen (of je te laten verwittigen)
        accelerometer (AccelerometerService):
            Om je te laten verwittigen van versnelling (beweging, botsing,...) van de microbit
        events (EventService):
            Om je in te schrijven op het ontvangen van gebeurtenissen van verschillende componenten van de microbit
        uart (UartService):
            Om tekst te sturen naar of te ontvangen van de microbit
        io_pin (IOPinService):
            Bestuur, lees, configureer de I/O contacten (pins) op de microbit
        led (LedService):
            Bestuur de LEDs van de microbit
        magnetometer (MagnetometerService):
            Om de gegevens van de magnetometer uit te lezen, of je ervan te laten verwittigen. De magnetometer meet
            heet magnetisch veld in de omgeving van de microbit (bvb het magnetisch veld van de aarde)


    See Also: https://makecode.microbit.org/reference/bluetooth

    See Also: https://makecode.microbit.org/device
    """

    def __init__(self, address: str, loop: BluetoothEventLoop = None):
        """
        Maak een KaspersMicrobit object met een gegeven bluetooth address.

        Args:
            address (str): het bluetooth adres van de microbit
            loop (BluetoothEventLoop): dit mag je leeg laten, dit bepaalt welke thread de communicatie met de microbit
                uitvoert.
        """
        self._device = BluetoothDevice(address, loop=loop)
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
        Connecteer met de microbit. Dit brengt een verbinding tot stand.
        Een microbit moet gepaired zijn met je computer voor dat je ermee kan verbinden. Je microbit mag nog geen
        verbinding hebben.

        Problemen in verband met bluetooth connecties met de microbit kunnen vaak verholpen worden door je computer
        opnieuw te pairen met je microbit.

        See Also: https://support.microbit.org/helpdesk/attachments/19075694226
        """
        self._device.connect()

    def disconnect(self) -> None:
        """
        Verbreek de verbinding met de microbit.
        Je moet verbonden zijn met deze microbit om deze methode succesvol te kunnen oproepen.
        """
        self._device.disconnect()
