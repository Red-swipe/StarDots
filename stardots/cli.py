"""Command line interface for StarDots — ASCII Universe Generator."""

import argparse
import sys
from typing import List, Optional

from stardots import __version__
from stardots.generators.starfield import StarfieldGenerator


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

    # Galaxy subcommand placeholder for future stages
    gal_parser = subparsers.add_parser(
        "galaxy",
        help="Generate a spiral galaxy",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    gal_parser.add_argument("--width", type=int, default=100, help="Canvas width in columns")
    gal_parser.add_argument("--height", type=int, default=30, help="Canvas height in rows")
    gal_parser.add_argument("--arms", type=int, default=2, help="Number of spiral arms")
    gal_parser.add_argument("--seed", type=int, default=None, help="Integer random seed")
    gal_parser.add_argument("--output", "-o", type=str, default=None, help="Save output to file")

    # Constellation subcommand placeholder
    const_parser = subparsers.add_parser(
        "constellation",
        help="Generate a constellation pattern",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    const_parser.add_argument("--preset", type=str, default="orion", help="Constellation preset (e.g. orion, big-dipper)")
    const_parser.add_argument("--width", type=int, default=80, help="Canvas width in columns")
    const_parser.add_argument("--height", type=int, default=24, help="Canvas height in rows")
    const_parser.add_argument("--seed", type=int, default=None, help="Integer random seed for background stars")
    const_parser.add_argument("--no-labels", action="store_true", help="Omit constellation star labels")
    const_parser.add_argument("--output", "-o", type=str, default=None, help="Save output to file")

    # Nebula subcommand placeholder
    neb_parser = subparsers.add_parser(
        "nebula",
        help="Generate an interstellar gas cloud / nebula",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    neb_parser.add_argument("--width", type=int, default=80, help="Canvas width in columns")
    neb_parser.add_argument("--height", type=int, default=24, help="Canvas height in rows")
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


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point function."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.subcommand:
        # If no subcommand supplied, show help for now (Stage 1)
        # Interactive mode will be plugged in Stage 3
        parser.print_help()
        return 0

    if args.subcommand == "starfield":
        return run_starfield(args)
    elif args.subcommand in ("galaxy", "constellation", "nebula", "presets", "interactive"):
        sys.stderr.write(f"Command '{args.subcommand}' is part of upcoming implementation stages.\n")
        return 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
