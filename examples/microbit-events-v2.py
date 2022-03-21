#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import time

import kaspersmicrobit.services.v2_events as v2_events
from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.event import Event

logging.basicConfig(level=logging.INFO)

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'
# example {


def print_events(event: Event):
    print(f"Event occured: {event_to_string(event)}")


def event_to_string(event: Event):
    match event:
        case Event(v2_events.DEVICE_ID_BUTTON_A, v2_events.EVENT_BUTTON_CLICK):
            return "Button A Click"
        case Event(v2_events.DEVICE_ID_GESTURE, v2_events.EVENT_GESTURE_TILT_UP):
            return "Tilt Up"
        case Event(v2_events.DEVICE_ID_GESTURE, v2_events.EVENT_GESTURE_TILT_DOWN):
            return "Tilt Down"
        case Event(v2_events.DEVICE_ID_GESTURE, v2_events.EVENT_GESTURE_TILT_LEFT):
            return "Tilt Left"
        case Event(v2_events.DEVICE_ID_GESTURE, v2_events.EVENT_GESTURE_TILT_RIGHT):
            return "Tilt Right"
        case Event(v2_events.DEVICE_ID_GESTURE, x):
            return f"Some gesture {x}"
        case Event(device, value):
            return f"Unkown {device} {value}"


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    # listen for events / luister naar gebeurtenissen
    microbit.events.notify_microbit_event(print_events)

    # inform the microbit of the events we want to receive
    # / informeer de microbit van de gebeurtenissen waarin we geïnteresseerd zijn
    microbit.events.write_client_requirements(
        # listen to listeners added to the message bus /
        # luister naar het toevoegen van event listeners aan de message bus
        Event(v2_events.DEVICE_ID_MESSAGE_BUS_LISTENER)
    )
    microbit.events.write_client_requirements(
        Event(v2_events.DEVICE_ID_BUTTON_A, v2_events.EVENT_BUTTON_CLICK)  # Button A clicks / Knop A klikken
    )
    microbit.events.write_client_requirements(
        Event(v2_events.DEVICE_ID_GESTURE)  # all gesture events / alle bewegings gebeurtenissen
    )

    print("Tilt your microbit or click button A to receive events")

    time.sleep(15)
# }
