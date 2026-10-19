"""Spiral galaxy generator with configurable arm count, core density, and aspect scaling."""

import math
from typing import List, Optional, Tuple

from stardots.canvas import Canvas
from stardots.generators.base import BaseGenerator


def _angle_diff(a: float, b: float) -> float:
    """Compute minimum absolute angular difference in [-pi, pi]."""
    diff = (a - b + math.pi) % (2 * math.pi) - math.pi
    return abs(diff)


class SpiralGalaxyGenerator(BaseGenerator):
    """Generates a spiral galaxy with mathematical spiral arms and glowing core."""

    def __init__(
        self,
        width: int = 100,
        height: int = 30,
        arms: int = 2,
        winding: float = 2.4,
        core_radius_ratio: float = 0.18,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__(width=width, height=height, seed=seed)
        if arms < 1:
            raise ValueError(f"Galaxy must have at least 1 spiral arm, got {arms}")
        self.arms = arms
        self.winding = winding
        self.core_radius_ratio = core_radius_ratio

    def generate(self) -> Canvas:
        """Generate the spiral galaxy canvas."""
        canvas = Canvas(self.width, self.height)

        cx = (self.width - 1) / 2.0
        cy = (self.height - 1) / 2.0

        # Account for typical terminal character aspect ratio (~2:1 vertical:horizontal)
        aspect = 2.0
        max_r_x = cx * 0.95
        max_r_y = (cy * aspect) * 0.95
        max_r = max(4.0, min(max_r_x, max_r_y))
        core_r = max(1.5, max_r * self.core_radius_ratio)

        arm_spacing = (2.0 * math.pi) / self.arms

        for y in range(self.height):
            for x in range(self.width):
                dx = x - cx
                dy = (y - cy) * aspect
                r = math.hypot(dx, dy)

                if r > max_r * 1.08:
                    # Outer space: sparse background stars
                    if self.rng.random() < 0.015:
                        canvas.set(x, y, ".")
                    continue

                phi = math.atan2(dy, dx)

                # Normalized radius from 0 to 1
                norm_r = r / max_r

                # Logarithmic / power winding angle for arms
                arm_theta_base = self.winding * math.pow(norm_r, 0.75) * math.pi

                # Distance to closest spiral arm
                min_arm_dist = math.pi
                for a in range(self.arms):
                    arm_angle = a * arm_spacing + arm_theta_base
                    dist = _angle_diff(phi, arm_angle)
                    if dist < min_arm_dist:
                        min_arm_dist = dist

                # Intensity components
                # Core intensity (Gaussian falloff)
                core_intensity = math.exp(-((r / core_r) ** 2))

                # Arm intensity (angular Gaussian + radial envelope)
                arm_thickness = 0.28 + 0.12 * norm_r
                arm_angular_falloff = math.exp(-((min_arm_dist / arm_thickness) ** 2))
                arm_radial_envelope = math.exp(-1.4 * norm_r) * (norm_r / (norm_r + 0.15))
                arm_intensity = arm_angular_falloff * arm_radial_envelope

                # Disc / halo background glow
                disc_glow = 0.10 * math.exp(-2.0 * norm_r)

                total_intensity = core_intensity * 1.2 + arm_intensity * 0.9 + disc_glow

                # Add small stochastic variation to avoid rigid banding
                jitter = self.rng.uniform(0.8, 1.25)
                effective = total_intensity * jitter

                # Map intensity to characters
                if r <= 1.2:
                    char = "@"
                elif effective > 0.85:
                    char = self.rng.choice(["@", "O", "*"])
                elif effective > 0.58:
                    char = self.rng.choice(["*", "o", "+"])
                elif effective > 0.38:
                    char = self.rng.choice(["+", "*", ":"])
                elif effective > 0.20:
                    char = self.rng.choice([".", ":"])
                elif effective > 0.10:
                    char = "." if self.rng.random() < 0.65 else " "
                else:
                    char = "." if self.rng.random() < 0.01 else " "

                if char != " ":
                    canvas.set(x, y, char)

        return canvas
