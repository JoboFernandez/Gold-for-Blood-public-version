import pygame

import settings as s


def adjust_sound_volume(sounds: dict):
    for action, details in sounds.items():
        details["sound"].set_volume(details["volume"])


def play_sfx(audio: str, volume=1.0):
    sfx = pygame.mixer.Sound(audio)
    sfx.set_volume(volume)
    sfx.play()


def change_bgm(bgm: str, volume: float):
    if s.bgm != bgm:
        pygame.mixer.music.load(bgm)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
    elif s.bgm_volume != volume:
        pygame.mixer.music.set_volume(volume)
    s.bgm = bgm
    s.bgm_volume = volume