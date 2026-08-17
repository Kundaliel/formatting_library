from .colors import (
    RGB,
    ColorFuncs,
    RESET,
    RAINBOW_COLORS,
    rgb_fore,
    rgb_back,
)
from .terminal import (
    Terminal,
    clear_screen,
    set_cursor_position,
    scroll_cursor,
    replace_current_line,
    replace_line,
)
from .text_formatting import (
    TextFormatter,
    ImprovedColors,
    rainbow_text,
    align,
    substitute,
    COLORS,
    formatted,
)
from .printing import (
    PrintOptions,
    Printer,
    slow_print,
    ccb_gen,
)
from .image_render import (
    ImageRenderer,
    IMAGE_CHARACTER,
    img_to_ascii,
)
from .c_builder import CBuilder
from .esoteric import (
    Esoteric,
    runBefunge,
    runLOLCODE,
)

__version__ = "1.3.0"
__author__ = "Kundaliel"
__email__ = "kundaliel.official@gmail.com"
