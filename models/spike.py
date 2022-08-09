from .stationary_trap import StationaryTrap


class Spike(StationaryTrap):

    def __init__(self, *args, **kwargs):
        default_images = [{"image": f"assets/images/unavoidable_spikes_just_roller_{str(i).zfill(2)}.png"} for i in range(1, 11)]
        animations = {
            "default": {
                "images": default_images,
                "thresholds": [2 * (i + 1) for i in range(len(default_images))],
                "offsets": [None for _ in range(len(default_images))],
                "hitboxes": [(75, 0, 145, 512) for _ in range(len(default_images))],
                "next": "default",
            }
        }
        super().__init__(animations=animations, *args, **kwargs)

