from typing import Tuple
import pygame

from utilities import load_image, render_text
from widgets import PlayButton, ExitButton
from models import Player
import settings as s


class GameOverOverlay:

    def __init__(self, size: Tuple[int, int]):
        self.size = size
        self.window_width, self.window_height = size

        self.mask = pygame.Surface(size)
        self.mask.fill((0, 0, 0))
        self.mask.set_alpha(170)

        self.summary = []

        self.buttons = [
            PlayButton(
                x=200 + 43,
                y=self.window_height*3//4-24,
                images=("assets/images/icon_replay.png", "assets/images/icon_replay_hover.png"),
                scale=(48, 48),
            ),
            ExitButton(
                x=200 + 43 * 5 + 48 * 2,
                y=self.window_height*3//4-24,
                images=("assets/images/icon_exit.png", "assets/images/icon_exit_hover.png"),
                scale=(48, 48)
            ),
        ]

    def restart(self):
        pass

    def update(self, game):
        for button in self.buttons:
            button.update(game=game)

    def draw(self, screen: pygame.display, world, player: Player, debug=False):
        # draw mask
        screen.blit(self.mask, (0, 0))

        # draw summary board
        summary_board = (world.window_width // 4, world.window_height // 4, world.window_width // 2, world.window_height // 2)
        pygame.draw.rect(screen, color=s.COLOR_BACKGROUND1, rect=summary_board, border_radius=10)
        pygame.draw.rect(screen, color=s.BLACK, rect=summary_board, border_radius=10, width=7)
        pygame.draw.rect(screen, color=s.GRAY, rect=summary_board, border_radius=10, width=6)
        pygame.draw.rect(screen, color=s.COLOR_OUTLINE1, rect=summary_board, border_radius=10, width=5)
        pygame.draw.rect(screen, color=s.GRAY, rect=summary_board, border_radius=10, width=2)
        pygame.draw.rect(screen, color=s.BLACK, rect=summary_board, border_radius=10, width=1)

        # draw achievements
        coin_detail = {"image": "assets/images/MonedaP.png", "width": 16}
        coin_image = load_image(image_detail=coin_detail, scale=(32, 32))
        coin_location = (world.window_width // 2 - 16 - 16, world.window_height // 2 - 16)
        coins_collected = str(player.inventory.get("coin", 0))
        coins_collected_image = render_text(text=coins_collected, font=s.FONT_TEXT2, size=32, color=s.COLOR_TEXT3)
        coins_collected_location = (world.window_width // 2 + 16, world.window_height // 2 - 18)
        screen.blit(coin_image, coin_location)
        screen.blit(coins_collected_image, coins_collected_location)

        # draw buttons
        for button in self.buttons:
            screen.blit(button.image, button.rect)

