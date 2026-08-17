"""Printing utilities: typewriter-style slow printing and boxed headers."""

import time
from typing import List, Optional, Tuple, Union
from dataclasses import dataclass

from .colors import RGB, ColorFuncs, RESET


@dataclass
class PrintOptions:
    speed: float = 10.0
    text_color: Optional[Union[RGB, List[int], Tuple[int, ...]]] = None
    background_color: Optional[Union[RGB, List[int], Tuple[int, ...]]] = None
    end: str = "\n"
    newline_delay: float = 0.5


class Printer:

    @staticmethod
    def slow_print(text: str, options: Optional[PrintOptions] = None):
        if options is None:
            options = PrintOptions()

        delay = 1 / options.speed

        if options.text_color:
            print(ColorFuncs.rgb_fore(options.text_color), end="")
        if options.background_color:
            print(ColorFuncs.rgb_back(options.background_color), end="")

        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
            if char == "\n":
                time.sleep(options.newline_delay)

        print(RESET, end=options.end)

    @staticmethod
    def print_box(text: str):
        """
        You can use this function to create the cool looking boxes that I've been using to group the code!
        """
        border = f"# {'=' * len(text)} #"
        print(f"{border}\n# {text} #\n{border}")


# Aliases
slow_print = Printer.slow_print
ccb_gen = Printer.print_box
