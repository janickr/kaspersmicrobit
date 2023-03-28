#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging

from tkinter import Tk, Canvas
from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.accelerometer import AccelerometerData

logging.basicConfig(level=logging.INFO)

# example {


class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ball:

    def __init__(self, canvas: Canvas, color):
        self.canvas = canvas
        self.position = XY((canvas.winfo_width() / 2) - 5, (canvas.winfo_height() / 2) -5)
        self.direction = XY(0, 0)
        self.id = canvas.create_oval(self.position.x, self.position.y , self.position.x + 10, self.position.y + 10, fill=color)

    def draw(self):
        new_position = XY(self.position.x+self.direction.x, self.position.y+self.direction.y)
        self.position.x = max(0, min(new_position.x, canvas.winfo_width()-10))
        self.position.y = max(0, min(new_position.y, canvas.winfo_height()-10))
        self.canvas.moveto(self.id, new_position.x, self.position.y)


tk = Tk()
tk.title("Use accelerometer to move ball")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=1280, height=720)
canvas.pack()
tk.update()
ball = Ball(canvas, 'blue')


def redraw():
    ball.draw()
    tk.after(10, redraw)


tk.after(10, redraw)


def accelerometer_data(data: AccelerometerData):
    ball.direction.x = data.x / 100
    ball.direction.y = data.y / 100


with KaspersMicrobit.find_one_microbit() as microbit:
    microbit.accelerometer.notify(accelerometer_data)
    tk.mainloop()

# }
