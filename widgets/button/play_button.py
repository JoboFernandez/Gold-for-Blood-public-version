from .image_button import ImageButton


class PlayButton(ImageButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def click(self, game):
        game.restart()

