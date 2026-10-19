"""Constellation generator supporting Orion, Big Dipper, and custom star patterns."""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from stardots.canvas import Canvas
from stardots.generators.base import BaseGenerator
from stardots.palette import DEFAULT_STAR_PALETTE


@dataclass
class ConstellationStar:
    """A star in a constellation."""
    name: str
    x_ratio: float  # Normalized 0.0 to 1.0 within bounding box
    y_ratio: float  # Normalized 0.0 to 1.0 within bounding box
    symbol: str = "o"
    label_offset: Tuple[int, int] = (2, 0)  # (dx, dy) for label placement


@dataclass
class ConstellationPreset:
    """Predefined constellation data."""
    name: str
    description: str
    stars: List[ConstellationStar]
    lines: List[Tuple[str, str]]  # Pairs of star names to connect


# Predefined Orion Constellation
ORION_PRESET = ConstellationPreset(
    name="orion",
    description="The Hunter, featuring Betelgeuse, Rigel, and Orion's Belt",
    stars=[
        ConstellationStar("Betelgeuse", 0.20, 0.15, symbol="*", label_offset=(2, 0)),
        ConstellationStar("Bellatrix", 0.80, 0.18, symbol="*", label_offset=(2, 0)),
        ConstellationStar("Alnitak", 0.40, 0.48, symbol="o", label_offset=(-8, -1)),
        ConstellationStar("Alnilam", 0.50, 0.50, symbol="o", label_offset=(2, -1)),
        ConstellationStar("Mintaka", 0.60, 0.52, symbol="o", label_offset=(2, 0)),
        ConstellationStar("Saiph", 0.28, 0.85, symbol="*", label_offset=(2, 0)),
        ConstellationStar("Rigel", 0.76, 0.82, symbol="*", label_offset=(2, 0)),
        ConstellationStar("Meissa", 0.50, 0.05, symbol="+", label_offset=(2, 0)),
    ],
    lines=[
        # Shoulders to head
        ("Betelgeuse", "Meissa"),
        ("Bellatrix", "Meissa"),
        # Shoulders to belt
        ("Betelgeuse", "Alnitak"),
        ("Bellatrix", "Mintaka"),
        # Belt
        ("Alnitak", "Alnilam"),
        ("Alnilam", "Mintaka"),
        # Belt to feet
        ("Alnitak", "Saiph"),
        ("Mintaka", "Rigel"),
        # Base between feet
        ("Saiph", "Rigel"),
    ],
)

# Predefined Big Dipper (Ursa Major asterism)
BIG_DIPPER_PRESET = ConstellationPreset(
    name="big-dipper",
    description="The Big Dipper / Plough asterism in Ursa Major",
    stars=[
        # Handle (from tip inwards)
        ConstellationStar("Alkaid", 0.05, 0.70, symbol="*", label_offset=(2, 0)),
        ConstellationStar("Mizar", 0.20, 0.58, symbol="*", label_offset=(2, -1)),
        ConstellationStar("Alioth", 0.35, 0.52, symbol="*", label_offset=(2, 1)),
        # Bowl
        ConstellationStar("Megrez", 0.52, 0.44, symbol="o", label_offset=(2, -1)),
        ConstellationStar("Phecda", 0.55, 0.85, symbol="o", label_offset=(2, 0)),
        ConstellationStar("Merak", 0.86, 0.82, symbol="*", label_offset=(2, 0)),
        ConstellationStar("Dubhe", 0.88, 0.42, symbol="*", label_offset=(2, 0)),
    ],
    lines=[
        ("Alkaid", "Mizar"),
        ("Mizar", "Alioth"),
        ("Alioth", "Megrez"),
        ("Megrez", "Phecda"),
        ("Phecda", "Merak"),
        ("Merak", "Dubhe"),
        ("Dubhe", "Megrez"),
    ],
)

