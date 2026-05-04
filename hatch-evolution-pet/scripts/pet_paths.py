from __future__ import annotations

from pathlib import Path

CODEX_HOME = Path.home() / ".codex"
PET_MACHINE_SPACE = CODEX_HOME / "pet-machinespace"
EVOLUTION_STATE_PATH = PET_MACHINE_SPACE / "evolution-state.json"
LINES_DIR = PET_MACHINE_SPACE / "lines"
PETS_DIR = CODEX_HOME / "pets"


def ensure_machinespace_dirs() -> None:
    PET_MACHINE_SPACE.mkdir(parents=True, exist_ok=True)
    LINES_DIR.mkdir(parents=True, exist_ok=True)


def ensure_pets_dir() -> None:
    PETS_DIR.mkdir(parents=True, exist_ok=True)


def line_dir(line_id: str) -> Path:
    return LINES_DIR / line_id

