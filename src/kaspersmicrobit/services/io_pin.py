#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Callable, TypeVar, Union, Generic, Type

from ..bluetoothdevice import BluetoothDevice, ByteData
from ..bluetoothprofile.characteristics import Characteristic


class Pin(IntEnum):
    """
    De pins beschikbaar voor configuratie en uitlezen via de io pin service.

    Pins 17 en 18 zijn niet beschikbaar
    """
    P0 = 0
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4
    P5 = 5
    P6 = 6
    P7 = 7
    P8 = 8
    P9 = 9
    P10 = 10
    P11 = 11
    P12 = 12
    P13 = 13
    P14 = 14
    P15 = 15
    P16 = 16
    P19 = 17
    P20 = 18


class PinAD(Enum):
    DIGITAL = 0
    ANALOG = 1


class PinIO(Enum):
    OUTPUT = 0
    INPUT = 1


PinConfigurationValue = Union[PinAD, PinIO]

T = TypeVar('T', bound=PinConfigurationValue)


class PinConfiguration(Generic[T]):
    NUMBER_OF_PINS = len(Pin)

    def __init__(self, configuration_value_type: Type[T], configuration: [T] = None):
        self._configuration = configuration if configuration \
            else [configuration_value_type(0)] * PinConfiguration.NUMBER_OF_PINS

    def __getitem__(self, item) -> T:
        return self._configuration.__getitem__(item)

    def __setitem__(self, key, value: T):
        self._configuration.__setitem__(key, value)

    def __str__(self):
        return self._configuration.__str__()

    def to_bytes(self) -> bytes:
        bits = 0
        for pin in range(PinConfiguration.NUMBER_OF_PINS):
            bits |= self._configuration[pin].value << pin

        return bits.to_bytes(4, "little")

    @staticmethod
    def list_from_bytes(configuration_value_type: Type[T], value: ByteData) -> [T]:
        bits = int.from_bytes(value[0:4], "little")
        configuration = []
        for pin in range(PinConfiguration.NUMBER_OF_PINS):
            configuration.append(configuration_value_type((bits >> pin) & 1))

        return configuration


class PinIOConfiguration(PinConfiguration[PinIO]):
    """
    De pin IO configuratie. Bevat voor iedere pin of die voor INPUT of OUTPUT gebruikt wordt
    """
    def __init__(self, configuration: [T] = None):
        super(PinIOConfiguration, self).__init__(PinIO, configuration=configuration)

    @staticmethod
    def from_bytes(value: ByteData) -> 'PinIOConfiguration':
        return PinIOConfiguration(PinConfiguration.list_from_bytes(PinIO, value))


class PinADConfiguration(PinConfiguration[PinAD]):
    """
    De pin AD configuratie. Bevat voor iedere pin of die voor ANALOG of DIGITAL gebruik is
    """
    def __init__(self, configuration: [T] = None):
        super(PinADConfiguration, self).__init__(PinAD, configuration=configuration)

    @staticmethod
    def from_bytes(value: ByteData) -> 'PinADConfiguration':
        return PinADConfiguration(PinADConfiguration.list_from_bytes(PinAD, value))


@dataclass
class PinValue:
    """
    De pin en zijn waarde

    Attributes:
        pin (Pin): de pin
        value (int): de waarde van de pin (door hoe deze waarde verzonden wordt over bluetooth)
            verliest de waarde precisie (de minst significante 2 bits worden niet verzonden)
            dit betekent bvb dat een waarde 1-3 als 0 en 255 als 252 wordt verzonden.
    """
    pin: Pin
    value: int

    @staticmethod
    def from_bytes(ad_config: PinADConfiguration, values: ByteData) -> 'PinValue':
        pin = Pin(int.from_bytes(values[0:1], "little"))
        compressed_value = int.from_bytes(values[1:2], "little")
        decompressed_value = compressed_value if ad_config[pin] == PinAD.DIGITAL else compressed_value << 2
        return PinValue(pin, decompressed_value)

    def to_bytes(self, ad_config: PinADConfiguration) -> bytes:
        compressed_value = self.value if ad_config[self.pin] == PinAD.DIGITAL else (self.value >> 2)
        return self.pin.value.to_bytes(1, "little") + compressed_value.to_bytes(1, "little")

    @staticmethod
    def list_from_bytes(ad_config: PinADConfiguration, values: ByteData) -> ['PinValue']:
        result = []
        for i in range(0, len(values), 2):
            result.append(PinValue.from_bytes(ad_config, values[i:i+2]))

        return result

    @staticmethod
    def list_to_bytes(ad_config: PinADConfiguration, values: ['PinValue']) -> bytes:
        result = bytes()
        for pin_value in values:
            result += pin_value.to_bytes(ad_config)

        return result


