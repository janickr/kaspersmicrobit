#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from tkinter import *
from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.tkinter import do_in_tkinter


MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'
# example {


class Paddle:
    LEFT = -4
    RIGHT = 4

    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.direction = 0
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        pos = self.canvas.coords(self.id)
        self.canvas.move(self.id, self.compute_movement_x(pos[0], pos[2]), 0)

    def compute_movement_x(self, left_edge, right_edge):
        if ((self.direction == Paddle.RIGHT) and (right_edge > self.canvas_width)) or ((self.direction == Paddle.LEFT) and (left_edge < 0)):
            return 0
        return self.direction

    def go_left(self, event):
        self.direction = Paddle.LEFT

    def go_right(self, event):
        self.direction = Paddle.RIGHT

    def stop_going_left(self, event):
        if self.direction == Paddle.LEFT:
            self.direction = 0

    def stop_going_right(self, event):
        if self.direction == Paddle.RIGHT:
            self.direction = 0


tk = Tk()
tk.title("Use buttons to move rectangle")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()
paddle = Paddle(canvas, 'blue')
canvas.bind_all('<KeyPress-Left>', paddle.go_left)
canvas.bind_all('<KeyRelease-Left>', paddle.stop_going_left)
canvas.bind_all('<KeyPress-Right>', paddle.go_right)
canvas.bind_all('<KeyRelease-Right>', paddle.stop_going_right)
canvas.bind_all('<<MICROBIT_BUTTON_PRESS_A>>', paddle.go_left)
canvas.bind_all('<<MICROBIT_BUTTON_RELEASE_A>>', paddle.stop_going_left)
canvas.bind_all('<<MICROBIT_BUTTON_PRESS_B>>', paddle.go_right)
canvas.bind_all('<<MICROBIT_BUTTON_RELEASE_B>>', paddle.stop_going_right)


def redraw():
    paddle.draw()
    tk.after(10, redraw)


tk.after(10, redraw)


def button_pressed(button: str):
    tk.event_generate(f'<<MICROBIT_BUTTON_PRESS_{button.upper()}>>', when='tail')


def button_released(button: str):
    tk.event_generate(f'<<MICROBIT_BUTTON_RELEASE_{button.upper()}>>', when='tail')


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.buttons.on_button_a(press=do_in_tkinter(tk, button_pressed), release=do_in_tkinter(tk, button_released))
    microbit.buttons.on_button_b(press=do_in_tkinter(tk, button_pressed), release=do_in_tkinter(tk, button_released))
    tk.mainloop()
# }
