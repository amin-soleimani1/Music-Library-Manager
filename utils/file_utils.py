from pathlib import Path
import sys
import music_tag
from PIL import Image
import io
import os


# --==» Base Path (Dev + PyInstaller safe) «==--

def get_base_path() -> Path:
    """
    Returns the absolute path to a project resource.
    Compatible with both development mode and PyInstaller builds.
    """
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parent.parent


BASE_PATH = get_base_path()


def resource_path(relative_path: str | Path) -> Path:
    """
    Returns the path to application resources,
    such as icons and UI images.
    """
    return BASE_PATH / relative_path


# --==» database file path «==--

def app_data_path() -> Path:
    """
    Permanent storage path for application data,
    including the database and cache.
    """
    
    base = Path(
        os.getenv("LOCALAPPDATA")
    )

    path = base / "Music Library Manager"

    path.mkdir(parents=True, exist_ok=True)

    return path


# # --==» Media Paths «==--

def get_media_path(folder_name="music_files") -> Path:
    """
    Returns the path to the directory where music files are stored.
    """

    path = app_data_path() / folder_name
    path.mkdir(parents=True, exist_ok=True)

    return path

# --==» File Utils «==--

def delete_file(file_path: str | Path) -> bool:
    """
    Safely deletes the specified file.
    """
    path = Path(file_path)
    if path.exists() and path.is_file():
        path.unlink()
        return True
    return False


# --==» Time Formatting «==--

def format_time(seconds: int) -> str:
    """
    Converts seconds to MM:SS format.
    """
    seconds = int(seconds or 0)
    minutes, sec = divmod(seconds, 60)
    return f"{minutes:02d}:{sec:02d}"


# --==» Metadata Extraction «==--

def extract_metadata(file_path: str | Path) -> dict:
    """
    Extracts metadata and artwork from a music file.
    """
    path = Path(file_path)

    try:
        audio = music_tag.load_file(path)

        title = audio["title"]
        artist = audio["artist"]
        length = audio["#length"]

        return {
            "title": str(title) if title else path.stem,
            "artist": str(artist) if artist else None,
            "length": int(length) if length else 0,
            "artwork": (
                audio["artwork"].first.data
                if "artwork" in audio and audio["artwork"]
                else None
            ),
            "file_path": str(path),
        }

    except Exception as e:
        print(f"[Metadata Error] {path} -> {e}")

        return {
            "title": "Unknown",
            "artist": None,
            "length": 0,
            "artwork": None,
            "file_path": str(path),
        }


# --==» Artwork Cache «==--

def save_artwork_cache(artwork_bytes: bytes, track_id: str | int) -> str | None:
    """
    Saves the extracted artwork as a cached image
    and returns its file path.
    """
    if not artwork_bytes:
        return None

    cache_dir = app_data_path() / "cache" / "artworks"
    cache_dir.mkdir(parents=True, exist_ok=True)
    file_path = cache_dir / f"art_{track_id}.webp"

    if file_path.exists():
        return str(file_path)

    try:
        image = Image.open(io.BytesIO(artwork_bytes))
        image.load()

        # Resize if the image is too large.
        if image.width > 1000 or image.height > 1000:
            image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)

        image.save(file_path, "WEBP", quality=85)

        return str(file_path)

    except Exception as e:
        print(f"[Artwork Cache Error] {e}")
        return None