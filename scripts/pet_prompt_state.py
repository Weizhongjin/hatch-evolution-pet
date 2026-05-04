from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Any

from pet_state import load_state, save_state


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def should_prompt(state: dict[str, Any]) -> bool:
    if not state.get("upgradeReady"):
        return False
    if state.get("lastUpgradePromptedAt") is None:
        return True
    return int(state.get("dialoguesSinceUpgradePrompt", 0)) >= 10


def record_dialogue(state: dict[str, Any]) -> dict[str, Any]:
    if state.get("upgradeReady") and state.get("lastUpgradePromptedAt") is not None:
        state["dialoguesSinceUpgradePrompt"] = int(
            state.get("dialoguesSinceUpgradePrompt", 0)
        ) + 1
    return state


def mark_prompted(state: dict[str, Any]) -> dict[str, Any]:
    state["lastUpgradePromptedAt"] = now_utc()
    state["dialoguesSinceUpgradePrompt"] = 0
    state["xpPenaltyActive"] = True
    return state


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-dialogue", action="store_true")
    parser.add_argument("--should-prompt", action="store_true")
    parser.add_argument("--mark-prompted", action="store_true")
    args = parser.parse_args()

    state = load_state()
    if args.should_prompt:
        print("true" if should_prompt(state) else "false")
        return
    if args.record_dialogue:
        save_state(record_dialogue(state))
        print(json.dumps(load_state(), indent=2, ensure_ascii=False))
        return
    if args.mark_prompted:
        save_state(mark_prompted(state))
        print(json.dumps(load_state(), indent=2, ensure_ascii=False))
        return
    parser.print_help()


if __name__ == "__main__":
    main()

