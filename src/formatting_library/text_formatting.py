"""Text-formatting utilities: alignment/substitution, rainbow text, and
Minecraft-style '&'-code text formatting."""

import re
from typing import Dict, Optional
from dataclasses import dataclass, field

from .colors import ColorFuncs, RAINBOW_COLORS, RESET


class TextFormatter:

    @staticmethod
    def rainbow_text(text: str, *, background: bool = False) -> str:
        color_func = ColorFuncs.rgb_back if background else ColorFuncs.rgb_fore
        non_spaces = [(i, c) for i, c in enumerate(text) if c != ' ']

        if not non_spaces:
            return text

        result = list(text)

        for i, (pos, char) in enumerate(non_spaces):
            color_index = min(
                int(i * len(RAINBOW_COLORS) / len(non_spaces)),
                len(RAINBOW_COLORS) - 1
            )
            rgb_color = RAINBOW_COLORS[color_index]
            result[pos] = f"{color_func(rgb_color)}{char}{RESET}"

        return ''.join(result)

    @staticmethod
    def align_text(text: str, width: int, alignment: str = "right") -> str:
        if width < len(text):
            raise ValueError(f"Width ({width}) cannot be less than text length ({len(text)})")

        mappings = {
            "left": f"{text:<{width}}",
            "right": f"{text:>{width}}",
            "center": f"{text:^{width}}"
        }

        try:
            return mappings[alignment.lower()]
        except KeyError:
            raise ValueError("Invalid alignment. Choose: 'left', 'right', 'center'")

    @staticmethod
    def substitute_text(text: str, replacement: str, start: int = 0, end: Optional[int] = None) -> str:
        if end is None:
            return text[:start] + replacement
        return text[:start] + replacement + text[end:]


@dataclass
class ImprovedColors:

    COLOR_MAP: Dict[str, str] = field(default_factory=lambda: {
        '0': "\33[38;2;0;0;0m",
        '1': "\33[38;2;0;0;170m",
        '2': "\33[38;2;0;170;0m",
        '3': "\33[38;2;0;170;170m",
        '4': "\33[38;2;170;0;0m",
        '5': "\33[38;2;170;0;170m",
        '6': "\33[38;2;255;170;0m",
        '7': "\33[38;2;170;170;170m",
        '8': "\33[38;2;85;85;85m",
        '9': "\33[38;2;85;85;255m",
        'a': "\33[38;2;85;255;85m",
        'b': "\33[38;2;85;255;255m",
        'c': "\33[38;2;255;85;85m",
        'd': "\33[38;2;255;85;255m",
        'e': "\33[38;2;255;255;85m",
        'f': "\33[38;2;255;255;255m",
        'l': '\33[1m',
        'n': '\33[4m',
        'o': '\33[3m',
        'r': "\33[0m"
    })

    def format_text(self, text: str) -> str:
        def replace_color_code(match):
            code = match.group(1).lower()
            return self.COLOR_MAP.get(code, '')

        result = re.sub(r'&(.)', replace_color_code, text)
        return result + RESET


# Aliases
rainbow_text = TextFormatter.rainbow_text
align = TextFormatter.align_text
substitute = TextFormatter.substitute_text

COLORS = ImprovedColors()
formatted = COLORS.format_text
