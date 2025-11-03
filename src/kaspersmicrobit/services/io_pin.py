#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Callable, TypeVar, Union, Generic, Type, List

from ..bluetoothdevice import BluetoothDevice, ByteData
from ..bluetoothprofile.characteristics import Characteristic
from ..bluetoothprofile.services import Service


class Pin(IntEnum):
    """
    The pins available for configuration and reading via the io pin service.

    Pins 17 and 18 are not available
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
    """The analog-digital configuration of a pin"""
    DIGITAL = 0
    """Indicates that a pin is used for a digital signal"""
    ANALOG = 1
    """Indicates that a pin is used for an analog signal"""


class PinIO(Enum):
    """The input-output configuration of a pin"""
    OUTPUT = 0
    """Indicates that a pin is being used to read from"""
    INPUT = 1
    """Indicates that a pin is being used to write to"""


PinConfigurationValue = Union[PinAD, PinIO]

T = TypeVar('T', bound=PinConfigurationValue)


class PinConfiguration(Generic[T]):
    NUMBER_OF_PINS = len(Pin)

    def __init__(self, configuration_value_type: Type[T], configuration: List[T] = None):
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
    def list_from_bytes(configuration_value_type: Type[T], value: ByteData) -> List[T]:
        bits = int.from_bytes(value[0:4], "little")
        configuration = []
        for pin in range(PinConfiguration.NUMBER_OF_PINS):
            configuration.append(configuration_value_type((bits >> pin) & 1))

        return configuration


class PinIOConfiguration(PinConfiguration[PinIO]):
    """
    The IO pin configuration. Contains for each pin whether it is used for INPUT or OUTPUT
    """
    def __init__(self, configuration: List[T] = None):
        super(PinIOConfiguration, self).__init__(PinIO, configuration=configuration)

    @staticmethod
    def from_bytes(value: ByteData) -> 'PinIOConfiguration':
        return PinIOConfiguration(PinConfiguration.list_from_bytes(PinIO, value))


class PinADConfiguration(PinConfiguration[PinAD]):
    """
    The AD pin configuration. Contains for each pin whether it is for ANALOG or DIGITAL use
    """
    def __init__(self, configuration: List[T] = None):
        super(PinADConfiguration, self).__init__(PinAD, configuration=configuration)

    @staticmethod
    def from_bytes(value: ByteData) -> 'PinADConfiguration':
        return PinADConfiguration(PinADConfiguration.list_from_bytes(PinAD, value))


@dataclass
class PinValue:
    """
    The pin and its value

    Attributes:
        pin (Pin): the pin
        value (int): the value of the pin. When the value is sent over Bluetooth
            it will lose precision (the least significant 2 bits are not sent)
            This means, for example, that a value 1-3 is sent as 0 and 255 as 252.
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
    def list_from_bytes(ad_config: PinADConfiguration, values: ByteData) -> List['PinValue']:
        result = []
        for i in range(0, len(values), 2):
            result.append(PinValue.from_bytes(ad_config, values[i:i+2]))

        return result

    @staticmethod
    def list_to_bytes(ad_config: PinADConfiguration, values: List['PinValue']) -> bytes:
        result = bytes()
        for pin_value in values:
            result += pin_value.to_bytes(ad_config)

        return result


