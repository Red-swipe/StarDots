"""Tests for CLI arguments, subcommands, and execution flow."""

import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from stardots.cli import create_parser, main


class TestCLI(unittest.TestCase):
    """Test StarDots command-line interface execution and argument parsing."""

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parser_creation(self) -> None:
        """Parser initializes with all required subcommands."""
        parser = create_parser()
        self.assertIsNotNone(parser)
        args = parser.parse_args(["starfield", "--width", "50", "--height", "15"])
        self.assertEqual(args.subcommand, "starfield")
        self.assertEqual(args.width, 50)
        self.assertEqual(args.height, 15)

    def test_starfield_execution(self) -> None:
        """Starfield subcommand runs successfully."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["starfield", "--width", "40", "--height", "10", "--density", "0.08", "--seed", "42"])
        self.assertEqual(code, 0)
        output = buf.getvalue().strip()
        lines = output.splitlines()
        self.assertEqual(len(lines), 10)

    def test_galaxy_execution(self) -> None:
        """Galaxy subcommand runs with custom arms."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["galaxy", "--width", "50", "--height", "15", "--arms", "3", "--seed", "10"])
        self.assertEqual(code, 0)
        self.assertIn("@", buf.getvalue())

    def test_constellation_execution(self) -> None:
        """Constellation subcommand runs for predefined presets."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["constellation", "--preset", "orion", "--seed", "42"])
        self.assertEqual(code, 0)
        self.assertIn("Betelgeuse", buf.getvalue())

    def test_nebula_execution(self) -> None:
        """Nebula subcommand runs with custom dimensions."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["nebula", "--width", "40", "--height", "12", "--seed", "42"])
        self.assertEqual(code, 0)
        lines = buf.getvalue().rstrip("\r\n").splitlines()
        self.assertEqual(len(lines), 12)

    def test_presets_subcommand(self) -> None:
        """Presets command outputs available presets catalog."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(["presets"])
        self.assertEqual(code, 0)
        self.assertIn("ORION", buf.getvalue())
        self.assertIn("MILKY-WAY", buf.getvalue())

    def test_cli_export_and_force(self) -> None:
        """CLI saves file to disk and requires --force to overwrite."""
        target = self.temp_dir / "cli_out.txt"
        with redirect_stdout(io.StringIO()):
            code = main(["starfield", "--width", "30", "--height", "10", "-o", str(target), "--seed", "1"])
        self.assertEqual(code, 0)
        self.assertTrue(target.exists())

        # Second run without force should report error
        err_buf = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(err_buf):
            code_fail = main(["starfield", "--width", "30", "--height", "10", "-o", str(target), "--seed", "2"])
        self.assertEqual(code_fail, 1)

        # Second run with force succeeds
        with redirect_stdout(io.StringIO()):
            code_overwrite = main(["starfield", "--width", "30", "--height", "10", "-o", str(target), "--force", "--seed", "3"])
        self.assertEqual(code_overwrite, 0)

    def test_invalid_arguments_validation(self) -> None:
        """Invalid inputs return error code 1."""
        err_buf = io.StringIO()
        with redirect_stderr(err_buf):
            # Negative width
            self.assertEqual(main(["starfield", "--width", "-5"]), 1)
            # Density > 1
            self.assertEqual(main(["starfield", "--density", "2.0"]), 1)
            # Arms < 1
            self.assertEqual(main(["galaxy", "--arms", "0"]), 1)
            # Unknown preset
            self.assertEqual(main(["constellation", "--preset", "nonexistent"]), 1)
            # Nebula clusters < 1
            self.assertEqual(main(["nebula", "--clusters", "0"]), 1)


if __name__ == "__main__":
    unittest.main()
