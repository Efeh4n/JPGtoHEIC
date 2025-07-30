#!/usr/bin/env python3
"""
Bulk-convert every JPG/JPEG in a folder you enter to HEIC,
and save all HEICs into a new "heic" folder on your Desktop.

Dependencies:
    pip install pillow pillow-heif
"""

from pathlib import Path
from PIL import Image, UnidentifiedImageError
import pillow_heif
import os

# Register HEIC/HEIF support with Pillow
pillow_heif.register_heif_opener()


def get_desktop_folder() -> Path:
    """
    Return the actual Desktop folder, handling OneDrive redirects on Windows.
    """
    # 1) OneDrive Desktop
    od = Path.home() / "OneDrive" / "Desktop"
    if od.exists():
        return od
    # 2) Standard Desktop
    std = Path.home() / "Desktop"
    if std.exists():
        return std
    # 3) Fallback: create standard Desktop if missing
    std.mkdir(parents=True, exist_ok=True)
    return std


def find_jpeg_files(folder: Path):
    """
    Recursively find all .jpg/.jpeg files under the given folder.
    """
    return [p for p in folder.rglob("*") if p.suffix.lower() in (".jpg", ".jpeg")]


def ensure_output_folder() -> Path:
    """
    Create (or reuse) the ~/Desktop/heic folder.
    """
    desktop = get_desktop_folder()
    out = desktop / "heic"
    out.mkdir(parents=True, exist_ok=True)
    return out


def convert_to_heic(src: Path, dst: Path, quality: int = 90):
    """
    Convert a single JPEG file to HEIC, preserving EXIF metadata if present.
    """
    with Image.open(src) as img:
        exif = img.info.get("exif")
        img.save(dst, quality=quality, exif=exif)


def main():
    # Ask user for the folder containing JPEGs
    folder_input = input("Enter full path of the folder with JPG/JPEG files:\n").strip()
    source_folder = Path(folder_input).expanduser().resolve()

    if not source_folder.is_dir():
        print(f"Error: '{source_folder}' is not a valid directory.")
        return

    # Gather all JPEGs
    jpeg_files = find_jpeg_files(source_folder)
    if not jpeg_files:
        print("No .jpg/.jpeg files found. Exiting.")
        return

    # Prepare ~/Desktop/heic output folder
    output_folder = ensure_output_folder()
    print(f"Found {len(jpeg_files)} JPEG files.")
    print(f"Converting to HEIC in: {output_folder.resolve()}\n")

    # Convert each file
    for jpg in jpeg_files:
        heic_path = output_folder / f"{jpg.stem}.heic"
        try:
            convert_to_heic(jpg, heic_path)
            print(f"✔ {jpg.name} → {heic_path.name}")
        except UnidentifiedImageError:
            print(f"✖ Skipped unreadable file: {jpg.name}")
        except Exception as e:
            print(f"✖ Failed to convert {jpg.name}: {e}")

    print(f"\nAll done! Your HEIC files are in:\n{output_folder.resolve()}")
    # On Windows, open the folder automatically
    try:
        os.startfile(output_folder.resolve())
    except Exception:
        pass


if __name__ == "__main__":
    main()
