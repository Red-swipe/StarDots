"""Tests for StarDots universe artwork generators."""

import unittest
from stardots.generators.constellation import (
    BIG_DIPPER_PRESET,
    CASSIOPEIA_PRESET,
    CONSTELLATION_PRESETS,
    ConstellationGenerator,
    ORION_PRESET,
)
from stardots.generators.galaxy import SpiralGalaxyGenerator
from stardots.generators.nebula import NebulaGenerator
from stardots.generators.starfield import StarfieldGenerator


class TestStarfieldGenerator(unittest.TestCase):
    """Test StarfieldGenerator."""

    def test_dimensions(self) -> None:
        """Starfield respects requested dimensions."""
        gen = StarfieldGenerator(width=60, height=20, density=0.1, seed=42)
        lines = gen.render().splitlines()
        self.assertEqual(len(lines), 20)
        self.assertTrue(all(len(line) == 60 for line in lines))

    def test_determinism(self) -> None:
        """Seeded starfield generation is strictly deterministic."""
        s1 = StarfieldGenerator(width=40, height=12, density=0.1, seed=12345).render()
        s2 = StarfieldGenerator(width=40, height=12, density=0.1, seed=12345).render()
        self.assertEqual(s1, s2)

    def test_unseeded_variation(self) -> None:
        """Unseeded starfields produce varied output."""
        s1 = StarfieldGenerator(width=40, height=12, density=0.15).render()
        s2 = StarfieldGenerator(width=40, height=12, density=0.15).render()
        self.assertNotEqual(s1, s2)

    def test_custom_palette(self) -> None:
        """Starfield uses characters from custom palette."""
        palette = ["#", "$"]
        gen = StarfieldGenerator(width=30, height=10, density=0.2, palette=palette, seed=42)
        rendered = gen.render()
        chars = set(rendered) - {" ", "\n"}
        self.assertTrue(chars.issubset(set(palette)))

    def test_invalid_parameters(self) -> None:
        """Invalid density or empty palette raises ValueError."""
        with self.assertRaises(ValueError):
            StarfieldGenerator(width=40, height=10, density=0.0)
        with self.assertRaises(ValueError):
            StarfieldGenerator(width=40, height=10, density=1.5)
        with self.assertRaises(ValueError):
            StarfieldGenerator(width=40, height=10, palette=[])


class TestConstellationGenerator(unittest.TestCase):
    """Test ConstellationGenerator."""

    def test_orion_generation(self) -> None:
        """Orion constellation contains key stars."""
        gen = ConstellationGenerator(preset="orion", width=80, height=24, show_labels=True, seed=42)
        rendered = gen.render()
        self.assertIn("Betelgeuse", rendered)
        self.assertIn("Rigel", rendered)
        self.assertIn("Mintaka", rendered)

    def test_big_dipper_generation(self) -> None:
        """Big Dipper constellation contains key stars."""
        gen = ConstellationGenerator(preset="big-dipper", width=80, height=24, show_labels=True, seed=42)
        rendered = gen.render()
        self.assertIn("Dubhe", rendered)
        self.assertIn("Merak", rendered)
        self.assertIn("Alkaid", rendered)

    def test_cassiopeia_generation(self) -> None:
        """Cassiopeia contains Caph and Schedar."""
        gen = ConstellationGenerator(preset="cassiopeia", width=80, height=24, show_labels=True, seed=42)
        rendered = gen.render()
        self.assertIn("Caph", rendered)
        self.assertIn("Schedar", rendered)

    def test_no_labels_option(self) -> None:
        """Omission of star labels."""
        gen = ConstellationGenerator(preset="orion", width=80, height=24, show_labels=False, seed=42)
        rendered = gen.render()
        self.assertNotIn("Betelgeuse", rendered)
        self.assertNotIn("Rigel", rendered)

    def test_unknown_preset(self) -> None:
        """Unknown constellation preset raises ValueError."""
        with self.assertRaises(ValueError):
            ConstellationGenerator(preset="unknown-constellation")

    def test_determinism(self) -> None:
        """Seeded background stars in constellation are deterministic."""
        c1 = ConstellationGenerator(preset="orion", width=60, height=20, seed=999).render()
        c2 = ConstellationGenerator(preset="orion", width=60, height=20, seed=999).render()
        self.assertEqual(c1, c2)


class TestSpiralGalaxyGenerator(unittest.TestCase):
    """Test SpiralGalaxyGenerator."""

    def test_galaxy_dimensions(self) -> None:
        """Galaxy respects width and height."""
        gen = SpiralGalaxyGenerator(width=90, height=25, arms=2, seed=42)
        lines = gen.render().splitlines()
        self.assertEqual(len(lines), 25)
        self.assertTrue(all(len(l) == 90 for l in lines))

    def test_arm_variations(self) -> None:
        """Galaxy supports multiple arms (1, 2, 3, 4)."""
        for arm_count in (1, 2, 3, 4):
            gen = SpiralGalaxyGenerator(width=60, height=20, arms=arm_count, seed=42)
            rendered = gen.render()
            self.assertGreater(len(rendered), 0)

    def test_invalid_arms(self) -> None:
        """Arms < 1 raises ValueError."""
        with self.assertRaises(ValueError):
            SpiralGalaxyGenerator(width=60, height=20, arms=0)

    def test_galaxy_determinism(self) -> None:
        """Seeded galaxy is deterministic."""
        g1 = SpiralGalaxyGenerator(width=70, height=20, arms=2, seed=777).render()
        g2 = SpiralGalaxyGenerator(width=70, height=20, arms=2, seed=777).render()
        self.assertEqual(g1, g2)


class TestNebulaGenerator(unittest.TestCase):
    """Test NebulaGenerator."""

    def test_nebula_dimensions(self) -> None:
        """Nebula respects dimensions."""
        gen = NebulaGenerator(width=75, height=22, clusters=5, seed=42)
        lines = gen.render().splitlines()
        self.assertEqual(len(lines), 22)
        self.assertTrue(all(len(l) == 75 for l in lines))

    def test_ascii_only_mode(self) -> None:
        """ASCII only mode uses pure standard ASCII characters."""
        gen = NebulaGenerator(width=50, height=15, use_ascii_only=True, seed=42)
        rendered = gen.render()
        for ch in rendered:
            self.assertLess(ord(ch), 128, f"Non-ASCII character found: {ch}")

    def test_nebula_determinism(self) -> None:
        """Seeded nebula is deterministic."""
        n1 = NebulaGenerator(width=60, height=20, clusters=4, seed=555).render()
        n2 = NebulaGenerator(width=60, height=20, clusters=4, seed=555).render()
        self.assertEqual(n1, n2)


if __name__ == "__main__":
    unittest.main()
