#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging


import pygame

from kaspersmicrobit import KaspersMicrobit
from kaspersmicrobit.services.accelerometer import AccelerometerData

logging.basicConfig(level=logging.INFO)

# example {

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

player_direction = pygame.Vector2()
player_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

BUTTON_A_PRESSED = pygame.USEREVENT + 1
BUTTON_A_RELEASED = pygame.USEREVENT + 2
BUTTON_B_PRESSED = pygame.USEREVENT + 3
BUTTON_B_RELEASED = pygame.USEREVENT + 4


def post_pygame_event(button_event: int):
    return lambda button: pygame.event.post(pygame.event.Event(button_event))


with KaspersMicrobit.find_one_microbit() as microbit:
    microbit.buttons.on_button_a(press=post_pygame_event(BUTTON_A_PRESSED), release=post_pygame_event(BUTTON_A_RELEASED))
    microbit.buttons.on_button_b(press=post_pygame_event(BUTTON_B_PRESSED), release=post_pygame_event(BUTTON_B_RELEASED))

    direction = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == BUTTON_A_PRESSED:
                direction = -10
            if event.type == BUTTON_B_PRESSED:
                direction = 10
            if event.type == BUTTON_A_RELEASED:
                direction = max(0, direction)
            if event.type == BUTTON_B_RELEASED:
                direction = min(0, direction)

        player_position.x += direction

        screen.fill("gray")

        player_position.x = pygame.math.clamp(player_position.x, 60, screen.get_width() - 60)
        player_position.y = pygame.math.clamp(player_position.y, 8, screen.get_height() - 8)
        pygame.draw.rect(screen, "blue", pygame.Rect(player_position.x-60, player_position.y-8, 120, 16))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

# }
