#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

# flake8: noqa
class Characteristic(Enum):
    """
    Lists all characteristics in the micro:bit GATT profile

    See Also: https://lancaster-university.github.io/microbit-docs/resources/bluetooth/bluetooth_profile.html
    """

    DEVICE_NAME = '00002a00-0000-1000-8000-00805f9b34fb'
    """
    Read Mandatory
    
    Write Mandatory
    
    Fields
    
    1. Name : utf8s
    """

    APPEARANCE = '00002a01-0000-1000-8000-00805f9b34fb'
    """
    The external appearance of this device. The values are composed of a category (10-bits) and sub-categories (6-bits).
    
    Read Mandatory
    
    Fields
    
    1. Category : 16bit
    """

    PERIPHERAL_PREFERRED_CONNECTION_PARAMETERS = '00002a04-0000-1000-8000-00805f9b34fb'
    """
    Read Mandatory
    
    Fields
    
    1. Minimum Connection Interval : uint16
    2. Maximum Connection Interval : uint16
    3. Slave Latency : uint16
    4. Connection Supervision Timeout Multiplier : uint16
    """

    SERVICE_CHANGED = '2a05'
    """
    Indicate Mandatory
    
    Fields
    
    1. Start of Affected Attribute Handle Range : uint16
    2. End of Affected Attribute Handle Range : uint16
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    MODEL_NUMBER_STRING = '00002a24-0000-1000-8000-00805f9b34fb'
    """
    The value of this characteristic is a UTF-8 string representing the model number assigned by the device vendor.
    
    Read Mandatory
    
    Fields
    
    1. Model Number : utf8s
    """

    SERIAL_NUMBER_STRING = '00002a25-0000-1000-8000-00805f9b34fb'
    """
    The value of this characteristic is a variable-length UTF-8 string representing the serial number for a particular
    instance of the device.
    
    Read Mandatory
    
    Fields
    
    1. Serial Number : utf8s
    """

    HARDWARE_REVISION_STRING = '00002a27-0000-1000-8000-00805f9b34fb'
    """
    The value of this characteristic is a UTF-8 string representing the hardware revision for the hardware within 
    the device.
    
    Read Mandatory
    
    Fields
    
    1. Hardware Revision : utf8s
    """

    FIRMWARE_REVISION_STRING = '00002a26-0000-1000-8000-00805f9b34fb'
    """
    The value of this characteristic is a UTF-8 string representing the firmware revision for the firmware within 
    the device.
    
    Read Mandatory
    
    Fields
    
    1. Firmware Revision : utf8s
    """

    MANUFACTURER_NAME_STRING = '00002a29-0000-1000-8000-00805f9b34fb'
    """
    The value of this characteristic is a UTF-8 string representing the name of the manufacturer of the device.  
    
    Read Mandatory
    
    Fields
    
    1. Manufacturer Name : utf8s    
    """

    ACCELEROMETER_DATA = 'e95dca4b-251d-470a-a062-fa1922dfa9a8'
    """
    Contains accelerometer measurements for X, Y and Z axes as 3 signed 16 bit values in that order and in little 
    endian format. X, Y and Z values should be divided by 1000.
    
    Read Mandatory
    
    Notify Mandatory
    
    Fields
    
    1. Accelerometer_X  : sint16
    2. Accelerometer_Y : sint16
    3. Accelerometer_Z : sint16
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    ACCELEROMETER_PERIOD = 'e95dfb24-251d-470a-a062-fa1922dfa9a8'
    """
    Determines the frequency with which accelerometer data is reported in milliseconds.
    Valid values are 1, 2, 5, 10, 20, 80, 160 and 640.
    
    Read Mandatory
    
    Write Mandatory
    
    Fields
    
    1. Accelerometer_Period : uint16
    """

    MAGNETOMETER_DATA = 'e95dfb11-251d-470a-a062-fa1922dfa9a8'
    """
    Contains magnetometer measurements for X, Y and Z axes as 3 signed 16 bit values in that order and in little endian 
    format. Data can be read on demand or notified periodically.
    
    Read Mandatory
    
    Notify Mandatory
    
    Fields
    
    1. Magnetometer_X : sint16
    2. Magnetometer_Y : sint16
    3. Magnetometer_Z : sint16
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    MAGNETOMETER_PERIOD = 'e95d386c-251d-470a-a062-fa1922dfa9a8'
    """
    Determines the frequency with which magnetometer data is reported in milliseconds.
    Valid values are 1, 2, 5, 10, 20, 80, 160 and 640.
    
    Read Mandatory
    
    Write Mandatory
    
    Fields
    
    1. Magnetometer_Period : uint16
    """

    MAGNETOMETER_BEARING = 'e95d9715-251d-470a-a062-fa1922dfa9a8'
    """
    Compass bearing in degrees from North.
    
    Read Mandatory
    
    Notify Mandatory
    
    Fields
    
    1. bearing value : uint16
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    MAGNETOMETER_CALIBRATION = 'e95db358-251d-470a-a062-fa1922dfa9a8'
    """
    Write Mandatory
    
    Notify Mandatory
    
    Fields
    
    1. calibration field : uint8
    
    
            0 - state unknown
            1 - calibration requested
            2 - calibration completed OK
            3 - calibration completed with error
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    BUTTON_A = 'e95dda90-251d-470a-a062-fa1922dfa9a8'
    """
    State of Button A may be read on demand by a connected client or the client may subscribe to notifications of 
    state change. 3 button states are defined and represented by a simple numeric enumeration: 
    
            0 = not pressed
            1 = pressed
            2 = long press.
    
    Read Mandatory
    
    Notify Mandatory
    
    Fields
    
    1. Button_State_Value : uint8
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    BUTTON_B = 'e95dda91-251d-470a-a062-fa1922dfa9a8'
    """
    State of Button B may be read on demand by a connected client or the client may subscribe to notifications of 
    state change. 3 button states are defined and represented by a simple numeric enumeration:  
    
            0 = not pressed
            1 = pressed
            2 = long press.
    
    Read Mandatory
    
    Notify Mandatory
    
    Fields
    
    1. Button_State_Value : uint8
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    PIN_DATA = 'e95d8d00-251d-470a-a062-fa1922dfa9a8'
    """
    Contains data relating to zero or more pins. Structured as a variable length array of up to 
    19 Pin Number / Value pairs. 

    Pin Number and Value are each uint8 fields. 
    Note however that the micro:bit has a 10 bit ADC and so values are compressed to 8 bits with a loss of resolution.

    OPERATIONS:

    WRITE: Clients may write values to one or more pins in a single GATT write operation. 
    A pin to which a value is to be written must have been configured for output using the Pin IO Configuration 
    characteristic. Any attempt to write to a pin which is configured for input will be ignored.

    NOTIFY: Notifications will deliver Pin Number / Value pairs for those pins defined as input pins by the Pin IO 
    Configuration characteristic and whose value when read differs from the last read of the pin.

    READ: A client reading this characteristic will receive Pin Number / Value pairs for all those pins defined as 
    input pins by the Pin IO Configuration characteristic.
    
    Read Mandatory
    
    Write Mandatory
    
    Notify Mandatory
    
    Fields
    
    1. IO_Pin_Data : uint8[]
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    PIN_AD_CONFIGURATION = 'e95d5899-251d-470a-a062-fa1922dfa9a8'
    """
    A bit mask which allows each pin to be configured for analogue or digital use.

    Bit n corresponds to pin n where 0 LESS THAN OR EQUAL TO n LESS THAN 19. 
    A value of 0 means digital and 1 means analogue.
    
    Read Mandatory
    
    Write Mandatory
    
    Fields
    
    1. Pin_AD_Config_Value : uint32
    """

    PIN_IO_CONFIGURATION = 'e95db9fe-251d-470a-a062-fa1922dfa9a8'
    """
    A bit mask (32 bit) which defines which inputs will be read. If the Pin AD Configuration bit mask is also set the 
    pin will be read as an analogue input, if not it will be read as a digital input.  

    Note that in practice, setting a pin's mask bit means that it will be read by the micro:bit runtime and, if 
    notifications have been enabled on the Pin Data characteristic, data read will be transmitted to the connected 
    Bluetooth peer device in a Pin Data notification. If the pin's bit is clear, it  simply means that it will not be 
    read by the micro:bit runtime.

    Bit n corresponds to pin n where 0 LESS THAN OR EQUAL TO n LESS THAN 19. A value of 0 means configured for output 
    and 1 means configured for input.
    
    Read Mandatory
    
    Write Mandatory
    
    Fields
    
    1. Pin_IO_Config_Value : uint32
    """

    PWM_CONTROL = 'e95dd822-251d-470a-a062-fa1922dfa9a8'
    """
    A variable length array 1 to 2 instances of :
     
        struct PwmControlData {
         uint8_t     pin;
         uint16_t    value;
         uint32_t    period;
        }
    
    Period is in microseconds and is an unsigned int but transmitted.
    Value is in the range 0 – 1024, per the current DAL API (e.g. setAnalogValue). 0 means OFF.
    
    Fields are transmitted over the air in Little Endian format.
    
        
    Write Mandatory
    
    Fields
    
    1. PWM Control Field : uint8[]
    """

    LED_MATRIX_STATE = 'e95d7b77-251d-470a-a062-fa1922dfa9a8'
    """
    Allows the state of any|all LEDs in the 5x5 grid to be set to on or off with a single GATT operation. 
    Consists of an array of 5 x utf8 octets, each representing one row of 5 LEDs.  
    Octet 0 represents the first row of LEDs i.e. the top row when the micro:bit is viewed with the edge connector at 
    the bottom and USB connector at the top. 
    Octet 1 represents the second row and so on.
    In each octet, bit 4 corresponds to the first LED in the row, bit 3 the second and so on. 
    Bit values represent the state of the related LED: off (0) or on (1).
    
    So we have:
    
        Octet 0, LED Row 1: bit4 bit3 bit2 bit1 bit0
        Octet 1, LED Row 2: bit4 bit3 bit2 bit1 bit0
        Octet 2, LED Row 3: bit4 bit3 bit2 bit1 bit0
        Octet 3, LED Row 4: bit4 bit3 bit2 bit1 bit0
        Octet 4, LED Row 5: bit4 bit3 bit2 bit1 bit0

    
    Read Mandatory
    
    Write Mandatory
    
    Fields
    
    1. LED_Matrix_State : uint8[]
    """

    LED_TEXT = 'e95d93ee-251d-470a-a062-fa1922dfa9a8'
    """
    A short UTF-8 string to be shown on the LED display. Maximum length 20 octets.
    
    Write Mandatory
    
    Fields
    
    1. LED_Text_Value : utf8s
    """

    SCROLLING_DELAY = 'e95d0d2d-251d-470a-a062-fa1922dfa9a8'
    """
    Specifies a millisecond delay to wait for in between showing each character on the display.
    
    Read Mandatory
    
    Write Mandatory
    
    Fields
    
    1. Scrolling_Delay_Value : uint16
    """

    MICROBIT_REQUIREMENTS = 'e95db84c-251d-470a-a062-fa1922dfa9a8'
    """
    A variable length list of event data structures which indicates the types of client event, potentially with a 
    specific value which the micro:bit wishes to be informed of when they occur. The client should read this 
    characteristic when it first connects to the micro:bit. It may also subscribe to notifications
    to that it can be informed if the value of this characteristic is changed by the micro:bit firmware.
    
        struct event {
          uint16 event_type;
          uint16 event_value;
        };
    
    Note that an event_type of zero means ANY event type and an event_value part set to zero means ANY event value.
    
    event_type and event_value are each encoded in little endian format.
    
    Read Mandatory
    
    Notify Mandatory
    
    Fields
    
    1. microbit_reqs_value : uint8[]
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    MICROBIT_EVENT = 'e95d9775-251d-470a-a062-fa1922dfa9a8'
    """
    Contains one or more event structures which should be notified to the client. It supports notifications and as 
    such the client should subscribe to notifications from this characteristic.
    
        struct event {
          uint16 event_type;
          uint16 event_value;
        };
        
    
    Read Mandatory
    
    Notify Mandatory
    
    Fields
    
    1. Event_Type_And_Value : uint8[]
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    CLIENT_REQUIREMENTS = 'e95d23c4-251d-470a-a062-fa1922dfa9a8'
    """
    a variable length list of event data structures which indicates the types of micro:bit event, potentially with a 
    specific value which the client wishes to be informed of when they occur. The client should write to this 
    characteristic when it first connects to the micro:bit.
    
        struct event {
          uint16 event_type;
          uint16 event_value;
        };
        
    
    Note that an event_type of zero means ANY event type and an event_value part set to zero means ANY event value.
    
    event_type and event_value are each encoded in little endian format.

    Write Mandatory
    
    Fields
    
    1. Client_Requirements_Value : uint8[]
    
    """

    CLIENT_EVENT = 'e95d5404-251d-470a-a062-fa1922dfa9a8'
    """
    a writable characteristic which the client may write one or more event structures to, to inform the micro:bit of 
    events which have occurred on the client. These should be of types indicated in the micro:bit Requirements 
    characteristic bit mask.
    
        struct event {
          uint16 event_type;
          uint16 event_value;
        };
    
    Write Mandatory
    
    Write Without Response Mandatory
    
    Fields
    
    1. Event_Types_And_Values : uint8[]
    
    """

    DFU_CONTROL = 'e95d93b1-251d-470a-a062-fa1922dfa9a8'
    """
    Writing 0x01 initiates rebooting the micro:bit into the Nordic Semiconductor bootloader if the DFU Flash Code 
    characteristic has been written to with the correct secret key. 

    Writing 0x02 to this characteristic  means "request flash code".
    
    Read Mandatory
    
    Write Mandatory
    
    Fields
    
    1. dfu_control : uint8
    """

    TEMPERATURE = 'e95d9250-251d-470a-a062-fa1922dfa9a8'
    """
    Signed integer 8 bit value in degrees celsius.
    
    Read Mandatory
    
    Notify Mandatory
    
    Fields
    
    1. temperature value : sint8
    
    Descriptors
    
    1. Client Characteristic Configuration : 2902
    """

    TEMPERATURE_PERIOD = 'e95d1b25-251d-470a-a062-fa1922dfa9a8'
    """
    Determines the frequency with which temperature data is updated in milliseconds.
    
    Read Mandatory
    
    Write Mandatory
    
    Fields
    
    1. temperature period value : uint16
    """

    TX_CHARACTERISTIC = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
    """
    This characteristic allows the micro:bit to transmit a byte array containing an arbitrary number of arbitrary 
    octet values to a connected device. 

    The maximum number of bytes which may be transmitted in one PDU is limited to the MTU minus three or 20 octets 
    to be precise.

    Indicate Mandatory
    
    Fields
    
    1. UART TX Field : uint8[]
    """

    RX_CHARACTERISTIC = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
    """
    This characteristic allows a connected client to send a byte array containing an arbitrary number of arbitrary 
    octet values to a connected micro:bit. 

    The maximum number of bytes which may be transmitted in one PDU is limited to the MTU minus three or 20 octets 
    to be precise.
    
    
    Write Mandatory
    
    Write Without Response Mandatory
    
    Fields
    
    1. UART TX Field : uint8[]
    """

    @staticmethod
    def lookup(uuid: str):
        """
        Looks up the enum corresponding the given uuid

        Returns (Characteristic):
            The enum with the given uuid, None if not found.
        """
        try:
            return Characteristic(uuid)
        except ValueError:
            return None
