#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from kaspersmicrobit.services.event import Event
import kaspersmicrobit.services.v1_events as v1_events


class TestEvent:
    def test_to_bytes(self):
        event = Event(v1_events.DEVICE_ID_GESTURE, v1_events.EVENT_GESTURE_3G)
        assert event.to_bytes() == bytearray.fromhex("0d 00 08 00")

    def test_from_bytes(self):
        event = Event(v1_events.DEVICE_ID_GESTURE, v1_events.EVENT_GESTURE_3G)
        assert Event.from_bytes(bytearray.fromhex("0d 00 08 00")) == event

    def test_list_to_bytes(self):
        events = [
            Event(v1_events.DEVICE_ID_GESTURE, v1_events.EVENT_GESTURE_3G),
            Event(v1_events.DEVICE_ID_DISPLAY, v1_events.EVENT_DISPLAY_ANIMATION_COMPLETE)
        ]
        assert Event.list_to_bytes(events) == bytearray.fromhex("0d 00 08 00 07 00 01 00")

    def test_list_from_bytes(self):
        events = [
            Event(v1_events.DEVICE_ID_GESTURE, v1_events.EVENT_GESTURE_3G),
            Event(v1_events.DEVICE_ID_DISPLAY, v1_events.EVENT_DISPLAY_ANIMATION_COMPLETE)
        ]
        assert Event.list_from_bytes(bytearray.fromhex("0d 00 08 00 07 00 01 00")) == events
