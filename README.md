# StarDots — ASCII Universe Generator

> A lightweight, zero-dependency Python CLI tool that generates rich ASCII and Unicode space artwork in your terminal and saves them to UTF-8 text files.

[![Tests](https://github.com/Red-swipe/StarDots/actions/workflows/test.yml/badge.svg)](https://github.com/Red-swipe/StarDots/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Features

- **Random Starfields**: Configurable canvas dimensions, star density, and custom palettes (`.`, `*`, `+`, `o`) with deterministic integer seeds.
- **Constellations**: Predefined astronomical patterns (Orion, Big Dipper, Cassiopeia) connected by directional lines (`/`, `\`, `|`, `-`) with optional star labels and overwrite-protected star points.
- **Spiral Galaxies**: Logarithmic and power-law density spirals with configurable arm counts, glowing galactic cores, and sparser outer regions.
- **Interstellar Nebulae**: Organic multi-cluster gas clouds and filaments rendered with multi-level brightness gradients and embedded newborn protostars.
- **Built-in Presets Catalog**: Quick-generation presets including *Milky Way*, *Whirlpool (M51)*, *Triangulum (M33)*, *Orion Nebula (M42)*, *Crab Nebula (M1)*, *Deep Field*, and more.
- **Interactive Terminal Menu**: Interactive terminal wizard with bounds checking, artwork preview, and direct export.
- **Zero External Dependencies**: Pure Python 3.11+ using only standard library modules (`random`, `math`, `argparse`, `pathlib`, `shutil`, `unittest`).
- **Reproducibility**: Isolated random number generator instances (`random.Random(seed)`) guarantee that identical seeds yield identical universes.
- **Robust Text Export**: Clean UTF-8 file export with collision prevention (auto-rename suffix or explicit `--force` overwrite).
- **Terminal Size Awareness**: Optional `--fit-terminal` flag to dynamically fit generated artwork to current terminal dimensions.

---

## Requirements & Supported Platforms

- **Python Version**: Python 3.11 or newer
- **Operating Systems**: Windows, Linux, macOS
- **Dependencies**: Python standard library only

---

## Installation

Clone the repository and run immediately without installing third-party packages:

```bash
git clone https://github.com/Red-swipe/StarDots.git
cd StarDots
```

---

## Usage Examples

StarDots can be executed directly via `python stardots.py` or as a module `python -m stardots.cli`.

### 1. Random Starfields
```bash
# Default starfield (80x24)
python stardots.py starfield

# Custom dimensions, density, and seed
python stardots.py starfield --width 80 --height 24 --density 0.12 --seed 42

# Custom star character palette
python stardots.py starfield --palette ".*+o" --density 0.15 --seed 100

# Fit canvas to your terminal window
python stardots.py starfield --fit-terminal
```

### 2. Spiral Galaxies
```bash
# 2-arm spiral galaxy
python stardots.py galaxy --width 100 --height 30 --arms 2 --seed 42

# 3-arm pinwheel galaxy
python stardots.py galaxy --width 100 --height 30 --arms 3 --seed 108

# Save galaxy to file
python stardots.py galaxy --width 100 --height 30 --arms 2 --output outputs/galaxy.txt
```

### 3. Constellations
```bash
# Orion with star labels (Betelgeuse, Rigel, Belt stars, etc.)
python stardots.py constellation --preset orion

# The Big Dipper (Ursa Major asterism)
python stardots.py constellation --preset big-dipper

# Cassiopeia without star labels
python stardots.py constellation --preset cassiopeia --no-labels

# Custom seed for background stars
python stardots.py constellation --preset orion --seed 42
```

### 4. Interstellar Nebulae
```bash
# Billowing gas cloud with default 5 clusters
python stardots.py nebula --width 80 --height 24

# Dense multi-cluster nebula with seed
python stardots.py nebula --width 80 --height 24 --clusters 7 --seed 1054

# Strict ASCII-only character gradient
python stardots.py nebula --width 80 --height 24 --ascii-only
```

### 5. Celestial Presets Catalog
```bash
# List all available presets across constellations, galaxies, and nebulae
python stardots.py presets
```

---

## Interactive Mode

Launch the interactive console menu:

```bash
python stardots.py interactive
```

*(Or simply run `python stardots.py` inside an interactive terminal).*

The menu allows you to:
1. Generate random starfields with custom parameters.
2. Select and render constellation asterisms.
3. Shape spiral galaxies with variable arm counts.
4. Render cloud-like nebulae with multi-tier shading.
5. Browse and generate from the built-in celestial catalog.
6. Export the active artwork directly to a UTF-8 text file.
7. Exit cleanly at any prompt (or via `Ctrl+C`).

---

## Text Export & Collision Prevention

Export artwork directly to disk using the `--output` / `-o` option:

```bash
# Export to outputs/ folder
python stardots.py galaxy --output outputs/milkyway.txt --arms 2 --seed 42

# Safe collision prevention:
# If outputs/milkyway.txt already exists, StarDots reports the conflict without overwriting.
python stardots.py galaxy --output outputs/milkyway.txt --arms 2 --seed 42
# Output: Export error: Target file already exists: 'outputs/milkyway.txt'. Use --force or choose another filename.

# Overwrite explicitly using --force:
python stardots.py galaxy --output outputs/milkyway.txt --force --arms 2 --seed 42
```

---

## Automated Testing

StarDots comes with comprehensive `unittest` coverage testing all generators, seeds, dimensions, argument parsing, presets, collision handling, and edge cases.

To run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

---

## Project Structure

```
StarDots/
├── .github/
│   └── workflows/
│       └── test.yml          # GitHub Actions CI matrix (Ubuntu, Windows, macOS)
├── outputs/                  # Export directory for generated .txt files
│   └── .gitkeep
├── stardots/                 # Core Python package
│   ├── __init__.py           # Package version and metadata
│   ├── canvas.py             # 2D character grid, line drawing, and terminal sizing
│   ├── cli.py                # Command-line interface and argument parsing
│   ├── export.py             # UTF-8 text export and overwrite protection
│   ├── interactive.py        # Interactive console menu loop
│   ├── palette.py            # Star palettes and shading gradients
│   ├── presets.py            # Celestial formations catalog registry
│   └── generators/           # Modular artwork generators
│       ├── __init__.py       # Generators exports
│       ├── base.py           # Abstract BaseGenerator with RNG isolation
│       ├── constellation.py  # Constellations with directional lines & labels
│       ├── galaxy.py         # Logarithmic spiral galaxy generator
│       ├── nebula.py         # Multi-scale gas blob and filament generator
│       └── starfield.py      # Random starfield generator
├── tests/                    # Automated unittest test suite
│   ├── __init__.py
│   ├── test_canvas.py        # Canvas and drawing tests
│   ├── test_cli.py           # CLI parsing and command execution tests
│   ├── test_export.py        # Text export and collision tests
│   ├── test_generators.py    # Generator determinism and dimensions tests
│   └── test_presets.py       # Preset catalog tests
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
├── README.md                 # Project documentation
└── stardots.py               # Executable entry point script
```

---

## Known Limitations

- **Terminal Font Aspect Ratio**: Terminal characters are vertically taller than they are wide (typically ~2:1). StarDots compensates for this aspect ratio mathematically, but extreme custom terminal font aspect ratios may slightly alter visual circularity.
- **Unicode Support**: While Unicode characters provide rich rendering on modern UTF-8 terminals, Windows legacy console windows (`cmd.exe`) may require standard code page 65001. StarDots automatically configures standard streams for UTF-8 and provides ASCII fallbacks.

---

## License

This project is licensed under the [MIT License](LICENSE).
