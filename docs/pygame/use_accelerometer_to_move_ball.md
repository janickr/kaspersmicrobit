---
title: Move a ball in pygame with the accelerometer of the micro:bit
description: Draw a ball with pygame in python, and move it around by tilting a micro:bit 
---

In this example the `accelerometer_data` callback is registered for the accelerometer data with 
`microbit.accelerometer.notify`

This happens when the micro:bit offers new accelerometer data:

 - the `accelerometer_data` callback is called with the new data as argument
 - the callback registers the data as the player_direction
 - the `while True:` loop updates the player_position and redraws the ball


See also the API documentation: 

- [kaspersmicrobit.services.accelerometer](../../reference/services/accelerometer/)
- [kaspersmicrobit](../../reference/kaspersmicrobit)


<!--codeinclude-->
[](../../examples/pygame/pygame-use-accelerometer-to-move-ball.py) inside_block:example
<!--/codeinclude-->
