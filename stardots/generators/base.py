"""Base generator class with isolated random number generation."""

import random
from abc import ABC, abstractmethod
from typing import Optional

from stardots.canvas import Canvas


class BaseGenerator(ABC):
    """Abstract base class for all universe artwork generators."""

    def __init__(self, width: int = 80, height: int = 24, seed: Optional[int] = None) -> None:
        if width <= 0 or height <= 0:
            raise ValueError(f"Dimensions must be positive integers: width={width}, height={height}")
        self.width = width
        self.height = height
        self.seed = seed
        self.rng = random.Random(seed)

    @abstractmethod
    def generate(self) -> Canvas:
        """Generate artwork on a Canvas instance and return it."""
        pass

    def render(self) -> str:
        """Convenience method to generate and return the rendered string."""
        return self.generate().render()
