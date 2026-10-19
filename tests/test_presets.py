"""Tests for Preset registry and catalog lookup."""

import unittest
from stardots.presets import PRESET_CATALOG, get_preset, list_all_presets


class TestPresets(unittest.TestCase):
    """Test preset catalog retrieval and structure."""

    def test_catalog_non_empty(self) -> None:
        """Catalog has registered presets across categories."""
        presets = list_all_presets()
        self.assertGreaterEqual(len(presets), 8)
        categories = {p.category for p in presets}
        self.assertIn("constellation", categories)
        self.assertIn("galaxy", categories)
        self.assertIn("nebula", categories)
        self.assertIn("starfield", categories)

    def test_get_preset_case_insensitivity(self) -> None:
        """Preset retrieval handles case and underscores/hyphens."""
        self.assertIsNotNone(get_preset("orion"))
        self.assertIsNotNone(get_preset("ORION"))
        self.assertIsNotNone(get_preset("big-dipper"))
        self.assertIsNotNone(get_preset("big_dipper"))
        self.assertIsNotNone(get_preset("milky-way"))

    def test_get_unknown_preset(self) -> None:
        """Unknown preset returns None."""
        self.assertIsNone(get_preset("nonexistent-preset-12345"))


if __name__ == "__main__":
    unittest.main()
