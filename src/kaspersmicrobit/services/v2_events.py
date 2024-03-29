#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
Device IDs and events ids for micro:bit v2.x
"""

DEVICE_ID_BLE = 1000
EVENT_BLE_CONNECTED = 1
EVENT_BLE_DISCONNECTED = 2

DEVICE_ID_BLE_UART = 1200
EVENT_BLE_UART_DELIM_MATCH = 1
EVENT_BLE_UART_HEAD_MATCH = 2
EVENT_BLE_UART_RX_FULL = 3

# Notify ONE = wake up one fiber (only display), else ALL fibers
DEVICE_ID_NOTIFY_ONE = 1022      # Notification channel, for general purpose synchronisation
EVENT_NOTIFY_ONE_DISPLAY_FREE = 1

DEVICE_ID_NOTIFY = 1023          # Notification channel, for general purpose synchronisation
EVENT_NOTIFY_DISPLAY_FREE = 1
EVENT_NOTIFY_SERIAL_TX_EMPTY = 2
EVENT_NOTIFY_POWER_CANCEL_DEEPSLEEP = 5

DEVICE_ID_ACCELEROMETER = 5
EVENT_ACCELEROMETER_DATA_UPDATE = 1

DEVICE_ID_GESTURE = 13
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
EVENT_GESTURE_2G = 12

DEVICE_ID_BUTTON_A = 1
DEVICE_ID_BUTTON_B = 2
DEVICE_ID_BUTTON_AB = 3
DEVICE_ID_BUTTON_RESET = 4
EVENT_BUTTON_DOWN = 1
EVENT_BUTTON_UP = 2
EVENT_BUTTON_CLICK = 3
EVENT_BUTTON_LONG_CLICK = 4
EVENT_BUTTON_HOLD = 5
EVENT_BUTTON_DOUBLE_CLICK = 6

DEVICE_ID_COMPASS = 6
EVENT_COMPASS_DATA_UPDATE = 1
EVENT_COMPASS_CONFIG_NEEDED = 2
EVENT_COMPASS_CALIBRATE = 3
EVENT_COMPASS_CALIBRATION_NEEDED = 4

DEVICE_ID_DISPLAY = 7
EVENT_DISPLAY_ANIMATION_COMPLETE = 1
EVENT_DISPLAY_LED_MATRIX_LIGHT_SENSE = 2
EVENT_DISPLAY_LED_MATRIX_FRAME_TIMEOUT = 3

_PIN_DEVICE_ID_OFFSET = 100                       # IDs 100-227 are reserved for I/O Pin IDs.
DEVICE_ID_PIN_P0 = (_PIN_DEVICE_ID_OFFSET + 0)
DEVICE_ID_PIN_P1 = (_PIN_DEVICE_ID_OFFSET + 1)
DEVICE_ID_PIN_P2 = (_PIN_DEVICE_ID_OFFSET + 2)
DEVICE_ID_PIN_P3 = (_PIN_DEVICE_ID_OFFSET + 3)
DEVICE_ID_PIN_P4 = (_PIN_DEVICE_ID_OFFSET + 4)
DEVICE_ID_PIN_P5 = (_PIN_DEVICE_ID_OFFSET + 5)
DEVICE_ID_PIN_P6 = (_PIN_DEVICE_ID_OFFSET + 6)
DEVICE_ID_PIN_P7 = (_PIN_DEVICE_ID_OFFSET + 7)
DEVICE_ID_PIN_P8 = (_PIN_DEVICE_ID_OFFSET + 8)
DEVICE_ID_PIN_P9 = (_PIN_DEVICE_ID_OFFSET + 9)
DEVICE_ID_PIN_P10 = (_PIN_DEVICE_ID_OFFSET + 10)
DEVICE_ID_PIN_P11 = (_PIN_DEVICE_ID_OFFSET + 11)
DEVICE_ID_PIN_P12 = (_PIN_DEVICE_ID_OFFSET + 12)
DEVICE_ID_PIN_P13 = (_PIN_DEVICE_ID_OFFSET + 13)
DEVICE_ID_PIN_P14 = (_PIN_DEVICE_ID_OFFSET + 14)
DEVICE_ID_PIN_P15 = (_PIN_DEVICE_ID_OFFSET + 15)
DEVICE_ID_PIN_P16 = (_PIN_DEVICE_ID_OFFSET + 16)
DEVICE_ID_PIN_P17 = (_PIN_DEVICE_ID_OFFSET + 17)
DEVICE_ID_PIN_P18 = (_PIN_DEVICE_ID_OFFSET + 18)
DEVICE_ID_PIN_P19 = (_PIN_DEVICE_ID_OFFSET + 19)
DEVICE_ID_PIN_P20 = (_PIN_DEVICE_ID_OFFSET + 20)
DEVICE_ID_PIN_LOGO = (_PIN_DEVICE_ID_OFFSET + 21)
DEVICE_ID_PIN_SPEAKER = (_PIN_DEVICE_ID_OFFSET + 22)
DEVICE_ID_PIN_RUNMIC = (_PIN_DEVICE_ID_OFFSET + 23)
DEVICE_ID_PIN_SDA = (_PIN_DEVICE_ID_OFFSET + 24)
DEVICE_ID_PIN_SCL = (_PIN_DEVICE_ID_OFFSET + 25)
DEVICE_ID_PIN_ROW1 = (_PIN_DEVICE_ID_OFFSET + 26)
DEVICE_ID_PIN_ROW2 = (_PIN_DEVICE_ID_OFFSET + 27)
DEVICE_ID_PIN_ROW3 = (_PIN_DEVICE_ID_OFFSET + 28)
DEVICE_ID_PIN_ROW4 = (_PIN_DEVICE_ID_OFFSET + 29)
DEVICE_ID_PIN_ROW5 = (_PIN_DEVICE_ID_OFFSET + 30)
DEVICE_ID_PIN_USBTX = (_PIN_DEVICE_ID_OFFSET + 31)
DEVICE_ID_PIN_USBRX = (_PIN_DEVICE_ID_OFFSET + 32)
DEVICE_ID_PIN_IRQ1 = (_PIN_DEVICE_ID_OFFSET + 33)
DEVICE_ID_PIN_MIC = (_PIN_DEVICE_ID_OFFSET + 34)
DEVICE_ID_PIN_P35 = (_PIN_DEVICE_ID_OFFSET + 35)
DEVICE_ID_PIN_P36 = (_PIN_DEVICE_ID_OFFSET + 36)
DEVICE_ID_PIN_P37 = (_PIN_DEVICE_ID_OFFSET + 37)
DEVICE_ID_PIN_P38 = (_PIN_DEVICE_ID_OFFSET + 38)
DEVICE_ID_PIN_P39 = (_PIN_DEVICE_ID_OFFSET + 39)
DEVICE_ID_PIN_P40 = (_PIN_DEVICE_ID_OFFSET + 40)
DEVICE_ID_PIN_P41 = (_PIN_DEVICE_ID_OFFSET + 41)
DEVICE_ID_PIN_P42 = (_PIN_DEVICE_ID_OFFSET + 42)
DEVICE_ID_PIN_P43 = (_PIN_DEVICE_ID_OFFSET + 43)
DEVICE_ID_PIN_P44 = (_PIN_DEVICE_ID_OFFSET + 44)
DEVICE_ID_PIN_P45 = (_PIN_DEVICE_ID_OFFSET + 45)
DEVICE_ID_PIN_P46 = (_PIN_DEVICE_ID_OFFSET + 46)
DEVICE_ID_PIN_P47 = (_PIN_DEVICE_ID_OFFSET + 47)

EVENT_PIN_EVENT_NONE = 0
EVENT_PIN_INTERRUPT_ON_EDGE = 1
EVENT_PIN_EVENT_ON_EDGE = 2
EVENT_PIN_EVENT_ON_PULSE = 3
EVENT_PIN_EVENT_ON_TOUCH = 4

EVENT_DEVICE_PIN_RISE = 2
EVENT_DEVICE_PIN_FALL = 3
EVENT_DEVICE_PIN_PULSE_HI = 4
EVENT_DEVICE_PIN_PULSE_LO = 5

DEVICE_ID_RADIO = 9
EVENT_RADIO_DATAGRAM = 1       # Event to signal that a new datagram has been received.

DEVICE_ID_RADIO_DATA_READY = 10
# protocol if not one of following:
# RADIO_PROTOCOL_DATAGRAM = 1  // A simple, single frame datagram. a little like UDP but with smaller packets. :-)
# RADIO_PROTOCOL_EVENTBUS = 2  // Transparent propogation of events from one micro:bit to another.

DEVICE_ID_MULTIBUTTON_ATTACH = 11

DEVICE_ID_SERIAL = 12
EVENT_SERIAL_DELIM_MATCH = 1
EVENT_SERIAL_HEAD_MATCH = 2
EVENT_SERIAL_RX_FULL = 3
EVENT_SERIAL_DATA_RECEIVED = 4

DEVICE_ID_THERMOMETER = 8
EVENT_THERMOMETER_UPDATE = 1

DEVICE_ID_PARTIAL_FLASHING = 36
EVENT_PARTIAL_FLASHING_FLASH_DATA = 0x01
EVENT_PARTIAL_FLASHING_END_OF_TRANSMISSION = 0x02
EVENT_PARTIAL_FLASHING_RESET = 0xFF

DEVICE_ID_POWER_MANAGER = 37
DEVICE_ID_USB_FLASH_MANAGER = 38
DEVICE_ID_VIRTUAL_SPEAKER_PIN = 39

DEVICE_ID_MBED_INTERRUPT_IN = 40
DEVICE_ID_MBED_PWM = 41
DEVICE_ID_MBED_TIMEOUT = 42
DEVICE_ID_MBED_TICKER = 43

DEVICE_ID_LOG = 44
EVENT_LOG_LOG_FULL = 1

# listen for device ids added to message bus
DEVICE_ID_MESSAGE_BUS_LISTENER = 1021  # Message bus indication that a handler for a given ID has been registered.
