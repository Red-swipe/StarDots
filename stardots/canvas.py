"""Canvas representation for 2D character grids in StarDots."""

from typing import Callable, Iterable, List, Optional, Set, Tuple


class Canvas:
    """A 2D character canvas for plotting ASCII and Unicode space artwork."""

    def __init__(self, width: int, height: int, fill_char: str = " ") -> None:
        if width <= 0 or height <= 0:
            raise ValueError(f"Canvas dimensions must be positive integers: width={width}, height={height}")
        self.width = width
        self.height = height
        self.fill_char = fill_char
        self.grid: List[List[str]] = [[fill_char for _ in range(width)] for _ in range(height)]
        # Track locked coordinates (e.g. stars in constellations) that shouldn't be overwritten
        self._protected_coords: Set[Tuple[int, int]] = set()

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) is within canvas bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, x: int, y: int) -> Optional[str]:
        """Get character at (x, y) or None if out of bounds."""
        if self.in_bounds(x, y):
            return self.grid[y][x]
        return None

    def set(self, x: int, y: int, char: str, protect: bool = False, overwrite_protected: bool = False) -> bool:
        """Set character at (x, y).

        Args:
            x: Horizontal position (0 to width - 1).
            y: Vertical position (0 to height - 1).
            char: Single character or string to place.
            protect: If True, marks this coordinate as protected from overwrite.
            overwrite_protected: If False, will not overwrite already protected coordinates.

        Returns:
            True if character was successfully set, False otherwise.
        """
        if not self.in_bounds(x, y):
            return False
        if not overwrite_protected and (x, y) in self._protected_coords:
            return False
        self.grid[y][x] = char
        if protect:
            self._protected_coords.add((x, y))
        return True

    def protect(self, x: int, y: int) -> None:
        """Mark coordinate (x, y) as protected."""
        if self.in_bounds(x, y):
            self._protected_coords.add((x, y))

    def is_protected(self, x: int, y: int) -> bool:
        """Check if coordinate is protected."""
        return (x, y) in self._protected_coords

    def draw_text(self, x: int, y: int, text: str, protect: bool = False, overwrite_protected: bool = False) -> None:
        """Draw horizontal text starting at (x, y)."""
        for i, ch in enumerate(text):
            tx = x + i
            if self.in_bounds(tx, y):
                self.set(tx, y, ch, protect=protect, overwrite_protected=overwrite_protected)

    def draw_line(
        self,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        char: Optional[str] = None,
        avoid_protected: bool = True,
        use_directional_chars: bool = True,
    ) -> None:
        """Draw a line between two points using Bresenham's algorithm.

        Args:
            x0: Start x.
            y0: Start y.
            x1: End x.
            y1: End y.
            char: Fixed character to use. If None and use_directional_chars is True,
                  chooses among '-', '|', '/', '\\' based on line angle.
            avoid_protected: Avoid replacing protected coordinates (like star points).
            use_directional_chars: Automatically pick connection characters.
        """
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        # Determine directional character if none provided
        line_char = char
        if line_char is None and use_directional_chars:
            if dx == 0:
                line_char = "|"
            elif dy == 0:
                line_char = "-"
            else:
                # Terminal character aspect ratio is typically ~2:1 (height:width).
                # Take aspect ratio into account for diagonal visual slope.
                slope = (y1 - y0) / (x1 - x0)
                if abs(slope) < 0.35:
                    line_char = "-"
                elif abs(slope) > 2.5:
                    line_char = "|"
                elif slope > 0:
                    line_char = "\\"
                else:
                    line_char = "/"

        curr_x, curr_y = x0, y0
        while True:
            # Skip endpoint if it's protected or starting point
            is_endpoint = (curr_x == x0 and curr_y == y0) or (curr_x == x1 and curr_y == y1)
            if not (is_endpoint and avoid_protected and self.is_protected(curr_x, curr_y)):
                self.set(curr_x, curr_y, line_char or "*", overwrite_protected=not avoid_protected)

            if curr_x == x1 and curr_y == y1:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                curr_x += sx
            if e2 < dx:
                err += dx
                curr_y += sy

    def render(self) -> str:
        """Convert the 2D grid into a multi-line string."""
        return "\n".join("".join(row) for row in self.grid)
