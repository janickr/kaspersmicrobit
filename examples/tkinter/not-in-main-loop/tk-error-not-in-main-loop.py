#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import time
from tkinter import Tk, Canvas
from kaspersmicrobit import KaspersMicrobit
from dot import Dot

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


tk = Tk()
tk.title("Example: error in main loop")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

dot_a = Dot(canvas, 100, 200, 'blue')
dot_b = Dot(canvas, 400, 200, 'red')

canvas.bind_all('<<MICROBIT_BUTTON_PRESS_A>>', dot_a.show)
canvas.bind_all('<<MICROBIT_BUTTON_RELEASE_A>>', dot_a.hide)
canvas.bind_all('<<MICROBIT_BUTTON_PRESS_B>>', dot_b.show)
canvas.bind_all('<<MICROBIT_BUTTON_RELEASE_B>>', dot_b.hide)


def redraw():
    dot_a.draw()
    dot_b.draw()
    tk.after(10, redraw)


tk.after(10, redraw)


def button_pressed(button: str):
    tk.event_generate(f'<<MICROBIT_BUTTON_PRESS_{button.upper()}>>', when='tail')


def button_released(button: str):
    tk.event_generate(f'<<MICROBIT_BUTTON_RELEASE_{button.upper()}>>', when='tail')


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.buttons.on_button_a(press=button_pressed, release=button_released)
    microbit.buttons.on_button_b(press=button_pressed, release=button_released)

    print("if you push button A or B now you'll get the not in main loop error")
    time.sleep(5)
    print("if you push button A or B now you will see dots appearing on the canvas")

    tk.mainloop()
