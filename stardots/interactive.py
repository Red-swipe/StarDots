"""Interactive terminal menu for StarDots — ASCII Universe Generator."""

import sys
from typing import Optional

from stardots.generators.constellation import ConstellationGenerator
from stardots.generators.galaxy import SpiralGalaxyGenerator
from stardots.generators.nebula import NebulaGenerator
from stardots.generators.starfield import StarfieldGenerator
from stardots.presets import PRESET_CATALOG, list_all_presets


def _prompt_int(prompt_text: str, default: int, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """Prompt user for an integer with default and bounds validation."""
    while True:
        try:
            raw = input(f"{prompt_text} [{default}]: ").strip()
            if not raw:
                return default
            val = int(raw)
            if min_val is not None and val < min_val:
                print(f"Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be at most {max_val}.")
                continue
            return val
        except ValueError:
            print("Please enter a valid integer.")


def _prompt_float(prompt_text: str, default: float, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
    """Prompt user for a float with default and bounds validation."""
    while True:
        try:
            raw = input(f"{prompt_text} [{default}]: ").strip()
            if not raw:
                return default
            val = float(raw)
            if min_val is not None and val < min_val:
                print(f"Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be at most {max_val}.")
                continue
            return val
        except ValueError:
            print("Please enter a valid number.")


def _prompt_optional_seed() -> Optional[int]:
    """Prompt for an optional random seed."""
    while True:
        raw = input("Random seed (leave blank for fresh random): ").strip()
        if not raw:
            return None
        try:
            return int(raw)
        except ValueError:
            print("Seed must be an integer or blank.")


def _prompt_bool(prompt_text: str, default: bool = True) -> bool:
    """Prompt for a yes/no boolean."""
    hint = "Y/n" if default else "y/N"
    raw = input(f"{prompt_text} [{hint}]: ").strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes", "true", "1")


class InteractiveSession:
    """Stateful interactive console session for generating and saving artwork."""

    def __init__(self) -> None:
        self.last_artwork: Optional[str] = None
        self.last_mode: Optional[str] = None

    def display_artwork(self, title: str, artwork: str) -> None:
        """Display generated artwork with clean header and footer."""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60 + "\n")
        print(artwork)
        print("\n" + "=" * 60)
        self.last_artwork = artwork
        self.last_mode = title

    def handle_starfield(self) -> None:
        """Interactive starfield creation."""
        print("\n--- Generate Starfield ---")
        width = _prompt_int("Width", default=80, min_val=10, max_val=250)
        height = _prompt_int("Height", default=24, min_val=5, max_val=100)
        density = _prompt_float("Density (0.01 to 0.50)", default=0.08, min_val=0.01, max_val=0.50)
        seed = _prompt_optional_seed()

        gen = StarfieldGenerator(width=width, height=height, density=density, seed=seed)
        artwork = gen.render()
        desc = f"Starfield ({width}x{height}, density={density}" + (f", seed={seed}" if seed else "") + ")"
        self.display_artwork(desc, artwork)

    def handle_constellation(self) -> None:
        """Interactive constellation creation."""
        print("\n--- Generate Constellation ---")
        presets = ["orion", "big-dipper", "cassiopeia"]
        print("Available presets:")
        for idx, p in enumerate(presets, 1):
            print(f"  {idx}. {p}")

        choice = _prompt_int("Select preset number", default=1, min_val=1, max_val=len(presets))
        preset_name = presets[choice - 1]

        width = _prompt_int("Width", default=80, min_val=20, max_val=250)
        height = _prompt_int("Height", default=24, min_val=10, max_val=100)
        show_labels = _prompt_bool("Show star name labels?", default=True)
        seed = _prompt_optional_seed()

        gen = ConstellationGenerator(
            preset=preset_name,
            width=width,
            height=height,
            show_labels=show_labels,
            seed=seed,
        )
        artwork = gen.render()
        desc = f"Constellation: {preset_name.title()} ({width}x{height}" + (f", seed={seed}" if seed else "") + ")"
        self.display_artwork(desc, artwork)

    def handle_galaxy(self) -> None:
        """Interactive spiral galaxy creation."""
        print("\n--- Generate Spiral Galaxy ---")
        width = _prompt_int("Width", default=100, min_val=20, max_val=250)
        height = _prompt_int("Height", default=30, min_val=10, max_val=100)
        arms = _prompt_int("Spiral arms count", default=2, min_val=1, max_val=8)
        seed = _prompt_optional_seed()

        gen = SpiralGalaxyGenerator(width=width, height=height, arms=arms, seed=seed)
        artwork = gen.render()
        desc = f"Spiral Galaxy ({width}x{height}, {arms} arms" + (f", seed={seed}" if seed else "") + ")"
        self.display_artwork(desc, artwork)

    def handle_nebula(self) -> None:
        """Interactive nebula creation."""
        print("\n--- Generate Interstellar Nebula ---")
        width = _prompt_int("Width", default=80, min_val=20, max_val=250)
        height = _prompt_int("Height", default=24, min_val=10, max_val=100)
        clusters = _prompt_int("Cloud cluster count", default=5, min_val=1, max_val=15)
        seed = _prompt_optional_seed()

        gen = NebulaGenerator(width=width, height=height, clusters=clusters, seed=seed)
        artwork = gen.render()
        desc = f"Interstellar Nebula ({width}x{height}, {clusters} clusters" + (f", seed={seed}" if seed else "") + ")"
        self.display_artwork(desc, artwork)

    def handle_presets_browser(self) -> None:
        """Browse catalog presets and generate one."""
        print("\n--- Celestial Presets Catalog ---")
        catalog_items = list_all_presets()
        for i, item in enumerate(catalog_items, 1):
            print(f"  {i}. [{item.category.upper():13}] {item.title}")
            print(f"      {item.description}")

        print(f"  0. Back to main menu")
        choice = _prompt_int("Select preset to generate", default=1, min_val=0, max_val=len(catalog_items))
        if choice == 0:
            return

        preset = catalog_items[choice - 1]
        params = dict(preset.parameters)

        if preset.category == "constellation":
            gen = ConstellationGenerator(**params)
        elif preset.category == "galaxy":
            gen = SpiralGalaxyGenerator(**params)
        elif preset.category == "nebula":
            gen = NebulaGenerator(**params)
        elif preset.category == "starfield":
            gen = StarfieldGenerator(**params)
        else:
            print("Unknown category.")
            return

        artwork = gen.render()
        self.display_artwork(f"Preset: {preset.title}", artwork)

    def handle_save(self) -> None:
        """Save the last generated artwork."""
        if not self.last_artwork:
            print("\n[!] No artwork generated yet. Generate something first!")
            return

        # We will use export module (or direct fallback if export module imported)
        from pathlib import Path
        output_dir = Path("outputs")
        output_dir.mkdir(parents=True, exist_ok=True)

        default_name = "artwork.txt"
        target_name = input(f"Enter filename to save in outputs/ [{default_name}]: ").strip()
        if not target_name:
            target_name = default_name
        if not target_name.endswith(".txt"):
            target_name += ".txt"

        target_path = output_dir / target_name
        try:
            target_path.write_text(self.last_artwork + "\n", encoding="utf-8")
            print(f"\n[✓] Successfully saved to {target_path.resolve()}")
        except Exception as e:
            print(f"\n[!] Error saving file: {e}")

    def run(self) -> int:
        """Main interaction loop."""
        while True:
            print("\n" + "=" * 60)
            print("        STARDOTS — ASCII UNIVERSE GENERATOR")
            print("=" * 60)
            print("  1. Random Starfield")
            print("  2. Constellation (Orion, Big Dipper, Cassiopeia)")
            print("  3. Spiral Galaxy")
            print("  4. Interstellar Nebula")
            print("  5. Built-in Presets Catalog")
            print("  6. Save Current Artwork")
            print("  7. Exit")
            print("=" * 60)

            try:
                choice = input("Enter choice (1-7): ").strip()
                if choice == "1":
                    self.handle_starfield()
                elif choice == "2":
                    self.handle_constellation()
                elif choice == "3":
                    self.handle_galaxy()
                elif choice == "4":
                    self.handle_nebula()
                elif choice == "5":
                    self.handle_presets_browser()
                elif choice == "6":
                    self.handle_save()
                elif choice in ("7", "q", "exit", "quit"):
                    print("\nExiting StarDots. Safe travels through the cosmos!\n")
                    return 0
                else:
                    print("Invalid option. Please enter a number from 1 to 7.")
            except (KeyboardInterrupt, EOFError):
                print("\n\nExiting StarDots. Safe travels through the cosmos!\n")
                return 0


def run_interactive() -> int:
    """Run an interactive session."""
    session = InteractiveSession()
    return session.run()
