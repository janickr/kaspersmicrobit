
In this example the `accelerometer_data` callback is registered for the accelerometer data with 
`microbit.accelerometer.notify`

This happens when the microbit offers new accelerometer data:

 - the `accelerometer_data` callback is called with the new data as argument
 - the callback registers the data as the ball.direction
- `tk.main_loop()` calls redraw which moves the ball on the canvas in the direction set earlier by the callback


See also the API documentation: 

- [kaspersmicrobit.services.accelerometer](../../reference/services/accelerometer/)
- [kaspersmicrobit](../../reference/kaspersmicrobit)


<!--codeinclude-->
[](../../examples/tkinter/tk-use-accelerometer-to-move-ball.py) inside_block:example
<!--/codeinclude-->
