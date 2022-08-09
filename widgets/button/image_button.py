from typing import Tuple, Union
import pygame

from utilities import load_image


class ImageButton:

    def __init__(
            self,
            x: float,
            y: float,
            images: Union[str, Tuple[str], Tuple[str, str], Tuple[str, str, str]],
            scale: Tuple[int, int] = None,
    ):
        self.x = x
        self.y = y

        if isinstance(images, str):
            image_default = images
            image_hovered = images
            image_clicked = images
        else:
            image_default = images[0]
            if len(images) == 1:
                image_hovered = images[0]
                image_clicked = images[0]
            elif len(images) == 2:
                image_hovered = images[1]
                image_clicked = images[1]
            else:
                image_hovered = images[1]
                image_clicked = images[2]

        image_detail = {"image": image_default}
        self.image_default = load_image(image_detail=image_detail, scale=scale)

        image_detail = {"image": image_hovered}
        self.image_hovered = load_image(image_detail=image_detail, scale=scale)

        image_detail = {"image": image_clicked}
        self.image_clicked = load_image(image_detail=image_detail, scale=scale)

        self.image = self.image_default

        self.rect.x = x
        self.rect.y = y

    @property
    def rect(self):
        rect = self.image.get_rect()
        rect.x = self.x
        rect.y = self.y
        return rect

    @property
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    @property
    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.is_hovered

    def click(self, game):
        pass

    def update(self, game):
        if self.is_clicked:
            self.image = self.image_clicked
            self.click(game)
        elif self.is_hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_default

    def draw(self, screen: pygame.display):
        screen.blit(self.image, (self.x, self.y))

