# Pet System Rules

## State Locations

- Desktop-facing pets: `~/.codex/pets/`
- Machinespace: `~/.codex/pet-machinespace/`
- Evolution ledger: `~/.codex/pet-machinespace/evolution-state.json`
- Line profiles: `~/.codex/pet-machinespace/lines/<line-id>/profile.json`
- Evolution briefs: `~/.codex/pet-machinespace/lines/<line-id>/evolution-briefs/`
- Generation history: `~/.codex/pet-machinespace/lines/<line-id>/generation-history/`

## Boundary Rules

- Do not modify Codex Desktop to implement the pet system.
- Keep Desktop-facing packages as normal selectable pet folders under `~/.codex/pets/`.
- Keep all growth state, lineage state, briefs, references, and generation history in machinespace.
- Keep old and newly unlocked forms available side by side.
- Do not use symlinks as the required Desktop pet switching mechanism.
- Do not embed the full pet system contract in `AGENTS.md`; only add a lightweight hook pointing to this rules file.

## Required System Maintenance

- Ensure `~/.codex/pet-machinespace/` exists before any create, sync, prompt, progression, or evolve action.
- Ensure `~/.codex/pet-machinespace/evolution-state.json` exists or can be initialized on demand.
- Ensure `~/.codex/pets/` exists before packaging an unlocked form.
- If pet-system integration is missing from `~/.codex/AGENTS.md`, add the minimal hook section that points Codex at this rules file and names the `hatch-evolution-pet` workflow.

## Naming Model

- `customName` is the user-facing companion name.
- `petDisplayName` is the current species or form name.
- Use both when reminding the user, for example: "`customName` can evolve. Current form: `petDisplayName`."

## XP Rules

- Under 50,000 daily tokens: `0 XP`
- At or above 50,000 daily tokens: `100 XP` base
- Between 50,000 and 1,000,000 daily tokens: add `floor((tokens - 50,000) / 4,750)` bonus XP
- At or above 1,000,000 daily tokens: `300 XP` cap
- Daily XP cap: `300`
- After the first ignored evolution reminder, final awarded XP is reduced by 50%.
- XP is global by day across Codex Desktop usage, not per project and not per thread.
- Never double-award XP for a date that is already recorded in `dailyUsage`.

## Evolution Reminder Rules

- A pet becomes evolution-ready when its level reaches the next configured evolution milestone.
- The first reminder appears on the first subsequent conversation after reaching a milestone.
- After the first reminder, re-prompt every 10 conversations while evolution remains available.
- `xpPenaltyActive` activates only after the first reminder has been shown and ignored.
- Keep prompt counters separate from XP totals so reminder mistakes cannot corrupt progression.

## Creation Rules

- Collect the companion name, origin/background, core personality, must-keep visual anchors, and growth tendency before full generation.
- Generate or obtain a base image first.
- Ask the user to confirm the base identity before running full spritesheet generation.
- Store stable identity data in the line profile before relying on it for future evolution suggestions.

## Evolution Rules

- Evolution is additive, not a forced replacement.
- Do not pre-generate or require a full evolution tree.
- Collaborate with the user on the next-form direction only when evolution is available.
- Ground suggestions in the existing line profile, current form, must-keep traits, unlocked forms, and prior choices.
- Confirm evolution base art before full generation.
- Add each new unlocked form to `~/.codex/pets/` as a normal Desktop-facing package.