# Predefined Cassiopeia (W pattern)
CASSIOPEIA_PRESET = ConstellationPreset(
    name="cassiopeia",
    description="The Queen of the Night Sky, distinct W-shaped asterism",
    stars=[
        ConstellationStar("Caph", 0.10, 0.70, symbol="*", label_offset=(2, 0)),
        ConstellationStar("Schedar", 0.32, 0.30, symbol="*", label_offset=(2, -1)),
        ConstellationStar("Navi", 0.52, 0.55, symbol="o", label_offset=(2, 0)),
        ConstellationStar("Ruchbah", 0.75, 0.25, symbol="*", label_offset=(2, -1)),
        ConstellationStar("Segin", 0.90, 0.65, symbol="+", label_offset=(2, 0)),
    ],
    lines=[
        ("Caph", "Schedar"),
        ("Schedar", "Navi"),
        ("Navi", "Ruchbah"),
        ("Ruchbah", "Segin"),
    ],
)

CONSTELLATION_PRESETS: Dict[str, ConstellationPreset] = {
    "orion": ORION_PRESET,
    "big-dipper": BIG_DIPPER_PRESET,
    "big_dipper": BIG_DIPPER_PRESET,
    "plough": BIG_DIPPER_PRESET,
    "cassiopeia": CASSIOPEIA_PRESET,
}


class ConstellationGenerator(BaseGenerator):
    """Generates constellations with connection lines and optional star labels."""

    def __init__(
        self,
        preset: str = "orion",
        width: int = 80,
        height: int = 24,
        show_labels: bool = True,
        background_density: float = 0.02,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__(width=width, height=height, seed=seed)
        norm_key = preset.strip().lower().replace("_", "-")
        if norm_key not in CONSTELLATION_PRESETS:
            valid = ", ".join(sorted({p.name for p in CONSTELLATION_PRESETS.values()}))
            raise ValueError(f"Unknown preset '{preset}'. Available presets: {valid}")

        self.preset_data = CONSTELLATION_PRESETS[norm_key]
        self.show_labels = show_labels
        self.background_density = background_density

    def generate(self) -> Canvas:
        """Render the constellation onto a new canvas."""
        canvas = Canvas(self.width, self.height)

        # 1. Populate faint background stars if density > 0
        if self.background_density > 0:
            total_cells = self.width * self.height
            bg_stars = int(round(total_cells * self.background_density))
            all_coords = [(x, y) for y in range(self.height) for x in range(self.width)]
            for x, y in self.rng.sample(all_coords, min(bg_stars, total_cells)):
                canvas.set(x, y, ".")

        # 2. Compute margin and bounding box for constellation stars
        margin_x = max(2, int(self.width * 0.12))
        margin_y = max(2, int(self.height * 0.12))
        usable_w = max(4, self.width - 2 * margin_x)
        usable_h = max(4, self.height - 2 * margin_y)

        # Map stars to canvas coordinates
        star_positions: Dict[str, Tuple[int, int]] = {}
        for star in self.preset_data.stars:
            sx = margin_x + int(round(star.x_ratio * (usable_w - 1)))
            sy = margin_y + int(round(star.y_ratio * (usable_h - 1)))
            # Clamp coordinates inside canvas
            sx = max(0, min(self.width - 1, sx))
            sy = max(0, min(self.height - 1, sy))
            star_positions[star.name] = (sx, sy)

        # 3. Draw connection lines between stars FIRST, or protect stars
        # To avoid overwriting stars, we first place and protect the stars
        for star in self.preset_data.stars:
            sx, sy = star_positions[star.name]
            canvas.set(sx, sy, star.symbol, protect=True, overwrite_protected=True)

        # Draw lines, respecting protected star points
        for start_name, end_name in self.preset_data.lines:
            if start_name in star_positions and end_name in star_positions:
                x0, y0 = star_positions[start_name]
                x1, y1 = star_positions[end_name]
                canvas.draw_line(x0, y0, x1, y1, avoid_protected=True, use_directional_chars=True)

        # Re-ensure stars are rendered cleanly in case of overlap
        for star in self.preset_data.stars:
            sx, sy = star_positions[star.name]
            canvas.set(sx, sy, star.symbol, protect=True, overwrite_protected=True)

        # 4. Draw optional labels
        if self.show_labels:
            for star in self.preset_data.stars:
                sx, sy = star_positions[star.name]
                dx, dy = star.label_offset
                label_x = sx + dx
                label_y = sy + dy

                # If label runs off right edge, shift it left
                if label_x + len(star.name) >= self.width:
                    label_x = max(0, sx - len(star.name) - 1)
                label_x = max(0, label_x)
                label_y = max(0, min(self.height - 1, label_y))

                canvas.draw_text(label_x, label_y, star.name)

        return canvas
