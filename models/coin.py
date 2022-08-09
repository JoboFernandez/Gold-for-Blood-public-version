from .collectible import Collectible


class SilverCoin(Collectible):

    def __init__(self, *args, **kwargs):
        default_images = [{"image": "assets/images/MonedaP.png", "left": 16 * i, "width": 16} for i in range(5)]
        super().__init__(images=default_images, *args, **kwargs)
        self.value = 10


class RedCoin(Collectible):

    def __init__(self, *args, **kwargs):
        default_images = [{"image": "assets/images/MonedaR.png", "left": 16 * i, "width": 16} for i in range(5)]
        super().__init__(images=default_images, *args, **kwargs)
        self.value = 50


class GoldCoin(Collectible):

    def __init__(self, *args, **kwargs):
        default_images = [{"image": "assets/images/MonedaD.png", "left": 16 * i, "width": 16} for i in range(5)]
        super().__init__(images=default_images, *args, **kwargs)
        self.value = 100

