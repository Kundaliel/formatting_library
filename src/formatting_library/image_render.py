"""Render images as ANSI-colored half-block ASCII art in the terminal."""

from pathlib import Path
from typing import Union

from PIL import Image  # type: ignore

from .colors import RGB, RESET

IMAGE_CHARACTER = "▄"


class ImageRenderer:

    @staticmethod
    def image_to_ascii(image_path: Union[str, Path]) -> str:
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        lines = []

        with Image.open(image_path) as image:
            if image.mode != 'RGB':
                image = image.convert('RGB')

            width, height = image.size

            for y in range(0, height - 1, 2):
                line_parts = []
                for x in range(width):
                    top_pixel = RGB(*image.getpixel((x, y)))  # type: ignore
                    bottom_pixel = RGB(*image.getpixel((x, y + 1)))  # type: ignore

                    color_code = top_pixel.to_dual(bottom_pixel)
                    line_parts.append(f"{color_code}{IMAGE_CHARACTER}")

                lines.append(''.join(line_parts) + RESET)

            if height % 2 == 1:
                line_parts = []
                for x in range(width):
                    top_pixel = RGB(*image.getpixel((x, height - 1)))  # type: ignore
                    bottom_pixel = RGB(255, 255, 255)

                    color_code = top_pixel.to_dual(bottom_pixel)
                    line_parts.append(f"{color_code}{IMAGE_CHARACTER}")

                lines.append(''.join(line_parts) + RESET)

        return '\n'.join(lines)


# Aliases
img_to_ascii = ImageRenderer.image_to_ascii
