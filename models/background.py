from typing import Tuple
import pygame
import math

from utilities import load_image


class Background:

    def __init__(self, image: str, x=0, y=0, x_parallax=1, y_parallax=1, scale: Tuple[int, int] = None):
        image_detail = {"image": image}
        self.image = load_image(image_detail=image_detail, scale=scale)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.x = x
        self.x_parallax = x_parallax
        self.x_scroll = 0
        self.horizontal_tile_count = 1

        self.y = y
        self.y_parallax = y_parallax
        self.y_scroll = 0
        self.vertical_tile_count = 1

    def update(self, world):
        self.x_scroll = world.x_scroll * self.x_parallax
        tiles_beyond_screen, tile_on_screen_edge = divmod(abs(self.x_scroll), self.width)
        self.x = -tile_on_screen_edge
        self.horizontal_tile_count = math.ceil((tile_on_screen_edge + world.window_width) / self.width)

    def draw(self, screen: pygame.display, debug=False):
        for i in range(self.horizontal_tile_count + 1):
            screen.blit(self.image, (self.x + i * self.width, self.y))
            if debug:
                rect = pygame.Rect(self.x + i * self.width, self.y, self.width, self.height)
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)

