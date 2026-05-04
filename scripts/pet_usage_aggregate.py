from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

SESSIONS_ROOT = Path.home() / ".codex" / "sessions"


def iter_session_files_for_day(day: str) -> list[Path]:
    year, month, date = day.split("-")
    day_dir = SESSIONS_ROOT / year / month / date
    if not day_dir.exists():
        return []
    return sorted(day_dir.glob("rollout-*.jsonl"))


def iter_jsonl(path: Path) -> Iterable[dict]:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        try:
            yield json.loads(raw_line)
        except json.JSONDecodeError:
            continue


def aggregate_day_tokens(day: str) -> int:
    total = 0
    for session_path in iter_session_files_for_day(day):
        for line in iter_jsonl(session_path):
            payload = line.get("payload", {})
            if line.get("type") != "event_msg":
                continue
            if payload.get("type") != "token_count":
                continue
            info = payload.get("info")
            if not isinstance(info, dict):
                continue
            last_usage = info.get("last_token_usage", {})
            if not isinstance(last_usage, dict):
                continue
            total += int(last_usage.get("total_tokens", 0) or 0)
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    print(aggregate_day_tokens(args.date))


if __name__ == "__main__":
    main()
