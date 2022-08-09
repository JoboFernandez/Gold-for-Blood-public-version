from .stationary_trap import StationaryTrap


class Saw(StationaryTrap):

    def __init__(self, *args, **kwargs):
        default_images = [{"image": f"assets/images/SAW{i}.png"} for i in range(0, 4)]
        animations = {
            "default": {
                "images": default_images,
                "thresholds": [1 * (i + 1) for i in range(len(default_images))],
                "offsets": [None for _ in range(len(default_images))],
                "hitboxes": [None for _ in range(len(default_images))],
                "next": "default",
            }
        }
        super().__init__(animations=animations, *args, **kwargs)
