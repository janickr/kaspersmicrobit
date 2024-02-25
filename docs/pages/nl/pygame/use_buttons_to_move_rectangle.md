---
title: Beweeg een balk met de knoppen van de micro:bit
description: Teken een rechthoek in pygame en verplaats deze zijwaarts door op de micro:bit-knoppen te drukken
---

In dit voorbeeld worden callbacks geregistreerd voor knoppen A en B voor hun "press" en "release" gebeurtenissen. 
Voor het voorbeeld posten de `post_pygame_event(button_event)` callbacks aangepaste pygame-events

Dit gebeurt er wanneer de A-knop wordt ingedrukt:

 - de callback `post_pygame_event(BUTTON_A_PRESSED)` wordt aangeroepen
 - een nieuwe `tk.pygame.event.Event(BUTTON_A_PRESSED)` wordt in de wachtrij voor pygame-events geplaatst
 - in de lus `while running:` haalt de knopevents op en past de richting van de rechthoek aan


Zie ook de API-documentatie:

- [kaspersmicrobit.services.buttons](../reference/services/buttons.md)
- [kaspersmicrobit](../reference/kaspersmicrobit.md)

<!--codeinclude-->
[](../../../../examples/pygame/pygame-use-buttons-to-move-rectangle.py) inside_block:example
<!--/codeinclude-->