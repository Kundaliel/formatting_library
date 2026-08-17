"""Terminal manipulation helpers (cursor movement, clearing, line replacement)."""


class Terminal:

    @staticmethod
    def clear_screen():
        print("\033c\033[H", end="")

    @staticmethod
    def set_cursor_position(x: int, y: int):
        print(f"\033[{x};{y}H", end="")

    @staticmethod
    def scroll_cursor(lines: int):
        direction = "A" if lines <= 0 else "B"
        print(f"\033[{abs(lines)}{direction}", end="")

    @staticmethod
    def replace_current_line(text: str):
        print(f"\33[2K\r{text}", end="")

    @staticmethod
    def replace_line(y: int, text: str):
        print(f"\33[s\33[{y};0H\33[2K\r{text}\33[u", end="")


# Aliases
clear_screen = Terminal.clear_screen
set_cursor_position = Terminal.set_cursor_position
scroll_cursor = Terminal.scroll_cursor
replace_current_line = Terminal.replace_current_line
replace_line = Terminal.replace_line
