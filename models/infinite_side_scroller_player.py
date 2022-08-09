from typing import Tuple
import pygame

from utilities import get_animations


class InfiniteSideScrollerPlayer:

    def __init__(
            self,
            x: float,
            y: float,
            jump_vel: float,
            animations: dict,
            scale: Tuple[int, int] = None,
    ):
        self.x = x
        self.y = y
        self.y_vel = 0
        self.jump_vel = jump_vel
        self.dx = 0
        self.dy = 0

        self.is_alive = True
        self.inventory = {}

        self.animations = get_animations(animations=animations, scale=scale)
        self.action = next(iter(animations))
        self.action_index = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
    def offset(self):
        offset = self.animations[self.action]["offsets"][self.image_index]
        _x, _y = offset if offset else (0, 0)
        return _x, _y

    @property
    def hitbox(self):
        _hitbox = self.animations[self.action]["hitboxes"][self.image_index]
        _x, _y, _w, _h = _hitbox if _hitbox else (0, 0, self.rect.width, self.rect.height)
        h_box = pygame.Rect(self.rect.x + _x, self.rect.y + _y, _w, _h)
        return h_box

    @property
    def width(self):
        return self.hitbox.width

    @property
    def height(self):
        return self.hitbox.height

    def handle_events(self):
        pass

    def update_death(self):
        pass

    def update_action(self, action: str):
        self.action_index = self.action_index + 1 if self.action == action else 0
        self.action = action
        thresholds = self.animations[self.action]["thresholds"]
        if self.action_index >= thresholds[-1]:
            self.action_index = 0
            next_action = self.animations[self.action]["next"]
            self.action = next_action
        self.update_death()

    def apply_gravity(self, world):
        pass

    def check_trap_collisions(self, world):
        pass

    def check_collectible_collisions(self, world):
        pass

    def handle_vertical_boudaries(self, world):
        pass

    def update_position(self, x: float, y: float):
        _x, _y = self.offset
        self.rect.x = x + _x
        self.rect.y = y + _y

    def update(self, world):
        self.dx, self.dy = 0, 0

        if self.is_alive:
            self.handle_events()

        self.apply_gravity(world=world)

        if self.is_alive:
            self.check_trap_collisions(world=world)
            self.check_collectible_collisions(world=world)

        self.handle_vertical_boudaries(world=world)

        new_x = self.rect.x + self.dx
        new_y = self.rect.y + self.dy
        self.update_position(x=new_x, y=new_y)

    def draw(self, screen: pygame.display, debug=False):
        screen.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(screen, (0, 0, 255), self.hitbox, 1)


