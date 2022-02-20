from collections import deque
from threading import Event
from typing import Callable, Any


class _Queue:
    def __init__(self):
        self._deque = deque()
        self._active = Event()

    def append(self, e):
        if self._active.is_set():
            self._deque.append(e)

    def offer(self):
        try:
            return self._deque.popleft()
        except IndexError:
            return None

    def set_active(self):
        self._active.set()


def _consume_event(tk, event_queue: _Queue, callback: Callable[[Any], None], delay_in_ms: int):
    e = event_queue.offer()
    while e:
        callback(e)
        e = event_queue.offer()

    tk.after(delay_in_ms, lambda: _consume_event(tk, event_queue, callback, delay_in_ms))


def _start_consuming_events(tk, event_queue: _Queue, callback: Callable[[Any], None], delay_in_ms: int):
    event_queue.set_active()
    tk.after(delay_in_ms, lambda: _consume_event(tk, event_queue, callback, delay_in_ms))


def do_in_tkinter(tk, callback: Callable[[Any], None], delay_in_ms: int = 10):
    queue = _Queue()
    tk.after(delay_in_ms, lambda: _start_consuming_events(tk, queue, callback, delay_in_ms))
    return queue.append
