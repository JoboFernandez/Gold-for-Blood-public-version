import pygame

from utilities import play_sfx
from .infinite_side_scroller_player import InfiniteSideScrollerPlayer
from .coin import SilverCoin, RedCoin, GoldCoin


class Player(InfiniteSideScrollerPlayer):

    def __init__(self, *args, **kwargs):
        jump_vel = 9.5

        walk = [{"image": f"assets/images/{x}.png"} for x in range(8, 16)]
        pre_jump = [{"image": f"assets/images/{x}.png"} for x in range(1, 3)]
        jump = [{"image": f"assets/images/{x}.png"} for x in range(3, 4)]
        fall = [{"image": f"assets/images/{x}.png"} for x in range(4, 5)]
        land = [{"image": f"assets/images/{x}.png"} for x in range(5, 8)]
        pre_slide = [{"image": f"assets/images/S{x}.png"} for x in range(1, 2)]
        slide = [{"image": f"assets/images/S{x}.png"} for x in range(2, 3)]
        stand_up = [{"image": f"assets/images/S{x}.png"} for x in range(3, 6)]
        die = [{"image": f"assets/images/{x}.png"} for x in range(0, 1)]
        animations = {
            "walk": {
                "images": walk,
                "thresholds": [3 * (i + 1) for i in range(len(walk))],
                "offsets": [None for _ in range(len(walk))],
                "hitboxes": [(4, 0, 38, 54) for _ in range(len(walk))],
                "next": "walk",
            },
            "pre-jump": {
                "images": pre_jump,
                "thresholds": [2 * (i + 1) for i in range(len(pre_jump))],
                "offsets": [None for _ in range(len(pre_jump))],
                "hitboxes": [(6, 0, 30, 54), (0, 0, 30, 58)],
                "next": "jump",
            },
            "jump": {
                "images": jump,
                "thresholds": [1 * (i + 1) for i in range(len(jump))],
                "offsets": [None for _ in range(len(jump))],
                "hitboxes": [(7, 0, 30, 49)],
                "next": "jump",
            },
            "fall": {
                "images": fall,
                "thresholds": [1 * (i + 1) for i in range(len(fall))],
                "offsets": [None for _ in range(len(fall))],
                "hitboxes": [(11, 0, 30, 53)],
                "next": "fall",
            },
            "land": {
                "images": land,
                "thresholds": [1 * (i + 1) for i in range(len(land))],
                "offsets": [None for _ in range(len(land))],
                "hitboxes": [(11, 0, 30, 50), (12, 0, 30, 48), (8, 0, 30, 55)],
                "next": "walk",
            },
            "pre-slide": {
                "images": pre_slide,
                "thresholds": [1 * (i + 1) for i in range(len(pre_slide))],
                "offsets": [(0, 9)],
                "hitboxes": [(0, 0, 32, 48)],
                "next": "slide",
            },
            "slide": {
                "images": slide,
                "thresholds": [1 * (i + 1) for i in range(len(slide))],
                "offsets": [(0, 24)],
                "hitboxes": [(0, 0, 57, 33)],
                "next": "slide",
            },
            "stand up": {
                "images": stand_up,
                "thresholds": [2 * (i + 1) for i in range(len(stand_up))],
                "offsets": [(0, 5), (0, 1), None],
                "hitboxes": [(0, 0, 44, 52), (0, 0, 39, 56), (0, 0, 33, 58)],
                "next": "walk",
            },
            "die": {
                "images": die,
                "thresholds": [1 * (i + 1) for i in range(len(die))],
                "offsets": [(0, 24)],
                "hitboxes": [(0, 0, 56, 34)],
                "next": "die",
            },
        }

        super().__init__(jump_vel=jump_vel, animations=animations, *args, **kwargs)

    def handle_events(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            if self.action in ["walk"]:
                self.update_action(action="pre-jump")
                self.y_vel = -self.jump_vel
                play_sfx(audio="assets/audio/Jump 1.wav", volume=0.70)
            else:
                self.update_action(action=self.action)
        elif keys[pygame.K_DOWN]:
            if self.action in ["walk"]:
                self.update_action(action="pre-slide")
                play_sfx(audio="assets/audio/Slide.mp3", volume=0.20)
            elif self.action in ["pre-slide", "slide"]:
                self.update_action(action="slide")
            else:
                self.update_action(action=self.action)
        else:
            if self.action in ["slide"]:
                self.update_action(action="stand up")
            else:
                self.update_action(action=self.action)

    def update_death(self):
        if self.action == "die" and self.is_alive:
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
                play_sfx(audio="assets/audio/Hit 1.wav", volume=0.50)
                self.update_action(action="die")

    def check_collectible_collisions(self, world):
        for collectible in world.collectibles:
            if collectible.hitbox.colliderect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height):
                self.inventory[collectible.name] = self.inventory.get(collectible.name, 0) + collectible.value
                if isinstance(collectible, (SilverCoin, RedCoin, GoldCoin)):
                    play_sfx(audio="assets/audio/Coin 1.wav", volume=0.20)
                world.collectibles.pop(world.collectibles.index(collectible))

    def handle_vertical_boudaries(self, world):
        if self.rect.bottom + self.dy > world.height:
            if self.action in ["walk"]:
                self.update_action(action="walk")
            elif self.action in ["fall"]:
                self.update_action(action="land")
            self.dy = world.height - self.rect.bottom
            self.y_vel = 0

