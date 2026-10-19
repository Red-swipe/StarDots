"""Palettes and character sets for StarDots generators."""

from typing import List, Tuple

# Default star palette ordered from faintest to brightest
DEFAULT_STAR_PALETTE: Tuple[str, ...] = (".", "*", "+", "o")

# High density / diverse star palette with Unicode support
UNICODE_STAR_PALETTE: Tuple[str, ...] = ("·", "•", "✦", "★", "✧", "✶")

# ASCII gradient from low to high density/brightness
ASCII_SHADING_GRADIENT: Tuple[str, ...] = (" ", ".", ":", "-", "=", "+", "*", "#", "%", "@")

# Smooth Unicode shading gradient
UNICODE_SHADING_GRADIENT: Tuple[str, ...] = (" ", "░", "▒", "▓", "█")

# Star symbols by brightness level
STAR_LEVELS = {
    "dim": (".", "·"),
    "medium": ("*", "x", "+"),
    "bright": ("o", "O", "★", "@"),
}
