from typing import List, Dict, Tuple
import pygame


def load_images(image_details: List[Dict], scale: Tuple[int, int] = None):
    _images = []
    for image_detail in image_details:
        _image = load_image(image_detail=image_detail, scale=scale)
        _images.append(_image)
    return _images


def load_image(image_detail: dict, scale: Tuple[int, int] = None, convert_alpha=False):
    image = image_detail["image"]
    top = 0 if "top" not in image_detail else image_detail["top"]
    left = 0 if "left" not in image_detail else image_detail["left"]
    width = None if "width" not in image_detail else image_detail["width"]
    height = None if "height" not in image_detail else image_detail["height"]

    _image = pygame.image.load(image)
    _width = width if width else _image.get_width() - left
    _height = height if height else _image.get_height() - top

    _image = _image.subsurface(left, top, _width, _height)
    if scale:
        _image = pygame.transform.scale(_image, scale)
    if convert_alpha:
        _image = _image.convert_alpha()

    return _image


def render_text(text: str, font: str, size: int, color=(255, 255, 255)):
    _font = pygame.font.Font(font, size)
    _font_image = _font.render(text, True, color)
    return _font_image


def get_animations(animations: dict, scale: Tuple[int, int] = None):
    _animations = {}
    for action, details in animations.items():
        _frames = len(details["images"])
        _images = load_images(image_details=details["images"], scale=scale)
        _thresholds = [1 * (i + 1) for i in range(_frames)] if "thresholds" not in details else details["thresholds"]
        _offsets = [None] * _frames if "offsets" not in details else details["offsets"]
        _hitboxes = get_scaled_hitboxes(
            hitboxes=[None] * _frames if "hitboxes" not in details else details["hitboxes"],
            images=details["images"],
            scale=scale
        )
        _next = action if "next" not in details else details["next"]

        _animations[action] = {
            "images": _images,
            "thresholds": _thresholds,
            "offsets": _offsets,
            "hitboxes": _hitboxes,
            "next": _next,
        }
    return _animations


def get_scaled_hitboxes(hitboxes: List[Tuple[int, int, int, int]], images: List[dict], scale: Tuple[int, int] = None):
    scaled_hitboxes = []
    for hitbox, image in zip(hitboxes, images):
        if hitbox is None:
            scaled_hitboxes.append(None)
            continue

        if scale:
            _image = load_image(image)
            image_width, image_height = _image.get_size()
            scale_width, scale_height = scale
            ratio_w = scale_width / image_width
            ratio_h = scale_height / image_height
        else:
            ratio_w = 1
            ratio_h = 1

        x, y, w, h = hitbox
        scaled_hitboxes.append((x * ratio_w, y * ratio_h, w * ratio_w, h * ratio_h))
    return scaled_hitboxes

