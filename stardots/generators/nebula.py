"""Interstellar nebula and cosmic gas cloud generator."""

import math
from typing import List, Optional, Tuple

from stardots.canvas import Canvas
from stardots.generators.base import BaseGenerator


class NebulaBlob:
    """A single Gaussian gas cloud puff."""

    def __init__(
        self,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        angle: float,
        weight: float,
    ) -> None:
        self.cx = cx
        self.cy = cy
        self.rx = max(1.0, rx)
        self.ry = max(1.0, ry)
        self.cos_a = math.cos(angle)
        self.sin_a = math.sin(angle)
        self.weight = weight

    def evaluate(self, x: float, y: float, aspect: float = 2.0) -> float:
        """Evaluate the gas puff intensity at (x, y)."""
        dx = x - self.cx
        dy = (y - self.cy) * aspect
        # Rotate coordinates
        rx_rot = dx * self.cos_a + dy * self.sin_a
        ry_rot = -dx * self.sin_a + dy * self.cos_a

        d2 = (rx_rot / self.rx) ** 2 + (ry_rot / self.ry) ** 2
        if d2 >= 1.0:
            return 0.0
        # Smooth cubic falloff
        return self.weight * ((1.0 - d2) ** 2)


class NebulaGenerator(BaseGenerator):
    """Generates cosmic gas nebulae with variable density, filaments, and embedded stars."""

    # Multi-level density gradient from faint gas to dense glowing core
    NEBULA_RAMP: Tuple[str, ...] = (" ", ".", ":", "-", "=", "+", "*", "#", "@")
    ASCII_RAMP: Tuple[str, ...] = (" ", ".", ":", "-", "=", "+", "*", "#", "@")

    def __init__(
        self,
        width: int = 80,
        height: int = 24,
        clusters: int = 5,
        use_ascii_only: bool = False,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__(width=width, height=height, seed=seed)
        self.clusters = max(1, clusters)
        self.use_ascii_only = use_ascii_only
        self.ramp = self.ASCII_RAMP if use_ascii_only else self.NEBULA_RAMP

    def _generate_blobs(self) -> List[NebulaBlob]:
        """Generate a collection of overlapping multi-scale gas puffs."""
        blobs: List[NebulaBlob] = []
        cx = self.width / 2.0
        cy = self.height / 2.0

        # Primary cluster centers around center of canvas
        for _ in range(self.clusters):
            # Cluster center displaced from origin
            dist = self.rng.uniform(0.1, 0.45)
            angle = self.rng.uniform(0, 2 * math.pi)
            cl_x = cx + dist * (self.width * 0.5) * math.cos(angle)
            cl_y = cy + dist * (self.height * 0.5) * math.sin(angle)

            # Cluster main puff
            rx = self.rng.uniform(self.width * 0.12, self.width * 0.30)
            ry = self.rng.uniform(self.height * 0.20, self.height * 0.45)
            rot = self.rng.uniform(0, math.pi)
            w = self.rng.uniform(0.6, 1.0)
            blobs.append(NebulaBlob(cl_x, cl_y, rx, ry, rot, w))

            # Satellite puffs around this cluster
            sub_count = self.rng.randint(2, 4)
            for _ in range(sub_count):
                sub_dist = self.rng.uniform(3.0, rx * 0.6)
                sub_ang = self.rng.uniform(0, 2 * math.pi)
                sx = cl_x + sub_dist * math.cos(sub_ang)
                sy = cl_y + (sub_dist / 2.0) * math.sin(sub_ang)
                srx = self.rng.uniform(rx * 0.35, rx * 0.75)
                sry = self.rng.uniform(ry * 0.35, ry * 0.75)
                srot = self.rng.uniform(0, math.pi)
                sw = self.rng.uniform(0.3, 0.7)
                blobs.append(NebulaBlob(sx, sy, srx, sry, srot, sw))

        return blobs

    def generate(self) -> Canvas:
        """Generate the nebula canvas."""
        canvas = Canvas(self.width, self.height)
        blobs = self._generate_blobs()

        # Generate harmonic perturbation parameters for filamentary texture
        f1 = self.rng.uniform(0.12, 0.28)
        f2 = self.rng.uniform(0.15, 0.35)
        p1 = self.rng.uniform(0, math.pi * 2)
        p2 = self.rng.uniform(0, math.pi * 2)

        # First pass: calculate raw gas densities
        densities: List[List[float]] = [[0.0 for _ in range(self.width)] for _ in range(self.height)]
        max_density = 0.0001

        aspect = 2.0
        for y in range(self.height):
            for x in range(self.width):
                # Sum puff contributions
                val = sum(b.evaluate(x, y, aspect=aspect) for b in blobs)

                # Filament harmonic wave
                wave = 1.0 + 0.25 * math.sin(f1 * x + p1) * math.cos(f2 * y + p2)
                density = val * wave

                densities[y][x] = density
                if density > max_density:
                    max_density = density

        # Second pass: normalize, map to characters, and seed proto-stars
        ramp_len = len(self.ramp)

        for y in range(self.height):
            for x in range(self.width):
                norm = densities[y][x] / max_density

                if norm < 0.08:
                    # Sparse background stars
                    if self.rng.random() < 0.015:
                        canvas.set(x, y, ".")
                    continue

                # Add mild stochastic texture so it looks granular like cosmic dust
                textured = norm + self.rng.uniform(-0.06, 0.06)
                clamped = max(0.0, min(1.0, textured))

                # Dense gas knots may collapse into bright new protostars!
                if clamped > 0.78 and self.rng.random() < 0.06:
                    star_char = self.rng.choice(["*", "+", "o", "O"])
                    canvas.set(x, y, star_char)
                    continue

                idx = int(clamped * (ramp_len - 1))
                char = self.ramp[idx]
                if char != " ":
                    canvas.set(x, y, char)

        return canvas
