#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections import deque
from threading import Event
from typing import Callable, Any


class _Queue:
    def __init__(self):
        self._deque = deque()
        self._active = Event()

    def append(self, item):
        if self._active.is_set():
            self._deque.append(item)

    def offer(self):
        try:
            return self._deque.popleft()
        except IndexError:
            return None

    def set_active(self):
        self._active.set()


def _consume_event(tk, event_queue: _Queue, callback: Callable[[Any], None], delay_in_ms: int):
    event = event_queue.offer()
    while event:
        callback(event)
        event = event_queue.offer()

    tk.after(delay_in_ms, lambda: _consume_event(tk, event_queue, callback, delay_in_ms))


def _start_consuming_events(tk, event_queue: _Queue, callback: Callable[[Any], None], delay_in_ms: int):
    event_queue.set_active()
    tk.after(delay_in_ms, lambda: _consume_event(tk, event_queue, callback, delay_in_ms))


def do_in_tkinter(tk, callback: Callable[[Any], None], delay_in_ms: int = 10) -> Callable[[Any], None]:
    """
    Use this function to convert a callback to a callback that runs in the thread in which Tk
    is executing. This is to avoid the "main thread is not in main loop" errors that Tk can raise. This will be
    done by having Tk periodically check whether new data has been received (using Tk.after(...))

    Example:
    ```python
    microbit.buttons.on_button_a(press=do_in_tkinter(tk, pressed_callback_that_calls_tk))
    microbit.accelerometer.notify(do_in_tkinter(tk, accelerometer_data_callback_that_calls_tk))
    ```

    Args:
        tk (Tk): your tk root object
        callback (Callable[[Any], None]): the callback function you want to execute on the tk thread
        delay_in_ms (int): the interval at which Tk checks for new data

    Returns (Callable[[Any], None]):
        a new callback function that causes the given callback function to be executed on the Tk thread
    """
    queue = _Queue()
    tk.after(delay_in_ms, lambda: _start_consuming_events(tk, queue, callback, delay_in_ms))
    return queue.append
