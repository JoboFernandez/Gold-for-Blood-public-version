import pygame
import sys

from .image_button import ImageButton


class ExitButton(ImageButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def click(self, game):
        pygame.quit()
        sys.exit()

