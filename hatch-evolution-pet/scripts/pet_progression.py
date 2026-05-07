from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
import fcntl
import json
from math import floor
from typing import Any, Union

from pet_paths import PET_MACHINE_SPACE, ensure_machinespace_dirs
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


@contextmanager
def progression_lock():
    ensure_machinespace_dirs()
    lock_path = PET_MACHINE_SPACE / "evolution-state.lock"
    with lock_path.open("w", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)


def sync_date_into_state(state: dict[str, Any], day: str) -> dict[str, Any]:
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

    return {
        "date": day,
        "alreadySynced": False,
        "dailyUsage": summary,
        "totalXp": state["totalXp"],
        "level": state["level"],
        "upgradeReady": state.get("upgradeReady", False),
    }


def sync_date(day: str) -> dict[str, Any]:
    with progression_lock():
        state = load_state()
        result = sync_date_into_state(state, day)
        if not result["alreadySynced"]:
            save_state(state)
        return result


def iter_date_range(start_day: str, end_day: str) -> list[str]:
    start = date.fromisoformat(start_day)
    end = date.fromisoformat(end_day)
    if end < start:
        raise ValueError("--sync-range end date must be on or after start date")
    days = []
    current = start
    while current <= end:
        days.append(current.isoformat())
        current += timedelta(days=1)
    return days


def sync_dates(days: list[str], include_today: bool = False) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    today = date.today().isoformat()
    with progression_lock():
        state = load_state()
        for day in days:
            if day == today and not include_today:
                results.append(
                    {
                        "date": day,
                        "skipped": True,
                        "skipReason": "current day is still in progress; pass --include-today to settle it intentionally",
                        "totalXp": state.get("totalXp", 0),
                        "level": state.get("level", 1),
                        "upgradeReady": state.get("upgradeReady", False),
                    }
                )
                continue
            results.append(sync_date_into_state(state, day))
        if any(not result.get("alreadySynced", True) and not result.get("skipped") for result in results):
            save_state(state)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sync-date", action="append")
    parser.add_argument("--sync-range", nargs=2, metavar=("START", "END"))
    parser.add_argument("--include-today", action="store_true")
    parser.add_argument("--compute-xp", type=int)
    args = parser.parse_args()

    if args.compute_xp is not None:
        print(compute_daily_xp(args.compute_xp))
        return
    if args.sync_date:
        results = sync_dates(args.sync_date, include_today=args.include_today)
        output: Union[dict[str, Any], list[dict[str, Any]]]
        output = results[0] if len(results) == 1 else results
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return
    if args.sync_range:
        print(
            json.dumps(
                sync_dates(
                    iter_date_range(args.sync_range[0], args.sync_range[1]),
                    include_today=args.include_today,
                ),
                indent=2,
                ensure_ascii=False,
            )
        )
        return
    parser.print_help()


if __name__ == "__main__":
    main()
