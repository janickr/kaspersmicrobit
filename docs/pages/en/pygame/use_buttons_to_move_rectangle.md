---
title: Move a paddle with the buttons of the micro:bit
description: Draw a rectangle in pygame, and move it sideways by pressing the micro:bit buttons
---

In this example callbacks are registered for buttons A and B for their "press" and "release" events. For the sake 
of the example the `post_pygame_event(button_event)`  callbacks post custom pygame events

This happens when the A button is pushed:

 - the `post_pygame_event(BUTTON_A_PRESSED)` callback is called 
 - a new `tk.pygame.event.Event(BUTTON_A_PRESSED)` is posted to the pygame event queue
 - in the `while running:` loop gets the button events and updates the direction of the rectangle accordingly


See also the API documentation: 

- [kaspersmicrobit.services.buttons](../reference/services/buttons.md)
- [kaspersmicrobit](../reference/kaspersmicrobit.md)

<!--codeinclude-->
[](../../../../examples/pygame/pygame-use-buttons-to-move-rectangle.py) inside_block:example
<!--/codeinclude-->
