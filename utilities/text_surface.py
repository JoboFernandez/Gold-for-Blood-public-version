from typing import Tuple
import pygame


class TextSurface:

    def __init__(
            self,
            text: str,
            width: int,
            font: str,
            size: int,
            color: Tuple[int, int, int],
            line_spacing: int = 0,
            antialias: bool = True,
            background: Tuple[int, int, int] = None
    ):
        self.width = width
        self.text = text
        self.font = pygame.font.Font(font, size)
        self.color = color
        self.antialias = antialias
        self.background = background
        self.line_spacing = line_spacing

        self.font_height = self.font.size("Tg")[1]
        self.wrapped_text = self.get_wrapped_text()

    def get_wrapped_text(self):
        _wrapped_text = []

        for paragraph in self.text.split("\n"):
            text = paragraph.replace("\t", " " * 5)
            if text == "":
                _wrapped_text.append("")
                continue

            while text:
                i = 1

                while self.font.size(text[:i])[0] < self.width and i < len(text):
                    i += 1

                if i < len(text):
                    i = text.rfind(" ", 0, i) + 1

                _wrapped_text.append(text[:i])
                text = text[i:]

        return _wrapped_text

    @property
    def image(self):
        _image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        y_line = 0
        for text in self.wrapped_text:
            if self.background:
                text_surface = self.font.render(text, self.antialias, self.color, self.background)
            else:
                text_surface = self.font.render(text, self.antialias, self.color)
            _image.blit(text_surface, (0, y_line))
            y_line += self.font_height + self.line_spacing
        return _image

    @property
    def height(self):
        lines = len(self.wrapped_text)
        text_contribution = lines * self.font_height
        spacing_contribution = (lines - 1) * self.line_spacing if lines >= 2 else 0
        return text_contribution + spacing_contribution
