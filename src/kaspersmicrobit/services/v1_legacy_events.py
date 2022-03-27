#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
Device IDs and events ids for outdated firmware versions (Microbit v1)
"""

DEVICE_ID_BLE = 1000
EVENT_BLE_CONNECTED = 1
EVENT_BLE_DISCONNECTED = 2

DEVICE_ID_BLE_UART = 1200
EVENT_BLE_UART_DELIM_MATCH = 1
EVENT_BLE_UART_HEAD_MATCH = 2
EVENT_BLE_UART_RX_FULL = 3

# Notify ONE = wake up one fiber (only display), else ALL fibers
DEVICE_ID_NOTIFY_ONE = 1022          # Notification channel, for general purpose synchronisation
EVENT_NOTIFY_ONE_DISPLAY_FREE = 1

DEVICE_ID_NOTIFY = 1023          # Notification channel, for general purpose synchronisation
EVENT_NOTIFY_DISPLAY_FREE = 1
EVENT_NOTIFY_SERIAL_TX_EMPTY = 2
EVENT_NOTIFY_UART_TX_EMPTY = 3

DEVICE_ID_ACCELEROMETER = 4
EVENT_ACCELEROMETER_DATA_UPDATE = 1

DEVICE_ID_GESTURE = 27
EVENT_GESTURE_NONE = 0
EVENT_GESTURE_TILT_UP = 1
EVENT_GESTURE_TILT_DOWN = 2
EVENT_GESTURE_TILT_LEFT = 3
EVENT_GESTURE_TILT_RIGHT = 4
EVENT_GESTURE_FACE_UP = 5
EVENT_GESTURE_FACE_DOWN = 6
EVENT_GESTURE_FREEFALL = 7
EVENT_GESTURE_3G = 8
EVENT_GESTURE_6G = 9
EVENT_GESTURE_8G = 10
EVENT_GESTURE_SHAKE = 11

DEVICE_ID_BUTTON_A = 1
DEVICE_ID_BUTTON_B = 2
DEVICE_ID_BUTTON_AB = 26    # Button A+B multibutton
DEVICE_ID_BUTTON_RESET = 3  # don't know if reset does anything

EVENT_BUTTON_DOWN = 1
EVENT_BUTTON_UP = 2
EVENT_BUTTON_CLICK = 3
EVENT_BUTTON_LONG_CLICK = 4
EVENT_BUTTON_HOLD = 5
EVENT_BUTTON_DOUBLE_CLICK = 6  # don't know if AB handles this

DEVICE_ID_COMPASS = 5
EVENT_COMPASS_DATA_UPDATE = 1
EVENT_COMPASS_CONFIG_NEEDED = 2
EVENT_COMPASS_CALIBRATE = 3
EVENT_COMPASS_CALIBRATION_NEEDED = 4

DEVICE_ID_DISPLAY = 6
EVENT_DISPLAY_ANIMATION_COMPLETE = 1
EVENT_DISPLAY_LIGHT_SENSE = 2

DEVICE_ID_IO_P0 = 7           # P0 is the left most pad (ANALOG/DIGITAL)
DEVICE_ID_IO_P1 = 8           # P1 is the middle pad (ANALOG/DIGITAL)
DEVICE_ID_IO_P2 = 9           # P2 is the right most pad (ANALOG/DIGITAL)
DEVICE_ID_IO_P3 = 10          # COL1 (ANALOG/DIGITAL)
DEVICE_ID_IO_P4 = 11          # BTN_A
DEVICE_ID_IO_P5 = 12          # COL2 (ANALOG/DIGITAL)
DEVICE_ID_IO_P6 = 13          # ROW2
DEVICE_ID_IO_P7 = 14          # ROW1
DEVICE_ID_IO_P8 = 15          # PIN 18
DEVICE_ID_IO_P9 = 16          # ROW3
DEVICE_ID_IO_P10 = 17          # COL3 (ANALOG/DIGITAL)
DEVICE_ID_IO_P11 = 18          # BTN_B
DEVICE_ID_IO_P12 = 19          # PIN 20
DEVICE_ID_IO_P13 = 20          # SCK
DEVICE_ID_IO_P14 = 21          # MISO
DEVICE_ID_IO_P15 = 22          # MOSI
DEVICE_ID_IO_P16 = 23          # PIN 16
DEVICE_ID_IO_P19 = 24          # SCL
DEVICE_ID_IO_P20 = 25          # SDA

DEVICE_ID_IO_INT1 = 33          # INT1
DEVICE_ID_IO_INT2 = 34          # INT2
DEVICE_ID_IO_INT3 = 35          # INT3

EVENT_PIN_EVENT_NONE = 0
EVENT_PIN_EVENT_ON_EDGE = 1
EVENT_PIN_EVENT_ON_PULSE = 2
EVENT_PIN_EVENT_ON_TOUCH = 3

EVENT_PIN_RISE = 2
EVENT_PIN_FALL = 3
EVENT_PIN_PULSE_HI = 4
EVENT_PIN_PULSE_LO = 5

DEVICE_ID_RADIO = 29
EVENT_RADIO_DATAGRAM = 1       # Event to signal that a new datagram has been received.

DEVICE_ID_RADIO_DATA_READY = 30
# protocol if not one of following:
# RADIO_PROTOCOL_DATAGRAM = 1  // A simple, single frame datagram. a little like UDP but with smaller packets. :-)
# RADIO_PROTOCOL_EVENTBUS = 2  // Transparent propogation of events from one micro:bit to another.

DEVICE_ID_SERIAL = 32
EVENT_SERIAL_DELIM_MATCH = 1
EVENT_SERIAL_HEAD_MATCH = 2
EVENT_SERIAL_RX_FULL = 3

DEVICE_ID_THERMOMETER = 28
EVENT_THERMOMETER_UPDATE = 1

DEVICE_ID_PARTIAL_FLASHING = 36
EVENT_PARTIAL_FLASHING_FLASH_DATA = 0x01
EVENT_PARTIAL_FLASHING_END_OF_TRANSMISSION = 0x02
EVENT_PARTIAL_FLASHING_RESET = 0xFF

# listen for device ids added to message bus
DEVICE_ID_MESSAGE_BUS_LISTENER = 1021  # Message bus indication that a handler for a given ID has been registered.
