# StarDots — ASCII Universe Generator

> A lightweight, zero-dependency Python CLI tool that generates rich ASCII and Unicode space artwork in your terminal and saves them to text files.

## Features

- **Random Starfields**: Configurable canvas dimensions, star density, and custom palettes with deterministic integer seeds.
- **Constellations** *(Stage 2)*: Recognizable celestial patterns (Orion, Big Dipper) with directional lines and star labels.
- **Spiral Galaxies** *(Stage 2)*: Logarithmic spirals with dense galactic cores and sparser outer spiral arms.
- **Nebulae** *(Stage 2)*: Cloud-like celestial gas formations with multi-level ASCII/Unicode brightness gradients.
- **Interactive Mode** *(Stage 3)*: Intuitive terminal menu for interactive exploration.
- **Zero Dependencies**: Pure Python 3.11+ using only standard library modules (`random`, `math`, `argparse`, `pathlib`, `unittest`).
- **Reproducibility**: Isolated random number generators guarantee that identical seeds yield identical universes.
- **UTF-8 Text Export** *(Stage 4)*: Clean export to text files with collision prevention.

---

## Requirements

- Python 3.11 or newer
- Operating System: Windows, macOS, or Linux
- Standard terminal with UTF-8 support

---

## Installation

No external dependencies are required. Clone the repository and run directly:

```bash
git clone https://github.com/Red-swipe/StarDots.git
cd StarDots
```

---

## Quick Start

### 1. Help & Available Commands
```bash
python stardots.py --help
```

### 2. Generate a Starfield
```bash
# Default starfield (80x24)
python stardots.py starfield

# Custom dimensions, density, and seed
python stardots.py starfield --width 80 --height 24 --density 0.12 --seed 42

# Custom star palette
python stardots.py starfield --palette ".*+o" --density 0.15 --seed 100
```

---

## License

This project is licensed under the [MIT License](LICENSE).
