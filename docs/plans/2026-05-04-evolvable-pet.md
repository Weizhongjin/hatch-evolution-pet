# Evolvable Pet System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first working version of the evolvable pet system by creating a new `hatch-evolution-pet` skill, a separate pet rules file, a machinespace-backed evolution ledger, daily Desktop token aggregation, and the create/evolve workflow glue without modifying Codex Desktop.

**Architecture:** The implementation keeps Codex Desktop unchanged and treats `~/.codex/pets/` as the output surface only. All system rules, lineage metadata, progression state, and aggregation logic live in a new skill rooted under `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet`, backed by `~/.codex/pet-machinespace/` as the runtime workspace and a small `~/.codex/AGENTS.md` hook that points Codex at the skill's rule file.

**Tech Stack:** Markdown skills, Python 3 standard library scripts, existing `hatch-pet` scripts and prompt patterns, local JSON files, local Codex Desktop session JSONL data, local Codex Desktop SQLite state.

---

## File Structure

### New skill workspace

- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/rules/pet-system-rules.md`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/references/`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/README.md`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_paths.py`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_state.py`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_usage_aggregate.py`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_progression.py`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_line_profile.py`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_evolution_brief.py`

### Machinespace runtime data

- Create on first run: `~/.codex/pet-machinespace/evolution-state.json`
- Create on first run: `~/.codex/pet-machinespace/lines/<line-id>/profile.json`
- Create on first run: `~/.codex/pet-machinespace/lines/<line-id>/evolution-briefs/<stage>.json`
- Create on first run: `~/.codex/pet-machinespace/lines/<line-id>/generation-history/`

### Existing user config integration

- Modify: `~/.codex/AGENTS.md`

### Existing skill reference sources

- Read-only reference: `/Users/weizhongjin/.codex/skills/hatch-pet/SKILL.md`
- Read-only reference: `/Users/weizhongjin/.codex/skills/hatch-pet/scripts/*.py`

---

### Task 1: Scaffold the new skill and standalone rules file

**Files:**
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/rules/pet-system-rules.md`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/README.md`
- Test: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md`

- [ ] **Step 1: Write the failing structure check**

Create a small shell verification command in the plan notebook or terminal notes:

```bash
test -f /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md
test -f /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/rules/pet-system-rules.md
test -f /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/README.md
```

- [ ] **Step 2: Run the structure check to verify it fails**

Run:

```bash
test -f /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md && echo PASS || echo FAIL
```

Expected: `FAIL`

- [ ] **Step 3: Create the minimal skill skeleton**

Write `SKILL.md` with a top section like:

```md
---
name: hatch-evolution-pet
description: Create, evolve, validate, and package Codex-compatible pets with persistent progression rules and machinespace-backed lineage state.
---

# Hatch Evolution Pet

## Overview

This skill extends hatch-pet into a persistent pet progression workflow.

Always read `rules/pet-system-rules.md` before running create, prompt, progression, or evolution actions.

This skill is also responsible for teaching Codex how to:
- add or update the lightweight pet-system hook in `~/.codex/AGENTS.md`
- initialize and maintain `~/.codex/pet-machinespace/`

Use this skill when the user wants to:
- create a new evolving pet
- review pet progression status
- respond to an evolution-ready reminder
- evolve an existing pet line
```

Write `rules/pet-system-rules.md` with the agreed rules, starting with:

```md
# Pet System Rules

## State Locations

- Desktop-facing pets: `~/.codex/pets/`
- Machinespace: `~/.codex/pet-machinespace/`
- Evolution ledger: `~/.codex/pet-machinespace/evolution-state.json`

## XP Rules

- under 50,000 daily tokens: 0 XP
- at or above 50,000 daily tokens: 100 XP base
- at or above 1,000,000 daily tokens: 300 XP cap
- after first ignored evolution reminder: final awarded XP is reduced by 50%

## Required System Maintenance Instructions

- ensure `~/.codex/pet-machinespace/` exists before any create, sync, prompt, or evolve action
- ensure `~/.codex/pet-machinespace/evolution-state.json` exists or can be initialized on demand
- if pet-system integration is missing from `~/.codex/AGENTS.md`, add the minimal hook section that points Codex at this rules file
```

Write `scripts/README.md` with a file inventory and one-line purpose per script.

- [ ] **Step 4: Run the structure check to verify it passes**

Run:

```bash
test -f /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md
test -f /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/rules/pet-system-rules.md
test -f /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/README.md
echo $?
```

Expected: `0`

- [ ] **Step 5: Commit**

```bash
git add /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/rules/pet-system-rules.md /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/README.md
git commit -m "Define the new hatch-evolution-pet workflow surface

Constraint: Pet rules must live outside AGENTS.md
Rejected: Reusing hatch-pet name | new flow is broader than hatching only
Confidence: high
Scope-risk: narrow
Directive: Keep the skill entrypoint thin and move operational rules into the rules file
Tested: Verified required skill files exist
Not-tested: Runtime workflow behavior"
```

### Task 2: Implement shared machinespace path and ledger helpers

**Files:**
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_paths.py`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_state.py`
- Test: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_state.py`

- [ ] **Step 1: Write the failing smoke command**

Plan the first smoke check:

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_state.py --print-default-state
```

- [ ] **Step 2: Run the smoke check to verify it fails**

Run:

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_state.py --print-default-state
```

Expected: Python file not found or import failure

- [ ] **Step 3: Write the minimal path and state implementation**

Create `pet_paths.py` with:

```python
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
```

Create `pet_state.py` with:

```python
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone

from pet_paths import EVOLUTION_STATE_PATH, ensure_machinespace_dirs


def default_state() -> dict:
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
        "updatedAt": datetime.now(timezone.utc).isoformat(),
    }


def load_state() -> dict:
    ensure_machinespace_dirs()
    if not EVOLUTION_STATE_PATH.exists():
        return default_state()
    return json.loads(EVOLUTION_STATE_PATH.read_text())


def save_state(state: dict) -> None:
    ensure_machinespace_dirs()
    state["updatedAt"] = datetime.now(timezone.utc).isoformat()
    EVOLUTION_STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-default-state", action="store_true")
    args = parser.parse_args()
    if args.print_default_state:
        print(json.dumps(default_state(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the smoke check to verify it passes**

Run:

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_state.py --print-default-state
```

Expected: pretty-printed default ledger JSON

- [ ] **Step 5: Commit**

```bash
git add /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_paths.py /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_state.py
git commit -m "Establish a stable machinespace ledger foundation

Constraint: The first version must keep state in local JSON under ~/.codex/pet-machinespace
Rejected: Hiding state inside Desktop package folders | state and package lifecycle should stay separate
Confidence: high
Scope-risk: narrow
Directive: Extend the ledger schema compatibly; do not repurpose existing fields for new meanings
Tested: Printed default state and ensured machinespace directory creation
Not-tested: Concurrent state writers"
```

### Task 3: Implement daily Desktop token aggregation and XP accounting

**Files:**
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_usage_aggregate.py`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_progression.py`
- Modify: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/rules/pet-system-rules.md`
- Test: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_progression.py`

- [ ] **Step 1: Write the failing aggregation command**

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_usage_aggregate.py --date 2026-05-03
```

- [ ] **Step 2: Run the aggregation command to verify it fails**

Run the command above.

Expected: file not found or import failure

- [ ] **Step 3: Write the aggregation and XP scripts**

Create `pet_usage_aggregate.py` with a JSONL scan shaped like:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

SESSIONS_ROOT = Path.home() / ".codex" / "sessions"


def iter_session_files_for_day(day: str):
    year, month, date = day.split("-")
    day_dir = SESSIONS_ROOT / year / month / date
    if not day_dir.exists():
        return []
    return sorted(day_dir.glob("rollout-*.jsonl"))


def aggregate_day_tokens(day: str) -> int:
    total = 0
    for session_path in iter_session_files_for_day(day):
        for raw_line in session_path.read_text().splitlines():
            line = json.loads(raw_line)
            payload = line.get("payload", {})
            if line.get("type") != "event_msg":
                continue
            if payload.get("type") != "token_count":
                continue
            last_usage = payload.get("info", {}).get("last_token_usage", {})
            total += int(last_usage.get("total_tokens", 0))
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    print(aggregate_day_tokens(args.date))
```

Create `pet_progression.py` with XP logic shaped like:

```python
from __future__ import annotations

import argparse
import json
from math import floor

from pet_state import load_state, save_state
from pet_usage_aggregate import aggregate_day_tokens


def compute_daily_xp(tokens: int) -> int:
    if tokens < 50_000:
        return 0
    if tokens >= 1_000_000:
        return 300
    return 100 + floor((tokens - 50_000) / 4_750)


def apply_penalty(xp: int, xp_penalty_active: bool) -> int:
    return xp // 2 if xp_penalty_active else xp
```

Extend the script so `--sync-date YYYY-MM-DD` loads the state, stores:

```json
{
  "dailyUsage": {
    "2026-05-03": {
      "totalTokens": 84231,
      "qualifiedActiveDay": true,
      "xpAwarded": 107,
      "xpReason": {
        "baseActiveDayXp": 100,
        "bonusTokenXp": 7,
        "dailyCapApplied": false,
        "penaltyApplied": false
      }
    }
  }
}
```

and does not re-award XP if the date is already present.

- [ ] **Step 4: Run the aggregation and sync checks**

Run:

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_usage_aggregate.py --date 2026-05-03
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_progression.py --sync-date 2026-05-03
```

Expected:

- first command prints a non-negative integer
- second command prints the synced day summary and writes `~/.codex/pet-machinespace/evolution-state.json`

- [ ] **Step 5: Commit**

```bash
git add /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_usage_aggregate.py /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_progression.py /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/rules/pet-system-rules.md
git commit -m "Turn Desktop usage into daily pet progression

Constraint: XP must be derived from Desktop-local session data without modifying Desktop
Rejected: Per-thread token accounting as the primary source | pet progression should reflect global usage across all projects
Confidence: medium
Scope-risk: moderate
Directive: Keep aggregation idempotent per date; never double-award a day
Tested: Aggregated one real Desktop day and synced it into the ledger
Not-tested: Corrupted session JSONL handling"
```

### Task 4: Add prompt-state tracking and evolution reminder logic

**Files:**
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py`
- Modify: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_progression.py`
- Modify: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/rules/pet-system-rules.md`
- Test: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py`

- [ ] **Step 1: Write the failing reminder command**

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py --record-dialogue
```

- [ ] **Step 2: Run the reminder command to verify it fails**

Run the command above.

Expected: file not found or import failure

- [ ] **Step 3: Write the reminder state logic**

Create `pet_prompt_state.py` with helper functions like:

```python
from __future__ import annotations

from datetime import datetime, timezone

from pet_state import load_state, save_state


def should_prompt(state: dict) -> bool:
    if not state.get("upgradeReady"):
        return False
    if state.get("lastUpgradePromptedAt") is None:
        return True
    return state.get("dialoguesSinceUpgradePrompt", 0) >= 10


def record_dialogue(state: dict) -> dict:
    if state.get("upgradeReady") and state.get("lastUpgradePromptedAt") is not None:
        state["dialoguesSinceUpgradePrompt"] = state.get("dialoguesSinceUpgradePrompt", 0) + 1
    return state


def mark_prompted(state: dict) -> dict:
    state["lastUpgradePromptedAt"] = datetime.now(timezone.utc).isoformat()
    state["dialoguesSinceUpgradePrompt"] = 0
    state["xpPenaltyActive"] = True
    return state
```

Expose commands:

```bash
python pet_prompt_state.py --record-dialogue
python pet_prompt_state.py --should-prompt
python pet_prompt_state.py --mark-prompted
```

Update the rules file with the exact reminder semantics:

- first reminder on the first subsequent conversation after reaching a milestone
- after that, re-prompt every 10 conversations
- XP penalty activates only after the first reminder has been shown and ignored

- [ ] **Step 4: Run the reminder smoke checks**

Run:

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py --should-prompt
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py --record-dialogue
```

Expected:

- first command prints `true` or `false`
- second command prints updated dialogue counters without crashing

- [ ] **Step 5: Commit**

```bash
git add /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_progression.py /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/rules/pet-system-rules.md
git commit -m "Make evolution reminders predictable and stateful

Constraint: Evolution prompts must be sparse and tied to dialogue cadence
Rejected: Prompting every day regardless of usage | too noisy
Confidence: high
Scope-risk: narrow
Directive: Keep prompt counters separate from XP totals so reminder bugs cannot corrupt progression
Tested: Exercised prompt decision and dialogue counter commands locally
Not-tested: Multi-thread reminder contention"
```

### Task 5: Implement pet line profile and evolution brief generation

**Files:**
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_line_profile.py`
- Create: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_evolution_brief.py`
- Modify: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md`
- Test: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_line_profile.py`

- [ ] **Step 1: Write the failing profile creation command**

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_line_profile.py --line-id gigimon --custom-name 小基 --pet-display-name Gigimon --origin "tiny digital hatchling" --personality "curious and clingy" --must-keep "red body" --must-keep "horn silhouette" --growth-tendency "gentle dragon"
```

- [ ] **Step 2: Run the command to verify it fails**

Run the command above.

Expected: file not found or import failure

- [ ] **Step 3: Write the profile and brief writers**

Create `pet_line_profile.py` with profile output like:

```python
{
  "lineId": "gigimon",
  "customName": "小基",
  "initialPetDisplayName": "Gigimon",
  "origin": "tiny digital hatchling",
  "corePersonality": "curious and clingy",
  "mustKeepVisualAnchors": ["red body", "horn silhouette"],
  "growthTendency": "gentle dragon"
}
```

Create `pet_evolution_brief.py` with output like:

```python
{
  "lineId": "gigimon",
  "fromStage": 0,
  "toStage": 1,
  "currentPetId": "gigimon",
  "currentPetDisplayName": "Gigimon",
  "customName": "小基",
  "confirmedDirection": "warmer, more dragon-like, still compact and friendly",
  "mustKeepVisualAnchors": ["red body", "horn silhouette"],
  "createdAt": "2026-05-04T00:00:00Z"
}
```

Update `SKILL.md` so create flow explicitly requires:

- background collection
- base image confirmation
- full pet generation only after confirmation
- machinespace initialization before writing profile data
- verifying the `~/.codex/AGENTS.md` hook exists before relying on ambient pet reminders

and evolve flow explicitly requires:

- reading the profile
- grounding suggestions in profile data
- confirming evolution base art before full generation
- reading the standalone rules file before touching reminder or progression state

- [ ] **Step 4: Run the profile and brief commands**

Run:

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_line_profile.py --line-id gigimon --custom-name 小基 --pet-display-name Gigimon --origin "tiny digital hatchling" --personality "curious and clingy" --must-keep "red body" --must-keep "horn silhouette" --growth-tendency "gentle dragon"
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_evolution_brief.py --line-id gigimon --from-stage 0 --to-stage 1 --current-pet-id gigimon --current-pet-display-name Gigimon --custom-name 小基 --confirmed-direction "warmer, more dragon-like, still compact and friendly"
```

Expected: both commands print written JSON file paths and create files under `~/.codex/pet-machinespace/lines/gigimon/`

- [ ] **Step 5: Commit**

```bash
git add /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_line_profile.py /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_evolution_brief.py /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md
git commit -m "Ground pet creation and evolution in explicit profile data

Constraint: Evolution suggestions must come from the pet's established identity
Rejected: Freeform evolution prompts without profile grounding | too easy to drift away from the pet line
Confidence: high
Scope-risk: moderate
Directive: Keep profile fields stable because later prompts and briefs depend on them by name
Tested: Created one profile and one evolution brief end-to-end
Not-tested: Non-ASCII shell quoting on every launcher path"
```

### Task 6: Wire create and evolve workflows onto the existing hatch-pet runtime

**Files:**
- Modify: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md`
- Modify: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/README.md`
- Read and mirror selectively: `/Users/weizhongjin/.codex/skills/hatch-pet/scripts/prepare_pet_run.py`
- Read and mirror selectively: `/Users/weizhongjin/.codex/skills/hatch-pet/scripts/finalize_pet_run.py`
- Test: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md`

- [ ] **Step 1: Write the failing workflow checklist**

Define the expected behavior checklist:

```text
create flow -> collect profile -> generate base -> ask for confirmation -> run hatch pipeline
evolve flow -> confirm eligibility -> read profile -> write brief -> generate evolution base -> ask for confirmation -> run hatch pipeline -> unlock new pet
```

- [ ] **Step 2: Verify the old skill does not yet expose the new workflow**

Run:

```bash
rg -n "hatch-evolution-pet|evolve flow|base image confirmation" /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md
```

Expected: missing sections for at least one of the new workflows

- [ ] **Step 3: Expand the skill instructions with explicit create/evolve branches**

Add sections shaped like:

```md
## Create Flow

1. Collect line profile data and write `profile.json`.
2. Ensure `~/.codex/pet-machinespace/` and `evolution-state.json` exist.
3. Ensure the minimal pet hook exists in `~/.codex/AGENTS.md`.
4. Prepare a base-image-only prompt.
5. Use image generation to produce the base concept.
6. Ask the user to confirm the base image.
7. Only after confirmation, call the inherited hatch pipeline to build the full pet package.

## Evolve Flow

1. Read `evolution-state.json` and the current line `profile.json`.
2. Ensure the minimal pet hook exists in `~/.codex/AGENTS.md`.
3. Verify that `upgradeReady` is true for the current stage.
4. Collaborate on an evolution direction grounded in the profile.
5. Write an evolution brief JSON file.
6. Generate the next-form base image.
7. Ask the user to confirm the base image.
8. Only after confirmation, run the full generation pipeline and package the new unlocked form under `~/.codex/pets/`.
9. Update the ledger to append the unlocked form and clear the pending prompt state.
```

Document which existing `hatch-pet` scripts are reused unchanged and which new scripts wrap them.

- [ ] **Step 4: Run the workflow checklist validation**

Run:

```bash
rg -n "## Create Flow|## Evolve Flow|profile.json|evolution-state.json|base image" /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md
```

Expected: matches for all the listed anchors

- [ ] **Step 5: Commit**

```bash
git add /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/SKILL.md /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/README.md
git commit -m "Turn hatching into a full create-and-evolve workflow

Constraint: Full spritesheet generation must still be grounded in the existing hatch-pet asset pipeline
Rejected: Rewriting the whole image pipeline from scratch | unnecessary risk and duplication
Confidence: medium
Scope-risk: moderate
Directive: Keep base-art confirmation mandatory before any full pet generation run
Tested: Verified the skill doc now exposes explicit create and evolve branches
Not-tested: Actual end-to-end image generation through the new skill"
```

### Task 7: Hook global Codex awareness to the standalone pet rules file

**Files:**
- Modify: `~/.codex/AGENTS.md`
- Test: `~/.codex/AGENTS.md`

- [ ] **Step 1: Write the failing lookup check**

```bash
rg -n "hatch-evolution-pet|pet-system-rules.md|pet-machinespace" /Users/weizhongjin/.codex/AGENTS.md
```

- [ ] **Step 2: Run the lookup check to verify it fails**

Run the command above.

Expected: no matches

- [ ] **Step 3: Add a minimal integration section to AGENTS.md**

Insert a small section shaped like:

```md
## Pet System

When the user asks about Codex pets, pet progression, pet evolution, hatch-evolution-pet, or upgrading their companion:

- Read `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/rules/pet-system-rules.md`
- Treat `~/.codex/pet-machinespace/` as the pet system workspace
- Use `hatch-evolution-pet` as the primary workflow surface for pet creation and pet evolution
```

Keep the section short and avoid duplicating the full rules.

- [ ] **Step 4: Run the lookup check to verify it passes**

Run:

```bash
rg -n "hatch-evolution-pet|pet-system-rules.md|pet-machinespace" /Users/weizhongjin/.codex/AGENTS.md
```

Expected: all three strings are present

- [ ] **Step 5: Commit**

```bash
git add /Users/weizhongjin/.codex/AGENTS.md
git commit -m "Teach Codex where to find the pet system rules

Constraint: AGENTS.md should point to the pet rules instead of re-embedding them
Rejected: Copying the full XP and reminder rules into AGENTS.md | invites drift
Confidence: high
Scope-risk: narrow
Directive: Keep AGENTS.md as an integration hook only; evolve pet behavior in the rules file
Tested: Verified the new AGENTS.md hook strings are present
Not-tested: Prompt-following behavior in a fresh future session"
```

### Task 8: Run end-to-end dry runs for create, sync, reminder, and evolve bookkeeping

**Files:**
- Test: `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/*.py`
- Test: `~/.codex/pet-machinespace/evolution-state.json`
- Test: `~/.codex/pet-machinespace/lines/<line-id>/`

- [ ] **Step 1: Prepare a disposable test line**

Use:

```bash
rm -rf ~/.codex/pet-machinespace/lines/plan-test-line
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_line_profile.py --line-id plan-test-line --custom-name 测试兽 --pet-display-name Testimon --origin "testing hatchling" --personality "patient" --must-keep "red accent" --growth-tendency "calmer dragon"
```

- [ ] **Step 2: Run the daily sync once and verify idempotence**

Run:

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_progression.py --sync-date 2026-05-03
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_progression.py --sync-date 2026-05-03
```

Expected:

- first run writes or updates one day entry
- second run reports that the date is already synced and does not add XP again

- [ ] **Step 3: Simulate an upgrade-ready reminder lifecycle**

Run:

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py --mark-upgrade-ready --level 5
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py --should-prompt
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py --mark-prompted
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_prompt_state.py --record-dialogue
```

Expected:

- first prompt becomes eligible
- `xpPenaltyActive` switches to `true` only after `--mark-prompted`
- dialogue counter increments after prompting

- [ ] **Step 4: Simulate unlocking a new form without forcing display switch**

Run:

```bash
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_evolution_brief.py --line-id plan-test-line --from-stage 0 --to-stage 1 --current-pet-id testimon --current-pet-display-name Testimon --custom-name 测试兽 --confirmed-direction "sleeker but still friendly"
python /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/scripts/pet_progression.py --unlock-pet testimon-stage-2 --pet-display-name Testimon Evo
```

Expected:

- `unlockedPetIds` contains both forms
- `observedSelectedAvatarId` remains unchanged unless explicitly refreshed from Desktop state

- [ ] **Step 5: Commit**

```bash
git add /Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet
git commit -m "Prove the evolvable pet loop before image generation rollout

Constraint: The first release needs a dry-run-safe bookkeeping path before relying on image generation
Rejected: Waiting for a full UI before validating state transitions | slows feedback too much
Confidence: medium
Scope-risk: moderate
Directive: Keep the dry-run commands working because they are the fastest regression checks for future changes
Tested: Profile creation, daily sync idempotence, reminder transitions, unlock bookkeeping
Not-tested: Live image generation through the full evolve path"
```

## Self-Review

### Spec coverage

- standalone rules file inside the skill: covered by Tasks 1 and 7
- renamed `hatch-evolution-pet` workflow: covered by Tasks 1 and 6
- `pet-machinespace` ledger and profile data: covered by Tasks 2 and 5
- global daily Desktop token aggregation: covered by Task 3
- reminder and XP-penalty rules: covered by Task 4
- create flow with background collection and base-image confirmation: covered by Tasks 5 and 6
- evolve flow with grounded suggestions and base-image confirmation: covered by Tasks 5 and 6
- unlocked form independent from displayed form: covered by Tasks 2, 4, and 8

No spec sections are intentionally left without a task.

### Placeholder scan

- No `TODO`, `TBD`, or "implement later" placeholders remain in the plan.
- Every task lists exact file paths.
- Every code-writing step includes a concrete code skeleton or exact content.
- Every verification step includes an exact command and expected outcome.

### Type consistency

Shared field names used consistently through the plan:

- `activePetId`
- `observedSelectedAvatarId`
- `customName`
- `petDisplayName`
- `upgradeReady`
- `lastUpgradePromptedAt`
- `dialoguesSinceUpgradePrompt`
- `xpPenaltyActive`
- `unlockedPetIds`

Shared directories used consistently through the plan:

- `~/.codex/pets/`
- `~/.codex/pet-machinespace/`
- `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet/`
