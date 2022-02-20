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


def do_in_tkinter(tk, callback: Callable[[Any], None], delay_in_ms: int = 10) -> Callable[[Any], None]:
    """
    Gebruik deze function om een callback om te vormen naar een callback die uitgevoerd wordt in de thread waarin Tk
    uitgevoerd wordt. Dit om de "main thread is not in main loop" fouten die Tk kan geven te vermijden. Dit wordt
    gedaan door Tk periodiek te laten nakijken of er nieuwe data ontvangen is (door middel van Tk.after(...))

    Example:
    ```python
    microbit.buttons.on_button_a(press=do_in_tkinter(tk, pressed_callback_that_calls_tk))
    microbit.accelerometer.notify(do_in_tkinter(tk, accelerometer_data_callback_that_calls_tk))
    ```

    Args:
        tk (Tk): je tk root object
        callback (Callable[[Any], None]): de callback functie die je wil laten uitvoeren op de tk thread
        delay_in_ms (int): het interval waarop Tk nakijkt of er nieuwe data is

    Returns (Callable[[Any], None]):
        een nieuwe callback functie die ervoorzorgt dat de gegeven callback functie laat uitvoeren op de Tk thread
    """
    queue = _Queue()
    tk.after(delay_in_ms, lambda: _start_consuming_events(tk, queue, callback, delay_in_ms))
    return queue.append
