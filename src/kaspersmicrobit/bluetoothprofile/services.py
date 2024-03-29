#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum


# flake8: noqa
class Service(Enum):
    """
    Lists all services that could be offered by the micro:bit

    See Also: https://lancaster-university.github.io/microbit-docs/resources/bluetooth/bluetooth_profile.html
    """

    GENERIC_ACCESS = '00001800-0000-1000-8000-00805f9b34fb'
    """
    The generic_access service contains generic information about the device.
    All available Characteristics are readonly.
    """

    GENERIC_ATTRIBUTE = '00001801-0000-1000-8000-00805f9b34fb'
    """
    """

    DEVICE_INFORMATION = '0000180a-0000-1000-8000-00805f9b34fb'
    """
    The Device Information Service exposes manufacturer and/or vendor information about a device.            
    
    This service exposes manufacturer information about a device.
    The Device Information Service is instantiated as a Primary Service.
    Only one instance of the Device Information Service is exposed on a device.
    """

    ACCELEROMETER = 'e95d0753-251d-470a-a062-fa1922dfa9a8'
    """
    Exposes accelerometer data. An accelerometer is an electromechanical device that will measure acceleration forces. 
    These forces may be static, like the constant force of gravity pulling at your feet, or they could be dynamic 
    - caused by moving or vibrating the accelerometer.

    Value contains fields which represent 3 separate accelerometer measurements for X, Y and Z axes 
    as 3 unsigned 16 bit values in that order and in little endian format. 

    Data can be read on demand or notified periodically.
    """

    MAGNETOMETER = 'e95df2d8-251d-470a-a062-fa1922dfa9a8'
    """
    Exposes magnetometer data.  A magnetometer measures a magnetic field such as the earth's magnetic field in 3 axes.
    """

    BUTTON = 'e95d9882-251d-470a-a062-fa1922dfa9a8'
    """
    Exposes the two Micro Bit buttons and allows 'commands' associated with button state changes to be associated 
    with button states and notified to a connected client.
    """

    IO_PIN = 'e95d127b-251d-470a-a062-fa1922dfa9a8'
    """
    Provides read/write access to I/O pins, individually or collectively. Allows configuration of each pin for 
    input/output and analogue/digital use.
    """

    LED = 'e95dd91d-251d-470a-a062-fa1922dfa9a8'
    """
    Provides access to and control of LED state. 
    Allows the state (ON or OFF) of all 25 LEDs to be set in a single write operation. 
    Allows short text strings to be sent by a client for display on the LED matrix and scrolled across at a speed 
    controlled by the Scrolling Delay characteristic.
    """

    EVENT = 'e95d93af-251d-470a-a062-fa1922dfa9a8'
    """
    A generic, bi-directional event communication service. 

    The Event Service allows events or commands to be notified to the micro:bit by a connected client and it allows 
    micro:bit to notify the connected client of events or commands originating from with the micro:bit. The micro:bit 
    can inform the client of the types of event it is interested in being informed about (e.g. an incoming call) and 
    the client can inform the micro:bit of types of event it wants to be notified about.  
    
    The term "event" will be used here for both event and command types of data.
    
    Events may have an associated value.
    
    Note that specific event ID values including any special values such as those which may represent wild cards are 
    not defined here. The micro:bit run time documentation should be consulted for this information.
    
    Multiple events of different types may be notified to the client or micro:bit at the same time.
    Event data is encoded as an array of structs each encoding an event of a given type together with an associated 
    value. Event Type and Event Value are both defined as uint16 and therefore the length of this array will always be 
    a multiple of 4.
    
        struct event {
         uint16 event_type;
         uint16 event_value;
        };

    """

    DFU_CONTROL = 'e95d93b0-251d-470a-a062-fa1922dfa9a8'
    """
    Allows clients to initiate the micro:bit pairing and over the air firmware update procedures.
    """

    TEMPERATURE = 'e95d6100-251d-470a-a062-fa1922dfa9a8'
    """
    Ambient temperature derived from several internal temperature sensors on the micro:bit
    """

    UART = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
    """
    This is an implementation of Nordic Semiconductor's UART/Serial Port Emulation over Bluetooth low energy. 

    See https://developer.nordicsemi.com/nRF5_SDK/nRF51_SDK_v8.x.x/doc/8.0.0/s110/html/a00072.html for the original 
    Nordic Semiconductor documentation by way of background.
    """

    @staticmethod
    def lookup(uuid: str):
        """
        Looks up the enum corresponding the given uuid

        Returns (Service):
            The enum with the given uuid, None if not found.
        """
        try:
            return Service(uuid)
        except ValueError:
            return None
