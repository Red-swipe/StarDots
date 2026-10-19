"""Random starfield generator."""

from typing import List, Optional, Sequence

from stardots.canvas import Canvas
from stardots.generators.base import BaseGenerator
from stardots.palette import DEFAULT_STAR_PALETTE


class StarfieldGenerator(BaseGenerator):
    """Generates random rectangular starfields with configurable density and palette."""

    def __init__(
        self,
        width: int = 80,
        height: int = 24,
        density: float = 0.08,
        palette: Optional[Sequence[str]] = None,
        palette_weights: Optional[Sequence[float]] = None,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__(width=width, height=height, seed=seed)
        if not (0.0 < density <= 1.0):
            raise ValueError(f"Density must be between 0.0 (exclusive) and 1.0 (inclusive), got {density}")
        self.density = density
        self.palette = list(palette) if palette else list(DEFAULT_STAR_PALETTE)
        if not self.palette:
            raise ValueError("Palette cannot be empty")

        if palette_weights is not None:
            if len(palette_weights) != len(self.palette):
                raise ValueError("palette_weights must match length of palette")
            self.palette_weights = list(palette_weights)
        else:
            # Default astronomical weighting: faintest stars are most common
            # e.g. for ['.', '*', '+', 'o'], weights = [65, 20, 10, 5]
            n = len(self.palette)
            if n == 4:
                self.palette_weights = [60.0, 25.0, 10.0, 5.0]
            else:
                # Geometric decrease for arbitrary length palette
                self.palette_weights = [1.0 / (2**i) for i in range(n)]

    def generate(self) -> Canvas:
        """Generate the starfield canvas."""
        canvas = Canvas(self.width, self.height)
        total_cells = self.width * self.height
        target_stars = int(round(total_cells * self.density))

        # Sample unique coordinates to avoid collisions
        all_coords = [(x, y) for y in range(self.height) for x in range(self.width)]
        star_coords = self.rng.sample(all_coords, min(target_stars, total_cells))

        for x, y in star_coords:
            char = self.rng.choices(self.palette, weights=self.palette_weights, k=1)[0]
            canvas.set(x, y, char)

        return canvas
