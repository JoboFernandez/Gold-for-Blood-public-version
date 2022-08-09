from typing import Tuple
import pygame

from utilities import load_images, adjust_sound_volume, get_scaled_hitboxes
from .coin import SilverCoin, RedCoin, GoldCoin


class Player:

    def __init__(self, x: float, y: float, scale: Tuple[int, int] = None):
        self.x = x
        self.y = y
        self.y_vel = 0
        self.jump_vel = 9.5
        self.dx = 0
        self.dy = 0

        self.is_alive = True
        self.inventory = {}

        walk = [{"image": f"assets/images/{x}.png"} for x in range(8, 16)]
        pre_jump = [{"image": f"assets/images/{x}.png"} for x in range(1, 3)]
        jump = [{"image": f"assets/images/{x}.png"} for x in range(3, 4)]
        fall = [{"image": f"assets/images/{x}.png"} for x in range(4, 5)]
        land = [{"image": f"assets/images/{x}.png"} for x in range(5, 8)]
        pre_slide = [{"image": f"assets/images/S{x}.png"} for x in range(1, 2)]
        slide = [{"image": f"assets/images/S{x}.png"} for x in range(2, 3)]
        stand_up = [{"image": f"assets/images/S{x}.png"} for x in range(3, 6)]
        die = [{"image": f"assets/images/{x}.png"} for x in range(0, 1)]
        self.animations = {
            "walk": {
                "images": load_images(image_details=walk, scale=scale),
                "thresholds": [3 * (i + 1) for i in range(len(walk))],
                "offsets": [None for _ in range(len(walk))],
                "hitboxes": [(4, 0, 38, 54) for _ in range(len(walk))],
                "next": "walk",
            },
            "pre-jump": {
                "images": load_images(image_details=pre_jump, scale=scale),
                "thresholds": [2 * (i + 1) for i in range(len(pre_jump))],
                "offsets": [None for _ in range(len(pre_jump))],
                "hitboxes": [(6, 0, 30, 54), (0, 0, 30, 58)],
                "next": "jump",
            },
            "jump": {
                "images": load_images(image_details=jump, scale=scale),
                "thresholds": [1 * (i + 1) for i in range(len(jump))],
                "offsets": [None for _ in range(len(jump))],
                "hitboxes": [(7, 0, 30, 49)],
                "next": "jump",
            },
            "fall": {
                "images": load_images(image_details=fall, scale=scale),
                "thresholds": [1 * (i + 1) for i in range(len(fall))],
                "offsets": [None for _ in range(len(fall))],
                "hitboxes": [(11, 0, 30, 53)],
                "next": "fall",
            },
            "land": {
                "images": load_images(image_details=land, scale=scale),
                "thresholds": [1 * (i + 1) for i in range(len(land))],
                "offsets": [None for _ in range(len(land))],
                "hitboxes": [(11, 0, 30, 50), (12, 0, 30, 48), (8, 0, 30, 55)],
                "next": "walk",
            },
            "pre-slide": {
                "images": load_images(image_details=pre_slide, scale=scale),
                "thresholds": [1 * (i + 1) for i in range(len(pre_slide))],
                "offsets": [(0, 9)],
                "hitboxes": [(0, 0, 32, 48)],
                "next": "slide",
            },
            "slide": {
                "images": load_images(image_details=slide, scale=scale),
                "thresholds": [1 * (i + 1) for i in range(len(slide))],
                "offsets": [(0, 24)],
                "hitboxes": [(0, 0, 57, 33)],
                "next": "slide",
            },
            "stand up": {
                "images": load_images(image_details=stand_up, scale=scale),
                "thresholds": [2 * (i + 1) for i in range(len(stand_up))],
                "offsets": [(0, 5), (0, 1), None],
                "hitboxes": [(0, 0, 44, 52), (0, 0, 39, 56), (0, 0, 33, 58)],
                "next": "walk",
            },
            "die": {
                "images": load_images(image_details=die, scale=scale),
                "thresholds": [1 * (i + 1) for i in range(len(die))],
                "offsets": [(0, 24)],
                "hitboxes": [(0, 0, 56, 34)],
                "next": "die",
            },
        }
        self.audios = {
            "jump": {
                "sound": pygame.mixer.Sound("assets/audio/Jump 1.wav"),
                "volume": 0.70,
            },
            "slide": {
                "sound": pygame.mixer.Sound("assets/audio/Slide.mp3"),
                "volume": 0.20,
            },
            "die": {
                "sound": pygame.mixer.Sound("assets/audio/Hit 1.wav"),
                "volume": 0.50,
            },
            "collect coin": {
                "sound": pygame.mixer.Sound("assets/audio/Coin 1.wav"),
                "volume": 0.20,
            },
        }
        adjust_sound_volume(sounds=self.audios)
        self.action = "walk"
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
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            if self.action in ["walk"]:
                self.update_action(action="pre-jump")
                self.y_vel = -self.jump_vel
                self.audios["jump"]["sound"].play()
            else:
                self.update_action(action=self.action)
        elif keys[pygame.K_DOWN]:
            if self.action in ["walk"]:
                self.update_action(action="pre-slide")
                self.audios["slide"]["sound"].play()
            elif self.action in ["pre-slide", "slide"]:
                self.update_action(action="slide")
            else:
                self.update_action(action=self.action)
        else:
            if self.action in ["slide"]:
                self.update_action(action="stand up")
            else:
                self.update_action(action=self.action)

    def update_action(self, action: str):
        self.action_index = self.action_index + 1 if self.action == action else 0
        self.action = action
        thresholds = self.animations[self.action]["thresholds"]
        if self.action_index >= thresholds[-1]:
            self.action_index = 0
            next_action = self.animations[self.action]["next"]
            self.action = next_action

        if action == "die" and self.is_alive:
            self.is_alive = False
            pygame.time.delay(1000)

    def apply_gravity(self, world):
        self.y_vel += world.gravity
        if self.y_vel - world.gravity > 0:
            if self.action not in ["die"]:
                self.action = "fall"
        self.dy = self.y_vel

    def check_trap_collisions(self, world):
        for trap in world.traps:
            if trap.hitbox.colliderect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height):
                self.audios["die"]["sound"].play()
                self.update_action(action="die")

    def check_collectible_collisions(self, world):
        for collectible in world.collectibles:
            if collectible.hitbox.colliderect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height):
                self.inventory[collectible.name] = self.inventory.get(collectible.name, 0) + collectible.value
                if isinstance(collectible, (SilverCoin, RedCoin, GoldCoin)):
                    self.audios["collect coin"]["sound"].play()
                world.collectibles.pop(world.collectibles.index(collectible))

    def handle_vertical_boudaries(self, world):
        if self.rect.bottom + self.dy > world.height:
            if self.action in ["walk"]:
                self.update_action(action="walk")
            elif self.action in ["fall"]:
                self.update_action(action="land")
            self.dy = world.height - self.rect.bottom
            self.y_vel = 0

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


