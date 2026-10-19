"""Command line interface for StarDots — ASCII Universe Generator."""

import argparse
import sys
from typing import List, Optional

from stardots import __version__
from stardots.generators.constellation import CONSTELLATION_PRESETS, ConstellationGenerator
from stardots.generators.galaxy import SpiralGalaxyGenerator
from stardots.generators.nebula import NebulaGenerator
from stardots.generators.starfield import StarfieldGenerator

def configure_terminal_encoding() -> None:
    """Ensure standard output and error support UTF-8 without crashing on Windows."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser for StarDots."""
    parser = argparse.ArgumentParser(
        prog="stardots",
        description="StarDots — ASCII Universe Generator: Generate space artwork in your terminal.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="Available generation modes")

    # Starfield subcommand
    sf_parser = subparsers.add_parser(
        "starfield",
        help="Generate a random starfield",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sf_parser.add_argument("--width", type=int, default=80, help="Canvas width in columns")
    sf_parser.add_argument("--height", type=int, default=24, help="Canvas height in rows")
    sf_parser.add_argument("--density", type=float, default=0.08, help="Star density between 0.0 and 1.0")
    sf_parser.add_argument("--seed", type=int, default=None, help="Integer random seed for reproducibility")
    sf_parser.add_argument("--palette", type=str, default=None, help="Custom star characters (e.g. '.*+o')")
    sf_parser.add_argument("--output", "-o", type=str, default=None, help="Save generated artwork to file path")

    # Galaxy subcommand
    gal_parser = subparsers.add_parser(
        "galaxy",
        help="Generate a spiral galaxy",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    gal_parser.add_argument("--width", type=int, default=100, help="Canvas width in columns")
    gal_parser.add_argument("--height", type=int, default=30, help="Canvas height in rows")
    gal_parser.add_argument("--arms", type=int, default=2, help="Number of spiral arms")
    gal_parser.add_argument("--winding", type=float, default=2.4, help="Spiral winding factor")
    gal_parser.add_argument("--seed", type=int, default=None, help="Integer random seed")
    gal_parser.add_argument("--output", "-o", type=str, default=None, help="Save output to file")

    # Constellation subcommand
    const_parser = subparsers.add_parser(
        "constellation",
        help="Generate a constellation pattern",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    const_parser.add_argument("--preset", type=str, default="orion", help="Constellation preset (e.g. orion, big-dipper, cassiopeia)")
    const_parser.add_argument("--width", type=int, default=80, help="Canvas width in columns")
    const_parser.add_argument("--height", type=int, default=24, help="Canvas height in rows")
    const_parser.add_argument("--seed", type=int, default=None, help="Integer random seed for background stars")
    const_parser.add_argument("--no-labels", action="store_true", help="Omit constellation star labels")
    const_parser.add_argument("--output", "-o", type=str, default=None, help="Save output to file")

    # Nebula subcommand
    neb_parser = subparsers.add_parser(
        "nebula",
        help="Generate an interstellar gas cloud / nebula",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    neb_parser.add_argument("--width", type=int, default=80, help="Canvas width in columns")
    neb_parser.add_argument("--height", type=int, default=24, help="Canvas height in rows")
    neb_parser.add_argument("--clusters", type=int, default=5, help="Number of cloud puff centers")
    neb_parser.add_argument("--ascii-only", action="store_true", help="Use strictly basic ASCII characters without Unicode")
    neb_parser.add_argument("--seed", type=int, default=None, help="Integer random seed")
    neb_parser.add_argument("--output", "-o", type=str, default=None, help="Save output to file")

    # Presets listing subcommand
    subparsers.add_parser(
        "presets",
        help="List available constellation and celestial presets",
    )

    # Interactive mode
    subparsers.add_parser(
        "interactive",
        help="Launch the interactive terminal menu",
    )

    return parser


def run_starfield(args: argparse.Namespace) -> int:
    """Execute starfield generation with validated parameters."""
    if args.width <= 0:
        sys.stderr.write(f"Error: --width must be positive, got {args.width}\n")
        return 1
    if args.height <= 0:
        sys.stderr.write(f"Error: --height must be positive, got {args.height}\n")
        return 1
    if not (0.0 < args.density <= 1.0):
        sys.stderr.write(f"Error: --density must be between 0.0 and 1.0, got {args.density}\n")
        return 1

    palette = list(args.palette) if args.palette else None

    try:
        gen = StarfieldGenerator(
            width=args.width,
            height=args.height,
            density=args.density,
            palette=palette,
            seed=args.seed,
        )
        artwork = gen.render()
        print(artwork)

        if getattr(args, "output", None):
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(artwork + "\n")
            print(f"\n[Saved to {args.output}]")
        return 0
    except Exception as e:
        sys.stderr.write(f"Error generating starfield: {e}\n")
        return 1


def run_galaxy(args: argparse.Namespace) -> int:
    """Execute spiral galaxy generation."""
    if args.width <= 0:
        sys.stderr.write(f"Error: --width must be positive, got {args.width}\n")
        return 1
    if args.height <= 0:
        sys.stderr.write(f"Error: --height must be positive, got {args.height}\n")
        return 1
    if args.arms < 1:
        sys.stderr.write(f"Error: --arms must be at least 1, got {args.arms}\n")
        return 1

    try:
        gen = SpiralGalaxyGenerator(
            width=args.width,
            height=args.height,
            arms=args.arms,
            winding=getattr(args, "winding", 2.4),
            seed=args.seed,
        )
        artwork = gen.render()
        print(artwork)

        if getattr(args, "output", None):
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(artwork + "\n")
            print(f"\n[Saved to {args.output}]")
        return 0
    except Exception as e:
        sys.stderr.write(f"Error generating galaxy: {e}\n")
        return 1


def run_constellation(args: argparse.Namespace) -> int:
    """Execute constellation generation."""
    if args.width <= 0:
        sys.stderr.write(f"Error: --width must be positive, got {args.width}\n")
        return 1
    if args.height <= 0:
        sys.stderr.write(f"Error: --height must be positive, got {args.height}\n")
        return 1

    norm_key = args.preset.strip().lower().replace("_", "-")
    if norm_key not in CONSTELLATION_PRESETS:
        valid = ", ".join(sorted({p.name for p in CONSTELLATION_PRESETS.values()}))
        sys.stderr.write(f"Error: Unknown preset '{args.preset}'. Available presets: {valid}\n")
        return 1

    try:
        gen = ConstellationGenerator(
            preset=args.preset,
            width=args.width,
            height=args.height,
            show_labels=not args.no_labels,
            seed=args.seed,
        )
        artwork = gen.render()
        print(artwork)

        if getattr(args, "output", None):
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(artwork + "\n")
            print(f"\n[Saved to {args.output}]")
        return 0
    except Exception as e:
        sys.stderr.write(f"Error generating constellation: {e}\n")
        return 1


def run_nebula(args: argparse.Namespace) -> int:
    """Execute nebula generation."""
    if args.width <= 0:
        sys.stderr.write(f"Error: --width must be positive, got {args.width}\n")
        return 1
    if args.height <= 0:
        sys.stderr.write(f"Error: --height must be positive, got {args.height}\n")
        return 1
    if args.clusters < 1:
        sys.stderr.write(f"Error: --clusters must be at least 1, got {args.clusters}\n")
        return 1

    try:
        gen = NebulaGenerator(
            width=args.width,
            height=args.height,
            clusters=args.clusters,
            use_ascii_only=args.ascii_only,
            seed=args.seed,
        )
        artwork = gen.render()
        print(artwork)

        if getattr(args, "output", None):
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(artwork + "\n")
            print(f"\n[Saved to {args.output}]")
        return 0
    except Exception as e:
        sys.stderr.write(f"Error generating nebula: {e}\n")
        return 1


def run_presets() -> int:
    """Display available presets with descriptions."""
    print("=" * 60)
    print("StarDots — Built-in Constellation & Celestial Presets")
    print("=" * 60)
    seen = set()
    for key, p in CONSTELLATION_PRESETS.items():
        if p.name in seen:
            continue
        seen.add(p.name)
        star_count = len(p.stars)
        line_count = len(p.lines)
        print(f"\n* {p.name.upper()} ({star_count} stars, {line_count} connections)")
        print(f"  Description: {p.description}")
        sample_stars = ", ".join(s.name for s in p.stars[:4])
        if star_count > 4:
            sample_stars += ", ..."
        print(f"  Key stars  : {sample_stars}")

    print("\n" + "=" * 60)
    print("Usage: python stardots.py constellation --preset <name>")
    print("=" * 60)
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point function."""
    configure_terminal_encoding()
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.subcommand:
        parser.print_help()
        return 0

    if args.subcommand == "starfield":
        return run_starfield(args)
    elif args.subcommand == "galaxy":
        return run_galaxy(args)
    elif args.subcommand == "constellation":
        return run_constellation(args)
    elif args.subcommand == "nebula":
        return run_nebula(args)
    elif args.subcommand == "presets":
        return run_presets()
    elif args.subcommand == "interactive":
        sys.stderr.write("Interactive mode will be plugged in Stage 3.\n")
        return 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
