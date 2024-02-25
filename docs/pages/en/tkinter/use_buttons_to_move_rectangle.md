---
title: Move a paddle with the buttons of the micro:bit
description: Draw a rectangle on a tkinter canvas in python, and move it sideways by pressing the micro:bit buttons
---

In this example callbacks are registered for buttons A and B for their "press" and "release" events. For the sake 
of the example the `button_pressed` and `button_released` callbacks emit tk events using the event_generate method: this
means we call TK API in a callback, so we wrap the callback in `do_in_tkinter` (see also [do_in_tkinter](../reference/tkinter.md))

This happens when the A button is pushed:

 - the `button_pressed` callback is called (do_in_tkinter makes sure this is done by TK)
 - `tk.event_generate` adds a `<<MICROBIT_BUTTON_PRESS_A>>` event at the end of the TK event queue
 - the tk.main_loop processes the `<<MICROBIT_BUTTON_PRESS_A>>` event, sees that there is a `paddle.go_left` event handler bound to it 
 - the `paddle.go_left` event handler is executed: this sets the direction attribute of paddle to `Paddle.LEFT`
 - `tk.main_loop()` calls `redraw` which moves the paddle in the canvas to the left


See also the API documentation: 

- [kaspersmicrobit.services.buttons](../reference/services/buttons.md)
- [kaspersmicrobit](../reference/kaspersmicrobit.md)

<!--codeinclude-->
[](../../../../examples/tkinter/tk-use-buttons-to-move-rectangle.py) inside_block:example
<!--/codeinclude-->
