"""Tests for text export and file collision handling."""

import shutil
import tempfile
import unittest
from pathlib import Path

from stardots.export import (
    ExportError,
    export_artwork,
    generate_descriptive_filename,
    resolve_output_path,
    sanitize_filename,
)


class TestExport(unittest.TestCase):
    """Test filesystem export and collision avoidance."""

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_sanitize_filename(self) -> None:
        """Sanitizes illegal filesystem characters."""
        self.assertEqual(sanitize_filename("star:field/one?*"), "star_field_one")
        self.assertEqual(sanitize_filename("   "), "artwork")

    def test_generate_descriptive_filename(self) -> None:
        """Generates filename starting with prefix and ending with .txt."""
        name = generate_descriptive_filename("galaxy")
        self.assertTrue(name.startswith("galaxy_"))
        self.assertTrue(name.endswith(".txt"))

    def test_export_success_and_content(self) -> None:
        """Export saves UTF-8 string faithfully."""
        content = "   *   \n  ***  \n   *   "
        target = self.temp_dir / "test_out.txt"
        saved = export_artwork(content, destination=target)
        self.assertTrue(saved.exists())
        self.assertEqual(saved.read_text(encoding="utf-8").strip(), content.strip())

    def test_collision_error_strategy(self) -> None:
        """Collision raises ExportError when conflict_strategy='error' and allow_overwrite=False."""
        target = self.temp_dir / "collision.txt"
        target.write_text("initial", encoding="utf-8")

        with self.assertRaises(ExportError):
            export_artwork("new content", destination=target, allow_overwrite=False, conflict_strategy="error")

    def test_collision_auto_rename_strategy(self) -> None:
        """Collision auto-renames with index suffix when strategy='auto_rename'."""
        target = self.temp_dir / "artwork.txt"
        target.write_text("initial", encoding="utf-8")

        saved = export_artwork("new", destination=target, allow_overwrite=False, conflict_strategy="auto_rename")
        self.assertNotEqual(saved, target)
        self.assertEqual(saved.name, "artwork_1.txt")
        self.assertTrue(saved.exists())
        self.assertEqual(target.read_text(encoding="utf-8"), "initial")

    def test_overwrite_allowed(self) -> None:
        """allow_overwrite=True safely replaces existing file."""
        target = self.temp_dir / "overwrite.txt"
        target.write_text("old", encoding="utf-8")

        saved = export_artwork("new", destination=target, allow_overwrite=True)
        self.assertEqual(saved, target)
        self.assertEqual(target.read_text(encoding="utf-8").strip(), "new")

    def test_invalid_artwork_type(self) -> None:
        """Non-string artwork raises ValueError."""
        with self.assertRaises(ValueError):
            export_artwork(12345, destination=self.temp_dir / "bad.txt")  # type: ignore


if __name__ == "__main__":
    unittest.main()
