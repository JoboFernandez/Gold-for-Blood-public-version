from typing import Tuple
import pygame

from utilities import get_animations


class StationaryTrap:

    def __init__(self, x: float, y: float, animations: dict, scale: Tuple[int, int] = None):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.x_scroll = 0

        self.animations = get_animations(animations=animations, scale=scale)
        self.action = "default"
        self.action_index = 0

    @property
    def image_index(self):
        image_index = 0
        thresholds = self.animations[self.action]["thresholds"]
        for i, threshold in enumerate(thresholds):
            if self.action_index < threshold:
                image_index = i
                break
        return image_index

    @property
    def image(self):
        return self.animations[self.action]["images"][self.image_index]

    @property
    def rect(self):
        x = self.x + self.x_scroll
        y = self.y
        return pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    @property
    def hitbox(self):
        _hitbox = self.animations[self.action]["hitboxes"][self.image_index]
        _x, _y, _w, _h = _hitbox if _hitbox else (0, 0, self.rect.width, self.rect.height)
        h_box = pygame.Rect(self.rect.x + _x, self.rect.y + _y, _w, _h)
        return h_box

    def update_action(self, action: str):
        self.action_index = self.action_index + 1 if self.action == action else 0
        self.action = action
        thresholds = self.animations[self.action]["thresholds"]
        if self.action_index >= thresholds[-1]:
            self.action_index = 0
            next_action = self.animations[self.action]["next"]
            self.action = next_action

    def update_position(self, x: float, y: float):
        self.rect.x = x
        self.rect.y = y

    def update(self, world):
        self.x_scroll = world.x_scroll
        self.update_action(action="default")

        new_x = self.rect.x + self.dx
        new_y = self.rect.y + self.dy
        self.update_position(x=new_x, y=new_y)

    def draw(self, screen: pygame.display, debug=False):
        screen.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)