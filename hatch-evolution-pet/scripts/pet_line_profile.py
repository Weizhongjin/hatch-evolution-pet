from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Any

from pet_paths import line_dir
from pet_state import load_state, save_state


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def profile_path(line_id: str):
    return line_dir(line_id) / "profile.json"


def write_profile(
    line_id: str,
    custom_name: str,
    pet_display_name: str,
    origin: str,
    personality: str,
    must_keep: list[str],
    growth_tendency: str,
) -> dict[str, Any]:
    target_dir = line_dir(line_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "evolution-briefs").mkdir(exist_ok=True)
    (target_dir / "references").mkdir(exist_ok=True)
    (target_dir / "generation-history").mkdir(exist_ok=True)

    profile = {
        "lineId": line_id,
        "customName": custom_name,
        "initialPetDisplayName": pet_display_name,
        "origin": origin,
        "corePersonality": personality,
        "mustKeepVisualAnchors": must_keep,
        "growthTendency": growth_tendency,
        "createdAt": now_utc(),
        "updatedAt": now_utc(),
    }
    path = profile_path(line_id)
    path.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    state = load_state()
    state["activePetId"] = state.get("activePetId") or line_id
    state["petDisplayName"] = state.get("petDisplayName") or pet_display_name
    state["customName"] = state.get("customName") or custom_name
    unlocked = state.setdefault("unlockedPetIds", [])
    if line_id not in unlocked:
        unlocked.append(line_id)
    save_state(state)
    return {"path": str(path), "profile": profile}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--line-id", required=True)
    parser.add_argument("--custom-name", required=True)
    parser.add_argument("--pet-display-name", required=True)
    parser.add_argument("--origin", required=True)
    parser.add_argument("--personality", required=True)
    parser.add_argument("--must-keep", action="append", default=[])
    parser.add_argument("--growth-tendency", required=True)
    args = parser.parse_args()

    print(
        json.dumps(
            write_profile(
                args.line_id,
                args.custom_name,
                args.pet_display_name,
                args.origin,
                args.personality,
                args.must_keep,
                args.growth_tendency,
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

