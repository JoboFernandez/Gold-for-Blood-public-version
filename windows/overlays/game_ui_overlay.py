import pygame
import settings as s

from utilities import load_image, render_text
from models import Player


class GameUIOverlay:

    def __init__(self):
        pass

    def update(self, game):
        pass

    @staticmethod
    def draw(screen: pygame.display, world, player: Player, debug=False):
        coin_detail = {"image": "assets/images/MonedaP.png", "width": 16}
        coin_image = load_image(image_detail=coin_detail, scale=(24, 24))

        coins_collected = str(player.inventory.get("coin", 0))
        coins_collected_image = render_text(text=coins_collected, font=s.FONT_TEXT2, size=16, color=s.COLOR_TEXT2)

        screen.blit(coin_image, (16, 16))
        screen.blit(coins_collected_image, (48, 18))
