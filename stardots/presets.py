"""Preset definitions and registry for celestial formations."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CelestialPreset:
    """A configured celestial preset that can be generated directly."""
    key: str
    category: str  # "constellation", "galaxy", "nebula", "starfield"
    title: str
    description: str
    parameters: Dict[str, Any]


PRESET_CATALOG: Dict[str, CelestialPreset] = {
    # Constellations
    "orion": CelestialPreset(
        key="orion",
        category="constellation",
        title="Orion (The Hunter)",
        description="Features Betelgeuse, Rigel, Bellatrix, Saiph, and the three belt stars.",
        parameters={"preset": "orion", "width": 80, "height": 24, "show_labels": True},
    ),
    "big-dipper": CelestialPreset(
        key="big-dipper",
        category="constellation",
        title="The Big Dipper (Ursa Major Asterism)",
        description="The famous seven-star celestial ladle and pointers to Polaris.",
        parameters={"preset": "big-dipper", "width": 80, "height": 24, "show_labels": True},
    ),
    "cassiopeia": CelestialPreset(
        key="cassiopeia",
        category="constellation",
        title="Cassiopeia (The Queen)",
        description="A distinctive five-star W pattern traversing the northern sky.",
        parameters={"preset": "cassiopeia", "width": 80, "height": 24, "show_labels": True},
    ),

    # Galaxies
    "milky-way": CelestialPreset(
        key="milky-way",
        category="galaxy",
        title="Milky Way Spiral",
        description="Grand design two-armed barred spiral galaxy with a glowing nucleus.",
        parameters={"width": 100, "height": 30, "arms": 2, "winding": 2.4, "seed": 42},
    ),
    "triangulum": CelestialPreset(
        key="triangulum",
        category="galaxy",
        title="Triangulum Pinwheel",
        description="A three-armed dynamic spiral galaxy (M33) with expansive outer arms.",
        parameters={"width": 90, "height": 28, "arms": 3, "winding": 2.2, "seed": 108},
    ),
    "whirlpool": CelestialPreset(
        key="whirlpool",
        category="galaxy",
        title="Whirlpool Galaxy (M51)",
        description="Tight classical spiral with prominent tidal arms and dense core.",
        parameters={"width": 100, "height": 32, "arms": 2, "winding": 3.2, "seed": 51},
    ),

    # Nebulae
    "orion-nebula": CelestialPreset(
        key="orion-nebula",
        category="nebula",
        title="Great Orion Nebula (M42)",
        description="Diffuse stellar nursery with dense ionizing gas knots and newborn stars.",
        parameters={"width": 80, "height": 24, "clusters": 6, "seed": 42},
    ),
    "crab-nebula": CelestialPreset(
        key="crab-nebula",
        category="nebula",
        title="Crab Supernova Remnant (M1)",
        description="Chaotic expanding synchrotron filaments and energetic central pulsar.",
        parameters={"width": 80, "height": 24, "clusters": 7, "seed": 1054},
    ),

    # Starfields
    "deep-field": CelestialPreset(
        key="deep-field",
        category="starfield",
        title="Cosmic Deep Field",
        description="A sparse, high-contrast expanse of distant glimmering points.",
        parameters={"width": 80, "height": 24, "density": 0.04, "seed": 777},
    ),
    "dense-cluster": CelestialPreset(
        key="dense-cluster",
        category="starfield",
        title="Dense Star Cluster",
        description="Rich, crowded field of sparkling celestial bodies.",
        parameters={"width": 80, "height": 24, "density": 0.16, "seed": 999},
    ),
}


def list_all_presets() -> List[CelestialPreset]:
    """Return all catalog presets."""
    return list(PRESET_CATALOG.values())


def get_preset(key: str) -> Optional[CelestialPreset]:
    """Retrieve a preset by key or alias."""
    norm = key.strip().lower().replace("_", "-")
    return PRESET_CATALOG.get(norm)