@dataclass
class PwmControlData:
    """
    Een klasse om PWM opdrachten te geven aan de microbit

    Attributes:
        pin (Pin): de pin waar de opdracht voor dient
        value (int): een waarde in het bereik (0-1024) (0 betekent uitgeschakeld)
        period (int): de periode in microseconden
    """
    pin: Pin
    value: int
    period: int

    @staticmethod
    def from_bytes(values: ByteData) -> 'PwmControlData':
        return PwmControlData(
            Pin(int.from_bytes(values[0:1], "little")),
            int.from_bytes(values[1:3], "little"),
            int.from_bytes(values[3:7], "little"),
        )

    def to_bytes(self) -> bytes:
        return self.pin.value.to_bytes(1, "little") \
               + self.value.to_bytes(2, "little") \
               + self.period.to_bytes(4, "little")


class IOPinService:
    """
    Deze klasse bevat de functies die je kan aanspreken in verband met de io pins op de rand van de microbit

    Dit zijn alle mogelijkheden aangeboden door de bluetooth io pin service

    See Also: https://tech.microbit.org/hardware/edgeconnector/

    See Also: https://www.micro-bit.nl/kennisbank-pinnen

    See Also: https://lancaster-university.github.io/microbit-docs/ble/iopin-service/
    """

    def __init__(self, device: BluetoothDevice):
        self._pin_ad_config = PinADConfiguration()
        self._device = device

    def notify_data(self, callback: Callable[[[PinValue]], None]):
        """
        Deze methode kan je oproepen wanneer je verwittigd wil worden van de waarde van pins. Deze pins moet je
        voorafgaand geconfigureerd hebben als PinIO.INPUT pins vie write_io_configuration. Je wordt verwittigd wanneer
        de waarde wijzigt.

        Args:
            callback: een functie die wordt opgeroepen met een lijst van PinValue objecten
        """
        self._device.notify(Characteristic.PIN_DATA,
                            lambda sender, data: callback(PinValue.list_from_bytes(self._pin_ad_config, data)))

    def read_data(self) -> [PinValue]:
        """
        Geeft de waarden voor iedere pin die geconfigureerd is als PinIO.INPUT via write_io_configuration.

        Returns ([PinValue]):
            Een lijst van input pins en hun bijhorende waarde
        """
        return PinValue.list_from_bytes(self._pin_ad_config, self._device.read(Characteristic.PIN_DATA))

    def write_data(self, values: [PinValue]):
        """
        Schrijft waarden naar 1 of meer pins. Deze pins moet je voorafgaand geconfigureerd hebben als PinIO.OUTPUT pins
        via write_io_configuration. Wanneer jes chrijft naar een input pin zal dit genegeerd worden

        Args:
            values ([PinValue]): de output pins en hun bijhorende waarde
        """
        if values:
            self._device.write(Characteristic.PIN_DATA, PinValue.list_to_bytes(self._pin_ad_config, values))

    def read_ad_configuration(self) -> PinADConfiguration:
        """
        Geeft voor iedere pin of die geconfigureerd is als een PinAD.DIGITAL of PinAD.ANALOG pin.

        Returns (PinADConfiguration):
            De analoog-digitaal configuratie voor iedere pin
        """
        return PinADConfiguration.from_bytes(self._device.read(Characteristic.PIN_AD_CONFIGURATION))

    def write_ad_configuration(self, config: PinADConfiguration):
        """
        Configureer iedere pin voor analoog of digitaal gebruik.

        Args:
            config (PinADConfiguration): De analoog-digitaal configuratie voor iedere pin
        """
        self._device.write(Characteristic.PIN_AD_CONFIGURATION, config.to_bytes())
        self._pin_ad_config = PinADConfiguration(config[:])

    def read_io_configuration(self) -> PinIOConfiguration:
        """
        Geeft voor iedere pin of die geconfigureerd is als een PinIO.INPUT of PinIO.OUTPUT pin.

        Returns (PinIOConfiguration):
            De input-output configuratie voor iedere pin
        """
        return PinIOConfiguration.from_bytes(self._device.read(Characteristic.PIN_IO_CONFIGURATION))

    def write_io_configuration(self, config: PinIOConfiguration):
        """
        Configureer iedere pin voor input of output.
        Enkel waarden van pins die als PinIO.INPUT geconfigureerd worden kunnen uitgelezen worden
        met read_data, en enkel voor deze pins kan je updates krijgen met notify_data.
        Enkel naar pins die geconfigureerd zijn als PinIO.OUTPUT kan je waarden schrijven.

        Args:
            config (PinIOConfiguration): De input-output configuratie voor iedere pin
        """
        self._device.write(Characteristic.PIN_IO_CONFIGURATION, config.to_bytes())

    def write_pwm_control_data(self, pwm_control1: PwmControlData, pwm_control2: PwmControlData = None):
        """
        Schrijft Pulse Width Modulation opdrachten naar de microbit. 1 of 2 opdrachten kunnen tegelijk gegeven worden

        See Also: https://microbit-micropython.readthedocs.io/en/latest/pin.html

        See Also: https://www.micro-bit.nl/kennisbank-pinnen

        Args:
            pwm_control1 (PwmControlData): een PWM opdracht
            pwm_control2 (PwmControlData): een optionele PWM opdracht
        """
        data = pwm_control1.to_bytes() + pwm_control2.to_bytes() if pwm_control2 else pwm_control1.to_bytes()
        self._device.write(Characteristic.PWM_CONTROL, data)
