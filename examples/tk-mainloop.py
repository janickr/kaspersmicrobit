#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from tkinter import *
from kaspersmicrobit import KaspersMicrobit

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<<MICROBIT_BUTTON_A>>', self.turn_left)
        self.canvas.bind_all('<<MICROBIT_BUTTON_B>>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -4

    def turn_right(self, evt):
        self.x = 4


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


def button_a(sender, data):
    tk.event_generate('<<MICROBIT_BUTTON_A>>', when='tail')


def button_b(sender, data):
    tk.event_generate('<<MICROBIT_BUTTON_B>>', when='tail')


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit1:
    microbit1.notify(Characteristic.BUTTON_A, button_a)
    microbit1.notify(Characteristic.BUTTON_B, button_b)
    tk.mainloop()
