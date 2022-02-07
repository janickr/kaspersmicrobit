#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from tkinter import *
from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.accelerometer import AccelerometerData

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


class Direction():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Bal:
    STOP = Direction(0, 0)
    LEFT = Direction(-4, 0)
    RIGHT = Direction(4, 0)

    def __init__(self, canvas, color):
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        center = self.canvas_width/2
        self.id = canvas.create_oval(center-5, center-5, center+5, center+5, fill=color)
        self.direction = Bal.STOP

    def draw(self):
        pos = self.canvas.coords(self.id)
        self.canvas.move(self.id, self.direction.x, self.direction.y)

    def go(self, direction):
        def eventhandler(event):
            self.direction = direction

        return eventhandler

    def stop(self, direction):
        def eventhandler(event):
            if self.direction == direction:
                self.direction = Bal.STOP

        return eventhandler


def test_move(event):
    print(f'{event}')


tk = Tk()
tk.title("spel")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
tk.update()
bal = Bal(canvas, 'blue')
canvas.bind_all('<KeyPress-Left>', bal.go(Bal.LEFT))
canvas.bind_all('<KeyRelease-Left>', bal.stop(Bal.LEFT))
canvas.bind_all('<KeyPress-Right>', bal.go(Bal.RIGHT))
canvas.bind_all('<KeyRelease-Right>', bal.stop(Bal.RIGHT))
canvas.bind_all('<<MICROBIT_MOVE>>', test_move)


def redraw():
    bal.draw()
    tk.after(10, redraw)


tk.after(10, redraw)


def accelerometer_data(data: AccelerometerData):
    tk.event_generate('<<MICROBIT_MOVE>>', when='tail', data=data)


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.accelerometer.notify(accelerometer_data)
    tk.mainloop()
#