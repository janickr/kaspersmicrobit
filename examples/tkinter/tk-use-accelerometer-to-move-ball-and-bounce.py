#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from tkinter import Tk, Canvas
from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.accelerometer import AccelerometerData

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


class Direction:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Direction(self.x + other.x, self.y + other.y)

    def __mul__(self, other: float):
        return Direction(self.x * other, self.y * other)


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
        if left_edge <= 0 or right_edge > self.canvas_width:
            self.direction = Direction(-self.direction.x, self.direction.y)
        elif top < 0 or bottom > self.canvas_width:
            self.direction = Direction(self.direction.x, -self.direction.y)

        return self.direction


tk = Tk()
tk.title("Use accelerometer to move ball an bounce")
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
    ball.direction = ball.direction * 0.98 + Direction(data.x, data.y) * 0.0004


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.accelerometer.notify(accelerometer_data)
    tk.mainloop()
