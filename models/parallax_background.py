from typing import List, Tuple
import pygame

from .background import Background


class ParallaxBackground:

    def __init__(
            self,
            images: List[str],
            x=0,
            y=0,
            x_parallax_start=1,
            x_parallax_end=0,
            y_parallax_start=1,
            y_parallax_end=1,
            scale: Tuple[int, int] = None
    ):
        parallax_dx = (x_parallax_start - x_parallax_end) / len(images)
        parallax_dy = (y_parallax_start - y_parallax_end) / len(images)

        self.backgrounds = [
            Background(
                image=images[i],
                x=x,
                y=y,
                x_parallax=x_parallax_end + parallax_dx * (i + 1),
                y_parallax=y_parallax_end + parallax_dy * (i + 1),
                scale=scale
            ) for i in range(len(images))
        ]

    def update(self, world):
        for background in self.backgrounds:
            background.update(world=world)

    def draw(self, screen: pygame.display, debug=False):
        for background in self.backgrounds:
            background.draw(screen=screen, debug=debug)