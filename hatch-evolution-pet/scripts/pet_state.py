from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Any

from pet_paths import EVOLUTION_STATE_PATH, ensure_machinespace_dirs


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_state() -> dict[str, Any]:
    return {
        "version": 1,
        "activePetId": None,
        "observedSelectedAvatarId": None,
        "petDisplayName": None,
        "customName": None,
        "totalXp": 0,
        "level": 1,
        "currentEvolutionStage": 0,
        "maxEvolutionStages": 5,
        "upgradeReady": False,
        "upgradeReadySince": None,
        "lastUpgradePromptedAt": None,
        "dialoguesSinceUpgradePrompt": 0,
        "xpPenaltyActive": False,
        "evolutionMilestones": [5, 12, 22, 35, 50],
        "unlockedPetIds": [],
        "dailyUsage": {},
        "evolutionHistory": [],
        "updatedAt": now_utc(),
    }


def load_state() -> dict[str, Any]:
    ensure_machinespace_dirs()
    if not EVOLUTION_STATE_PATH.exists():
        return default_state()
    return json.loads(EVOLUTION_STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    ensure_machinespace_dirs()
    state["updatedAt"] = now_utc()
    EVOLUTION_STATE_PATH.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def init_state() -> dict[str, Any]:
    state = load_state()
    save_state(state)
    return state


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-default-state", action="store_true")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--print-state", action="store_true")
    args = parser.parse_args()

    if args.print_default_state:
        print(json.dumps(default_state(), indent=2, ensure_ascii=False))
        return
    if args.init:
        print(json.dumps(init_state(), indent=2, ensure_ascii=False))
        return
    if args.print_state:
        print(json.dumps(load_state(), indent=2, ensure_ascii=False))
        return
    parser.print_help()


if __name__ == "__main__":
    main()
