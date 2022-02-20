#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from tkinter import Tk, Canvas
from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.accelerometer import AccelerometerData

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'
# example {


class Direction:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ball:

    def __init__(self, canvas, color):
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        center = self.canvas_width/2
        self.id = canvas.create_oval(center-5, center-5, center+5, center+5, fill=color)
        self.direction = Direction(0, 0)

    def draw(self):
        pos = self.canvas.coords(self.id)
        movement = self.compute_movement(pos[0], pos[2], pos[1], pos[3])
        self.canvas.move(self.id, movement.x, movement.y)

    def compute_movement(self, left_edge, right_edge, top, bottom):
        x = self.direction.x
        y = self.direction.y

        if self.direction.x < 0 and left_edge < 0:
            x = 5
        if self.direction.x > 0 and right_edge > self.canvas_width:
            x = -5
        if self.direction.y < 0 and top < 0:
            y = 5
        if self.direction.y > 0 and bottom > self.canvas_width:
            y = -5

        return Direction(x, y)


tk = Tk()
tk.title("Use accelerometer to move ball")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=500)
canvas.pack()
tk.update()
ball = Ball(canvas, 'blue')


def redraw():
    ball.draw()
    tk.after(10, redraw)


tk.after(10, redraw)


def accelerometer_data(data: AccelerometerData):
    ball.direction = Direction(data.x / 250, data.y / 250)


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.accelerometer.notify(tk, accelerometer_data)
    tk.mainloop()
# }
