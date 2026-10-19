"""Export management and safe filesystem operations for StarDots."""

import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Union


class ExportError(Exception):
    """Raised when artwork export fails due to filesystem or validation errors."""
    pass


def get_default_output_dir() -> Path:
    """Return the default output directory within the project, ensuring it exists."""
    output_dir = Path.cwd() / "outputs"
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise ExportError(f"Could not create default output directory '{output_dir}': {e}") from e
    return output_dir


def sanitize_filename(name: str) -> str:
    """Sanitize a filename to ensure cross-platform safety (Windows, Linux, macOS)."""
    # Remove characters forbidden on Windows/Linux: < > : " / \ | ? *
    clean = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    clean = re.sub(r'_+', '_', clean)
    clean = clean.strip(" ._")
    return clean or "artwork"


def generate_descriptive_filename(prefix: str = "artwork", extension: str = ".txt") -> str:
    """Generate a clean, descriptive timestamped filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_prefix = sanitize_filename(prefix)
    ext = extension if extension.startswith(".") else f".{extension}"
    return f"{clean_prefix}_{timestamp}{ext}"


def resolve_output_path(
    destination: Optional[Union[str, Path]] = None,
    default_prefix: str = "artwork",
    allow_overwrite: bool = False,
    conflict_strategy: str = "auto_rename",
) -> Path:
    """Resolve and validate the target path for saving artwork.

    Args:
        destination: Path or filename given by user. If None, generates a timestamped name in outputs/.
        default_prefix: Prefix used if generating a default name.
        allow_overwrite: If True, existing files at destination will be replaced.
        conflict_strategy: 'auto_rename' (appends _1, _2, etc.) or 'error' (raises ExportError if exists).

    Returns:
        Resolved Path ready for writing.
    """
    if destination is None or not str(destination).strip():
        out_dir = get_default_output_dir()
        filename = generate_descriptive_filename(default_prefix)
        target = out_dir / filename
    else:
        target = Path(destination)
        # If destination is a directory or ends with slash, place default named file inside it
        if target.is_dir() or str(destination).endswith(("/", "\\")):
            target.mkdir(parents=True, exist_ok=True)
            filename = generate_descriptive_filename(default_prefix)
            target = target / filename
        else:
            # If target has no parent directory specified, default to outputs/
            if len(target.parts) == 1:
                target = get_default_output_dir() / target
            if not target.suffix:
                target = target.with_suffix(".txt")

    # Ensure parent directory exists
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise ExportError(f"Cannot create destination directory '{target.parent}': {e}") from e

    # Handle file collision if file already exists
    if target.exists() and not allow_overwrite:
        if conflict_strategy == "error":
            raise ExportError(f"Target file already exists: '{target}'. Use --force or choose another filename.")
        elif conflict_strategy == "auto_rename":
            base_stem = target.stem
            suffix = target.suffix
            counter = 1
            while target.exists():
                target = target.parent / f"{base_stem}_{counter}{suffix}"
                counter += 1

    return target


def export_artwork(
    artwork: str,
    destination: Optional[Union[str, Path]] = None,
    default_prefix: str = "artwork",
    allow_overwrite: bool = False,
    conflict_strategy: str = "auto_rename",
) -> Path:
    """Export artwork string to a UTF-8 encoded text file with robust error handling.

    Args:
        artwork: The multi-line string artwork to save.
        destination: Target file path or directory.
        default_prefix: Prefix for auto-generated filename.
        allow_overwrite: Whether to overwrite existing destination.
        conflict_strategy: 'auto_rename' or 'error'.

    Returns:
        The Path to the saved file.
    """
    if not isinstance(artwork, str):
        raise ValueError(f"Artwork must be a string, got {type(artwork).__name__}")

    target_path = resolve_output_path(
        destination=destination,
        default_prefix=default_prefix,
        allow_overwrite=allow_overwrite,
        conflict_strategy=conflict_strategy,
    )

    try:
        # Standardize on LF line endings in text export
        content = artwork.rstrip("\r\n") + "\n"
        target_path.write_text(content, encoding="utf-8")
    except PermissionError as e:
        raise ExportError(f"Permission denied when writing to '{target_path}': {e}") from e
    except OSError as e:
        raise ExportError(f"Filesystem error writing to '{target_path}': {e}") from e

    return target_path
