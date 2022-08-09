import pygame
import sys

from windows import InfiniteSideScrollerWindow
from utilities import change_bgm
import settings as s


pygame.init()
pygame.display.set_caption(s.GAME_TITLE)
window = pygame.display.set_mode((s.WINDOW_WIDTH, s.WINDOW_HEIGHT))
pygame.font.init()
clock = pygame.time.Clock()

game = InfiniteSideScrollerWindow(size=(s.WINDOW_WIDTH, s.WINDOW_HEIGHT))
change_bgm(bgm=game.bgm, volume=game.bgm_volume)

while True:

    clock.tick(s.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.update(game=None)
    game.draw(screen=window, debug=s.DEBUG)
    pygame.display.update()

