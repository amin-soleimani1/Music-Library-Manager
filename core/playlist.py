from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlayLists:
    id: int
    name: str
