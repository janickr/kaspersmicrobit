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


def accelerometer_data(data: AccelerometerData):
    player_direction.x = data.x / 100
    player_direction.y = data.y / 100


with KaspersMicrobit.find_one_microbit() as microbit:
    microbit.accelerometer.notify(accelerometer_data)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("gray")

        new_position = player_position + player_direction
        player_position.x = pygame.math.clamp(new_position.x, 8, screen.get_width() - 8)
        player_position.y = pygame.math.clamp(new_position.y, 8, screen.get_height() - 8)
        pygame.draw.circle(screen, "blue", player_position, 8)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

# }
