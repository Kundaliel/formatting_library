"""RGB color representation and ANSI color-escape helpers."""

from typing import List, Tuple, Union
from dataclasses import dataclass

RESET = "\033[0m"

RAINBOW_COLORS = [
    (255, 179, 179),
    (255, 217, 179),
    (255, 255, 179),
    (179, 255, 179),
    (179, 179, 255),
    (217, 179, 255)
]


@dataclass
class RGB:

    r: int
    g: int
    b: int

    def __post_init__(self):
        if not all(0 <= val <= 255 for val in (self.r, self.g, self.b)):
            raise ValueError("RGB values must be between 0 and 255")

    @classmethod
    def from_sequence(cls, rgb: Union[List[int], Tuple[int, ...]]) -> 'RGB':
        if len(rgb) != 3:
            raise ValueError("RGB must contain exactly 3 values")
        return cls(*rgb)

    def to_foreground(self) -> str:
        return f"\033[38;2;{self.r};{self.g};{self.b}m"

    def to_background(self) -> str:
        return f"\033[48;2;{self.r};{self.g};{self.b}m"

    def to_dual(self, bottom: 'RGB') -> str:
        return f"\033[48;2;{self.r};{self.g};{self.b};38;2;{bottom.r};{bottom.g};{bottom.b}m"


class ColorFuncs:

    @staticmethod
    def rgb_fore(rgb: Union[RGB, List[int], Tuple[int, ...]]) -> str:
        if not isinstance(rgb, RGB):
            rgb = RGB.from_sequence(rgb)
        return rgb.to_foreground()

    @staticmethod
    def rgb_back(rgb: Union[RGB, List[int], Tuple[int, ...]]) -> str:
        if not isinstance(rgb, RGB):
            rgb = RGB.from_sequence(rgb)
        return rgb.to_background()


# Aliases
rgb_fore = ColorFuncs.rgb_fore
rgb_back = ColorFuncs.rgb_back
