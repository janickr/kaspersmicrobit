#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Callable
from unittest.mock import Mock

import pytest
from kaspersmicrobit.tkinter import do_in_tkinter


class TkStub:
    def __init__(self):
        self.callbacks = []

    def after(self, millis: int, callback: Callable[[], None]):
        self.callbacks.append((millis, callback))

    def simulate_one_main_loop_iteration(self):
        callbacks = self.callbacks
        self.callbacks = []
        for (millis, callback) in callbacks:
            callback()


@pytest.fixture
def tk():
    return TkStub()


@pytest.fixture
def callback():
    return Mock()


def test_calls_will_be_executed_by_tk_main_loop(tk, callback):
    new_callback = do_in_tkinter(tk, callback)

    tk.simulate_one_main_loop_iteration()

    new_callback('some data')

    tk.simulate_one_main_loop_iteration()

    assert callback.call_count == 1


def test_calls_will_not_be_executed_if_tk_main_loop_not_started_yet(tk, callback):
    new_callback = do_in_tkinter(tk, callback)

    new_callback('some data')

    tk.simulate_one_main_loop_iteration()
    tk.simulate_one_main_loop_iteration()

    assert callback.call_count == 0


def test_calls_will_not_be_executed_without_tk_main_loop_iteration(tk, callback):
    new_callback = do_in_tkinter(tk, callback)

    tk.simulate_one_main_loop_iteration()

    new_callback('some data')

    assert callback.call_count == 0


def test_multiple_calls_will_be_executed_in_one_tk_main_loop_iteration(tk, callback):
    new_callback = do_in_tkinter(tk, callback)

    tk.simulate_one_main_loop_iteration()

    new_callback('some data')
    new_callback('some data')
    new_callback('some data')

    tk.simulate_one_main_loop_iteration()

    assert callback.call_count == 3


def test_multiple_calls_will_be_executed_in_multiple_tk_main_loop_iterations(tk, callback):
    new_callback = do_in_tkinter(tk, callback)

    tk.simulate_one_main_loop_iteration()

    new_callback('some data')
    tk.simulate_one_main_loop_iteration()
    new_callback('some data')
    new_callback('some data')
    tk.simulate_one_main_loop_iteration()
    new_callback('some data')
    tk.simulate_one_main_loop_iteration()

    assert callback.call_count == 4
