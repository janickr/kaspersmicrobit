#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum
from tkinter import *
from kaspersmicrobit import KaspersMicrobit

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


class Paddle:
    class Direction(Enum):
        LEFT = -1
        STOP = 0
        RIGHT = 1

    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.direction = Paddle.Direction.STOP
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.go(Paddle.Direction.LEFT))
        self.canvas.bind_all('<KeyRelease-Left>', self.stop(Paddle.Direction.LEFT))
        self.canvas.bind_all('<KeyPress-Right>', self.go(Paddle.Direction.RIGHT))
        self.canvas.bind_all('<KeyRelease-Right>', self.stop(Paddle.Direction.RIGHT))
        self.canvas.bind_all('<<MICROBIT_BUTTON_PRESS_A>>', self.go(Paddle.Direction.LEFT))
        self.canvas.bind_all('<<MICROBIT_BUTTON_RELEASE_A>>', self.stop(Paddle.Direction.LEFT))
        self.canvas.bind_all('<<MICROBIT_BUTTON_PRESS_B>>', self.go(Paddle.Direction.RIGHT))
        self.canvas.bind_all('<<MICROBIT_BUTTON_RELEASE_B>>', self.stop(Paddle.Direction.RIGHT))

    def draw(self):
        pos = self.canvas.coords(self.id)
        self.canvas.move(self.id, self.compute_displacement(pos[0], pos[2]), 0)

    def compute_displacement(self, left_edge, right_edge):
        if (self.direction == Paddle.Direction.RIGHT) and (right_edge <= self.canvas_width):
            return 4
        elif (self.direction == Paddle.Direction.LEFT) and (left_edge >= 0):
            return -4
        return 0

    def go(self, direction):
        def eventhandler(event):
            self.direction = direction

        return eventhandler

    def stop(self, direction):
        def eventhandler(event):
            if self.direction == direction:
                self.direction = Paddle.Direction.STOP

        return eventhandler


tk = Tk()
tk.title("spel")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()
paddle = Paddle(canvas, 'blue')


def redraw():
    paddle.draw()
    tk.after(10, redraw)


tk.after(10, redraw)


def button_pressed(button: str):
    tk.event_generate(f'<<MICROBIT_BUTTON_PRESS_{button.upper()}>>', when='tail')


def button_released(button: str):
    tk.event_generate(f'<<MICROBIT_BUTTON_RELEASE_{button.upper()}>>', when='tail')


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.buttons.on_button_a(press=button_pressed, up=button_released)
    microbit.buttons.on_button_b(press=button_pressed, up=button_released)
    tk.mainloop()
