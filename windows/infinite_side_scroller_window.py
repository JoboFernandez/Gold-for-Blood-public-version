from typing import Tuple
import pygame
import random

from utilities import play_sfx
from models import Background, ParallaxBackground, Player, Saw, Spike, SilverCoin, RedCoin, GoldCoin
from .overlays import GameUIOverlay, GameOverOverlay


class InfiniteSideScrollerWindow:

    def __init__(self, size: Tuple[int, int]):
        self.size = size
        self.window_width, self.window_height = size
        self.height = 400

        self.x_scroll = 0
        self.scroll_speed = 5
        self.gravity = 0.5
        self.benchmark = 0

        self.backgrounds = []
        self.foregrounds = []
        self.player = Player(x=100, y=313)
        self.traps = []
        self.collectibles = []
        self.overlays = []
        self._overlays = {
            "ui": GameUIOverlay(),
            "game over": GameOverOverlay(size=size),
        }
        self.restart()

        self.bgm = "assets/audio/otherworld.ogg"
        self.bgm_volume = 0.75

        self.state = "play"

    def restart(self):
        self.x_scroll = 0
        self.scroll_speed = 5
        self.benchmark = 0
        self.backgrounds = []
        self.foregrounds = []
        self.player = Player(x=100, y=313)
        self.traps = []
        self.collectibles = []

        self.backgrounds = [
            ParallaxBackground(
                images=[
                    "assets/images/Layer_0011_0.png",
                    "assets/images/Layer_0010_1.png",
                    "assets/images/Layer_0009_2.png",
                    "assets/images/Layer_0008_3.png",
                    # "assets/images/Layer_0007_Lights.png",
                    # "assets/images/Layer_0006_4.png",
                    "assets/images/Layer_0005_5.png",
                    # "assets/images/Layer_0004_Lights.png",
                    # "assets/images/Layer_0003_6.png",
                    "assets/images/Layer_0001_8.png",
                ],
                y=-346,
            )
        ]
        self.foregrounds = [
            Background(image="assets/images/Layer_0002_7.png", x_parallax=1, y=-346),
            Background(image="assets/images/Layer_0000_9.png", x_parallax=1, y=-346),
        ]

        self.add_elements()

        self.overlays = ["ui"]
        self.state = "play"

    def add_elements(self):

        def get_new_trap(world, trap_location: float):
            if abs(world.x_scroll) <= world.window_width * 4:
                trap_type = random.randint(0, 1)
            elif abs(world.x_scroll) <= world.window_width * 10:
                trap_type = random.choice([0, 1, 1, 2, 2])
            elif abs(world.x_scroll) <= world.window_width * 20:
                trap_type = random.choice([0, 1, 1, 2, 2, 3, 3])
            else:
                trap_type = random.choice([0, 1, 1, 2, 2, 3, 3, 4, 4])

            if trap_type == 0:
                _new_trap = Spike(x=trap_location, y=0, scale=(64, world.height - 96))
            elif trap_type == 1:
                _new_trap = Saw(x=trap_location, y=self.height - 48, scale=(48, 48))
            elif trap_type == 2:
                _new_trap = Spike(x=trap_location, y=0, scale=(64, world.height - 48))
            else:
                _new_trap = Saw(x=trap_location, y=self.height - 64, scale=(64, 64))
            return _new_trap

        def get_new_coin(world, coin_x, coin_y):
            if abs(world.x_scroll) <= world.window_width * 4:
                coin_type = 0
            elif abs(world.x_scroll) <= world.window_width * 10:
                coin_type = random.randint(0, 11)
            else:
                coin_type = random.randint(0, 12)

            if coin_type < 10:
                _new_coin = SilverCoin(x=coin_x, y=coin_y, scale=(32, 32), name="coin")
            elif coin_type < 12:
                _new_coin = RedCoin(x=coin_x, y=coin_y, scale=(32, 32), name="coin")
            else:
                _new_coin = GoldCoin(x=coin_x, y=coin_y, scale=(32, 32), name="coin")
            return _new_coin

        trap_distance = (2 * self.scroll_speed * self.player.jump_vel / self.gravity) + 250
        coin_distance = 64
        coin_span = int(2.5 * self.window_width)

        if not self.collectibles:
            coin_start = int(trap_distance) + random.randint(-32, 32)
            coin_end = coin_span
            for coin_x in range(coin_start, coin_end, coin_distance):
                coin_y = random.choice([self.height - 48, self.height - 48 * 2, self.height - 48 * 3, None, None])
                if coin_y:
                    new_coin = get_new_coin(world=self, coin_x=coin_x, coin_y=coin_y)
                    self.collectibles.append(new_coin)

        if abs(self.x_scroll + self.benchmark) > self.window_width:
            self.benchmark += self.window_width

            coin_start = int(self.collectibles[-1].x) + coin_distance
            coin_end = int(abs(self.x_scroll) + coin_span)
            for coin_x in range(coin_start, coin_end, coin_distance):
                coin_y = random.choice([self.height - 48, self.height - 48 * 2, self.height - 48 * 3, None, None])
                if coin_y:
                    new_coin = get_new_coin(world=self, coin_x=coin_x, coin_y=coin_y)
                    self.collectibles.append(new_coin)

        if not self.traps:
            new_trap = get_new_trap(world=self, trap_location=trap_distance)
            self.traps.append(new_trap)

        while trap_distance < abs(self.x_scroll) + 2 * self.window_width - self.traps[-1].x:
            trap_location = self.traps[-1].x + trap_distance
            new_trap = get_new_trap(world=self, trap_location=trap_location)
            self.traps.append(new_trap)

            self.scroll_speed += 0.1
            trap_distance = (2 * self.scroll_speed * self.player.jump_vel / self.gravity) + 300

        for trap in self.traps:
            for collectible in self.collectibles:
                if trap.hitbox.colliderect(collectible.hitbox):
                    self.collectibles.pop(self.collectibles.index(collectible))

    def update(self, game):
        if not self.player.is_alive:
            if "game over" not in self.overlays:
                play_sfx(audio="assets/audio/Game Over 1.wav", volume=0.60)
                self.overlays.append("game over")
                self.overlays.remove("ui")
            self.scroll_speed = 0

        self.x_scroll -= self.scroll_speed

        self.player.update(world=self)

        for background in self.backgrounds:
            background.update(world=self)
        for foreground in self.foregrounds:
            foreground.update(world=self)

        if self.state == "play":
            self.add_elements()

        for trap in self.traps:
            trap.update(world=self)
            if trap.hitbox.x + trap.hitbox.width < 0:
                self.traps.pop(self.traps.index(trap))

        for collectible in self.collectibles:
            collectible.update(world=self)
            if collectible.hitbox.x + collectible.hitbox.width < 0:
                self.collectibles.pop(self.collectibles.index(collectible))

        for overlay in self.overlays:
            self._overlays[overlay].update(game=self)

    def draw(self, screen: pygame.display, debug=False):
        for background in self.backgrounds:
            background.draw(screen=screen, debug=debug)

        for trap in self.traps:
            trap.draw(screen=screen, debug=debug)

        for collectible in self.collectibles:
            collectible.draw(screen=screen, debug=debug)

        self.player.draw(screen=screen, debug=debug)

        for foreground in self.foregrounds:
            foreground.draw(screen=screen, debug=debug)

        for overlay in self.overlays:
            self._overlays[overlay].draw(screen=screen, world=self, player=self.player)
