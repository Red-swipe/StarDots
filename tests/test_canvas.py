"""Tests for Canvas and rendering utilities."""

import unittest
from stardots.canvas import Canvas, get_terminal_canvas_size


class TestCanvas(unittest.TestCase):
    """Test 2D Canvas functionality."""

    def test_dimensions_validation(self) -> None:
        """Canvas rejects non-positive dimensions."""
        with self.assertRaises(ValueError):
            Canvas(0, 10)
        with self.assertRaises(ValueError):
            Canvas(10, -5)

    def test_initial_grid(self) -> None:
        """Canvas initializes filled with specified character."""
        canvas = Canvas(5, 3, fill_char=" ")
        lines = canvas.render().splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines, ["     ", "     ", "     "])

    def test_set_and_get(self) -> None:
        """Setting characters inside and outside bounds."""
        canvas = Canvas(4, 4)
        self.assertTrue(canvas.set(1, 1, "*"))
        self.assertEqual(canvas.get(1, 1), "*")
        # Out of bounds
        self.assertFalse(canvas.set(-1, 0, "x"))
        self.assertFalse(canvas.set(4, 2, "x"))
        self.assertIsNone(canvas.get(10, 10))

    def test_protected_coordinates(self) -> None:
        """Protected coordinates cannot be overwritten when protected."""
        canvas = Canvas(5, 5)
        canvas.set(2, 2, "o", protect=True)
        self.assertTrue(canvas.is_protected(2, 2))
        # Attempt overwrite with overwrite_protected=False
        canvas.set(2, 2, "-", overwrite_protected=False)
        self.assertEqual(canvas.get(2, 2), "o")
        # Overwrite with overwrite_protected=True
        canvas.set(2, 2, "*", overwrite_protected=True)
        self.assertEqual(canvas.get(2, 2), "*")

    def test_draw_line(self) -> None:
        """Bresenham line drawing connects points correctly."""
        canvas = Canvas(10, 10)
        canvas.draw_line(0, 0, 4, 0, char="-")
        rendered = canvas.render().splitlines()[0]
        self.assertEqual(rendered[:5], "-----")

    def test_directional_chars(self) -> None:
        """Line drawing picks appropriate directional character."""
        # Horizontal
        c1 = Canvas(5, 5)
        c1.draw_line(0, 2, 4, 2, use_directional_chars=True)
        self.assertEqual(c1.get(2, 2), "-")

        # Vertical
        c2 = Canvas(5, 5)
        c2.draw_line(2, 0, 2, 4, use_directional_chars=True)
        self.assertEqual(c2.get(2, 2), "|")

    def test_draw_text(self) -> None:
        """Drawing text renders horizontally."""
        canvas = Canvas(12, 3)
        canvas.draw_text(2, 1, "ORION")
        line = canvas.render().splitlines()[1]
        self.assertEqual(line[2:7], "ORION")

    def test_terminal_canvas_size(self) -> None:
        """get_terminal_canvas_size returns positive dimensions."""
        w, h = get_terminal_canvas_size(fallback_w=80, fallback_h=24)
        self.assertGreaterEqual(w, 10)
        self.assertGreaterEqual(h, 5)


if __name__ == "__main__":
    unittest.main()
