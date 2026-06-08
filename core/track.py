from dataclasses import dataclass


@dataclass(slots=True)
class Track:
    track_id: int
    title: str
    is_favorite: bool
    file_path: str
    length: int
    artwork: str | None = None
