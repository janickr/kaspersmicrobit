#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

class Dot:

    def __init__(self, canvas, x, y, color):
        self._color = color
        self._y = y
        self._x = x
        self._canvas = canvas
        self._show = False
        self._id = None

    def draw(self):
        if self._show and not self._id:
            self._id = self._canvas.create_oval(self._x - 10, self._y - 10, self._x + 10, self._y + 10, fill=self._color)
        elif not self._show and self._id:
            self._canvas.delete(self._id)
            self._id = None

    def show(self, event):
        print("show called")
        self._show = True

    def hide(self, event):
        print("hide called")
        self._show = False
