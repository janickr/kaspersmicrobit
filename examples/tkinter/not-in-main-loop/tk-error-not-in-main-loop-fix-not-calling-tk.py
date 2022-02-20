#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import time
from tkinter import Tk, Canvas
from src.kaspersmicrobit import KaspersMicrobit
from dot import Dot

MICROBIT_BLUETOOTH_ADDRESS = 'E3:7E:99:0D:C1:BA'


tk = Tk()
tk.title("Example: error in main loop - fix without calling tk")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

dot_a = Dot(canvas, 100, 200, 'blue')
dot_b = Dot(canvas, 400, 200, 'red')


def redraw():
    dot_a.draw()
    dot_b.draw()
    tk.after(10, redraw)


tk.after(10, redraw)


with KaspersMicrobit(MICROBIT_BLUETOOTH_ADDRESS) as microbit:
    microbit.buttons.on_button_a(press=dot_a.show, release=dot_a.hide)
    microbit.buttons.on_button_b(press=dot_b.show, release=dot_b.hide)

    print("if you push button A or B now you will not get the not in main loop error")
    print("But you'll still get 'show called' and 'hide called' because press and release callbacks get executed")
    time.sleep(5)
    print("if you push button A or B now you will see dots appearing on the canvas")

    tk.mainloop()
