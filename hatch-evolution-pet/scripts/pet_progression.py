from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from math import floor
from typing import Any

from pet_state import load_state, save_state
from pet_usage_aggregate import aggregate_day_tokens

XP_PER_LEVEL = 100


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def compute_daily_xp(tokens: int) -> int:
    if tokens < 50_000:
        return 0
    if tokens >= 1_000_000:
        return 300
    return min(300, 100 + floor((tokens - 50_000) / 4_750))


def apply_penalty(xp: int, xp_penalty_active: bool) -> int:
    return xp // 2 if xp_penalty_active else xp


def xp_reason(tokens: int, raw_xp: int, awarded_xp: int, penalty: bool) -> dict[str, Any]:
    base = 100 if tokens >= 50_000 else 0
    return {
        "baseActiveDayXp": base,
        "bonusTokenXp": max(0, raw_xp - base),
        "dailyCapApplied": tokens >= 1_000_000 or raw_xp >= 300,
        "penaltyApplied": penalty and raw_xp != awarded_xp,
    }


def level_for_xp(total_xp: int) -> int:
    return max(1, total_xp // XP_PER_LEVEL + 1)


def update_upgrade_state(state: dict[str, Any]) -> None:
    stage = int(state.get("currentEvolutionStage", 0))
    milestones = state.get("evolutionMilestones", [])
    if stage >= len(milestones):
        state["upgradeReady"] = False
        return
    if int(state.get("level", 1)) >= int(milestones[stage]):
        if not state.get("upgradeReady"):
            state["upgradeReady"] = True
            state["upgradeReadySince"] = now_utc()


def sync_date(day: str) -> dict[str, Any]:
    state = load_state()
    daily_usage = state.setdefault("dailyUsage", {})
    if day in daily_usage:
        return {
            "date": day,
            "alreadySynced": True,
            "dailyUsage": daily_usage[day],
            "totalXp": state.get("totalXp", 0),
            "level": state.get("level", 1),
            "upgradeReady": state.get("upgradeReady", False),
        }

    tokens = aggregate_day_tokens(day)
    raw_xp = compute_daily_xp(tokens)
    penalty_active = bool(state.get("xpPenaltyActive", False))
    awarded_xp = apply_penalty(raw_xp, penalty_active)
    qualified = tokens >= 50_000

    summary = {
        "totalTokens": tokens,
        "qualifiedActiveDay": qualified,
        "xpAwarded": awarded_xp,
        "xpReason": xp_reason(tokens, raw_xp, awarded_xp, penalty_active),
        "syncedAt": now_utc(),
    }
    daily_usage[day] = summary
    state["totalXp"] = int(state.get("totalXp", 0)) + awarded_xp
    state["level"] = level_for_xp(int(state["totalXp"]))
    update_upgrade_state(state)
    save_state(state)

    return {
        "date": day,
        "alreadySynced": False,
        "dailyUsage": summary,
        "totalXp": state["totalXp"],
        "level": state["level"],
        "upgradeReady": state.get("upgradeReady", False),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync-date")
    parser.add_argument("--compute-xp", type=int)
    args = parser.parse_args()

    if args.compute_xp is not None:
        print(compute_daily_xp(args.compute_xp))
        return
    if args.sync_date:
        print(json.dumps(sync_date(args.sync_date), indent=2, ensure_ascii=False))
        return
    parser.print_help()


if __name__ == "__main__":
    main()