@dataclass
class PwmControlData:
    """
    A class to give PWM commands to the micro:bit

    Attributes:
        pin (Pin): the pin for which the command is intended
        value (int): a value in the range (0-1024) (0 means disabled)
        period (int): the period in microseconds
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
    This class contains the functions that you can access in connection with the io pins on the edge of the micro:bit

    These are all options offered by the Bluetooth IO PIN service

    See Also: https://tech.microbit.org/hardware/edgeconnector/

    See Also: https://www.micro-bit.nl/kennisbank-pinnen

    See Also: https://lancaster-university.github.io/microbit-docs/ble/iopin-service/
    """

    def __init__(self, device: BluetoothDevice):
        self._pin_ad_config = PinADConfiguration()
        self._device = device

    def is_available(self) -> bool:
        """
        Checks whether the I/O pin Bluetooth service is found on the connected micro:bit.

        Returns:
            true if the I/O pin service was found, false if not.
        """
        return self._device.is_service_available(Service.IO_PIN)

    def notify_data(self, callback: Callable[[List[PinValue]], None]):
        """
        You can call this method when you want to be notified of the value of pins. You need these pins
        previously configured as PinIO.INPUT pins via write_io_configuration. You will be notified when
        the value changes.

        Args:
            callback: a function called with a list of PinValue objects

        Raises:
            errors.BluetoothServiceNotFound: When the I/O pin service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the I/O pin service is active but there was no way
                to activate the notifications for the PIN data (normally does not occur)
        """
        self._device.notify(Service.IO_PIN, Characteristic.PIN_DATA,
                            lambda sender, data: callback(PinValue.list_from_bytes(self._pin_ad_config, data)))

    def read_data(self) -> List[PinValue]:
        """
        Returns the values for each pin configured as PinIO.INPUT via write_io_configuration.

        Returns:
            A list of input pins and their associated values

        Raises:
            errors.BluetoothServiceNotFound: When the I/O pin service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the I/O pin service is active but there was no way
                to read the pin data (normally does not occur)
        """
        return PinValue.list_from_bytes(self._pin_ad_config, self._device.read(Service.IO_PIN, Characteristic.PIN_DATA))

    def write_data(self, values: List[PinValue]):
        """
        Writes values to 1 or more pins. You must have previously configured these pins as PinIO.OUTPUT pins
        via write_io_configuration. When you write to an input pin it will be ignored

        Args:
            values (List[PinValue]): the output pins and their associated values

        Raises:
            errors.BluetoothServiceNotFound: When the I/O pin service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the I/O pin service is active but there was no way
                to write the pin data (normally does not occur)
        """
        if values:
            self._device.write(Service.IO_PIN, Characteristic.PIN_DATA,
                               PinValue.list_to_bytes(self._pin_ad_config, values))

    def read_ad_configuration(self) -> PinADConfiguration:
        """
        Returns for each pin whether it is configured as a PinAD.DIGITAL or PinAD.ANALOG pin.

        Returns:
            The analog-digital configuration for each pin

        Raises:
            errors.BluetoothServiceNotFound: When the I/O pin service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the I/O pin service is active but there was no way
                to read the pin analog-digital configuration (normally does not occur)
        """
        return PinADConfiguration.from_bytes(self._device.read(Service.IO_PIN, Characteristic.PIN_AD_CONFIGURATION))

    def write_ad_configuration(self, config: PinADConfiguration):
        """
        Configure each pin for analog or digital use.

        Args:
            config (PinADConfiguration): The analog-digital configuration for each pin

        Raises:
            errors.BluetoothServiceNotFound: When the I/O pin service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the I/O pin service is active but there was no way
                to write the analog-digital configuration (normally not present)
        """
        self._device.write(Service.IO_PIN, Characteristic.PIN_AD_CONFIGURATION, config.to_bytes())
        self._pin_ad_config = PinADConfiguration(config[:])

    def read_io_configuration(self) -> PinIOConfiguration:
        """
        Returns for each pin whether it is configured as a PinIO.INPUT or PinIO.OUTPUT pin.

        Returns:
            The input-output configuration for each pin

        Raises:
            errors.BluetoothServiceNotFound: When the I/O pin service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the I/O pin service is active but there was no way
                to read the input-output configuration (normally does not occur)
        """
        return PinIOConfiguration.from_bytes(self._device.read(Service.IO_PIN, Characteristic.PIN_IO_CONFIGURATION))

    def write_io_configuration(self, config: PinIOConfiguration):
        """
        Configure each pin for input or output.
        Only values of pins configured as PinIO.INPUT can be read with read_data,
        and for these pins only you can get updates with notify_data.
        You can write values only to pins configured as PinIO.OUTPUT.

        Args:
            config (PinIOConfiguration): The input-output configuration for each pin

        Raises:
            errors.BluetoothServiceNotFound: When the I/O pin service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the I/O pin service is active but there was no way
                to write the input-output configuration (normally not present)
        """
        self._device.write(Service.IO_PIN, Characteristic.PIN_IO_CONFIGURATION, config.to_bytes())

    def write_pwm_control_data(self, pwm_control1: PwmControlData, pwm_control2: PwmControlData = None):
        """
        Writes Pulse Width Modulation commands to the micro:bit. 1 or 2 assignments can be given at the same time

        See Also: https://microbit-micropython.readthedocs.io/en/latest/pin.html

        See Also: https://www.micro-bit.nl/kennisbank-pinnen

        Args:
            pwm_control1 (PwmControlData): a PWM command
            pwm_control2 (PwmControlData): an optional PWM command

        Raises:
            errors.BluetoothServiceNotFound: When the I/O pin service is not active on the micro:bit
            errors.BluetoothCharacteristicNotFound: When the I/O pin service is active but there was no way
                to write the pwm control data (normally does not occur)
        """
        data = pwm_control1.to_bytes() + pwm_control2.to_bytes() if pwm_control2 else pwm_control1.to_bytes()
        self._device.write(Service.IO_PIN, Characteristic.PWM_CONTROL, data)
