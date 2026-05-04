# Hatch Evolution Pet

[English](README.md) | [简体中文](README.zh-CN.md)

An evolvable replacement for [`hatch-pet`](https://github.com/openai/skills/tree/main/skills/.curated/hatch-pet).

`hatch-evolution-pet` keeps the original Codex pet generation workflow, then adds local XP, evolution state, lineage records, and unlocked forms. Codex Desktop stays unchanged: every form is still packaged as a normal selectable pet under `~/.codex/pets/`.

## Features

- Evolvable replacement for `hatch-pet`.
- XP and levels from daily Codex usage.
- User-customizable evolution direction instead of a fixed tree.
- New forms unlock as normal selectable Codex pets.
- Old forms and evolved forms stay available side by side, like Digimon: evolved forms can still roll back.

## Example Evolution

| Stage 0 | Stage 1 |
| --- | --- |
| ![Gigimon](assets/readme/gigimon-preview.png) | ![GigiRookie](assets/readme/gigirookie-preview.png) |
| `gigi` / `Gigimon` | `gigi-stage-1` / `GigiRookie` |

## Rules

- Desktop-facing pet packages live in `~/.codex/pets/`.
- Runtime state lives in `~/.codex/pet-machinespace/`.
- Main ledger: `~/.codex/pet-machinespace/evolution-state.json`.
- Evolution rules live in `rules/pet-system-rules.md`.
- `AGENTS.md` should only contain a lightweight hook pointing to the rules file.
- Evolution is additive: a new form is unlocked, not used to overwrite an old form.

### XP

The pet gains XP from daily Codex usage. More token usage gives more XP, but each day has a cap. A recorded day should only be counted once.

### Generation

- Use `$imagegen` for base art and row strips.
- Use canonical base references and layout guides for row generation.
- Record generated outputs with `record_imagegen_result.py`.
- Do not manually edit `imagegen-jobs.json`.
- Do not copy images into `decoded/` as a shortcut.
- Review contact sheets, QA reports, preview videos, and row continuity.

## Quickstart

Install this skill by placing this directory under `~/.codex/skills/`:

```bash
cp -R /path/to/hatch-evolution-pet ~/.codex/skills/hatch-evolution-pet
```

Restart Codex or start a new conversation so the skill list refreshes.

Then use the skill in Codex:

```text
[$hatch-evolution-pet](~/.codex/skills/hatch-evolution-pet/SKILL.md)
I want to create an evolving pet named gigi. Use this reference image and make it grow toward stronger dragon forms.
```

Example creation prompt:

![gigi creation chat](assets/readme/gigi-creation-chat.png)

That is enough for the skill to initialize machinespace, collect identity details, generate a base image for confirmation, and then run the pet generation workflow.

For progression checks, ask Codex naturally, for example: "Check my pet XP" or "Can my pet evolve now?"

## Personal Notes

> Reserved for project motivation and personal notes.
