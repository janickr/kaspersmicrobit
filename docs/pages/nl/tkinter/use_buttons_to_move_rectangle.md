---
title: Beweeg een balk met de knoppen van de micro:bit
description: Teken een rechthoek op een tkinter-canvas in Python en verplaats deze zijwaarts door op de micro:bit-knoppen te drukken
---

In dit voorbeeld worden callbacks geregistreerd voor knoppen A en B voor hun "press" en "release" gebeurtenissen. Voor het
voorbeeld zenden de callbacks `button_press` en `button_released` tk-events uit met behulp van de event_generate-methode: dit
betekent dat we de TK API oproepen in een callback, dus we verpakken de callback in `do_in_tkinter` (zie ook [do_in_tkinter](../reference/tkinter.md))

Dit gebeurt wanneer de A-knop wordt ingedrukt:

 - de callback `button_press` wordt aangeroepen (`do_in_tkinter` zorgt ervoor dat dit wordt gedaan door TK)
 - `tk.event_generate` voegt een `<<MICROBIT_BUTTON_PRESS_A>>` event toe aan het einde van de TK-eventwachtrij
 - de tk.main_loop verwerkt het event `<<MICROBIT_BUTTON_PRESS_A>>` en ziet dat er een eventhandler `paddle.go_left` aan is gebonden
 - de eventhandler  `paddle.go_left` wordt uitgevoerd: dit stelt de richting van paddle in op `Paddle.LEFT`
 - `tk.main_loop()` roept `redraw` aan waardoor de paddle in het canvas naar links beweegt


Zie ook de API-documentatie:

- [kaspersmicrobit.services.buttons](../reference/services/buttons.md)
- [kaspersmicrobit](../reference/kaspersmicrobit.md)

<!--codeinclude-->
[](../../../../examples/tkinter/tk-use-buttons-to-move-rectangle.py) inside_block:example
<!--/codeinclude-->