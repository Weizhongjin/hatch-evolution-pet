from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pet_paths import line_dir


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_profile(line_id: str) -> dict[str, Any]:
    path = line_dir(line_id) / "profile.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def brief_path(line_id: str, to_stage: int) -> Path:
    return line_dir(line_id) / "evolution-briefs" / f"stage-{to_stage}.json"


def write_brief(
    line_id: str,
    from_stage: int,
    to_stage: int,
    current_pet_id: str,
    current_pet_display_name: str,
    custom_name: str,
    confirmed_direction: str,
) -> dict[str, Any]:
    profile = read_profile(line_id)
    target = brief_path(line_id, to_stage)
    target.parent.mkdir(parents=True, exist_ok=True)
    brief = {
        "lineId": line_id,
        "fromStage": from_stage,
        "toStage": to_stage,
        "currentPetId": current_pet_id,
        "currentPetDisplayName": current_pet_display_name,
        "customName": custom_name,
        "confirmedDirection": confirmed_direction,
        "mustKeepVisualAnchors": profile.get("mustKeepVisualAnchors", []),
        "origin": profile.get("origin"),
        "corePersonality": profile.get("corePersonality"),
        "growthTendency": profile.get("growthTendency"),
        "createdAt": now_utc(),
    }
    target.write_text(json.dumps(brief, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"path": str(target), "brief": brief}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--line-id", required=True)
    parser.add_argument("--from-stage", required=True, type=int)
    parser.add_argument("--to-stage", required=True, type=int)
    parser.add_argument("--current-pet-id", required=True)
    parser.add_argument("--current-pet-display-name", required=True)
    parser.add_argument("--custom-name", required=True)
    parser.add_argument("--confirmed-direction", required=True)
    args = parser.parse_args()

    print(
        json.dumps(
            write_brief(
                args.line_id,
                args.from_stage,
                args.to_stage,
                args.current_pet_id,
                args.current_pet_display_name,
                args.custom_name,
                args.confirmed_direction,
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

