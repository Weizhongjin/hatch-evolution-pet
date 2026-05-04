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

Both forms are normal selectable Codex pets:

![Codex pet picker showing multiple forms](assets/readme/codex-pet-picker.png)

## Rules

- Desktop-facing pet packages live in `~/.codex/pets/`.
- Runtime state lives in `~/.codex/pet-machinespace/`.
- Main ledger: `~/.codex/pet-machinespace/evolution-state.json`.
- Evolution rules live in `hatch-evolution-pet/rules/pet-system-rules.md`.
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

Install the skill by copying the `hatch-evolution-pet/` skill folder into `~/.codex/skills/`:

```bash
cp -R /path/to/repo/hatch-evolution-pet ~/.codex/skills/hatch-evolution-pet
```

Restart Codex or start a new conversation so the skill list refreshes.

Then use the skill in Codex:

```text
[$hatch-evolution-pet](~/.codex/skills/hatch-evolution-pet/SKILL.md)
我要创建一个属于的 pet，我希望他叫小基基，实际是数码宝贝第三部中主角基尔兽的幼年体基基兽。图片可以参考，进化路线参考数码宝贝进化的风格，应该是基尔兽、古拉兽、大古拉兽、红莲骑士兽这样，越来越强，越来越帅。
```

Example creation prompt:

![gigi creation chat](assets/readme/gigi-creation-chat.png)

That is enough for the skill to initialize machinespace, collect identity details, generate a base image for confirmation, and then run the pet generation workflow.

For progression checks, ask Codex naturally, for example: "Check my pet XP" or "Can my pet evolve now?"

## Personal Notes

For those of us born in the 90s and mid-to-late 90s, there is a good chance that *Digimon* was part of our childhood. We have grown from the age of the "Chosen Children" into the age of adults like Yukio Oikawa, Mitsuo Yamaki, and Lee Janyuu.

But when I first saw the tiny pixel-style Codex pet, the first thing that flashed through my mind was the moment Guilmon was born. In that instant, I suddenly felt that the real Digital World might already be here. It does not look exactly like the world we saw in the anime when we were kids, but it awakened that same childhood dream in me: to have a digital partner that truly belongs to me, an AI companion that stays with me and grows alongside me.

This project started from that feeling. It brought back the imagination I had as a child about the Digital World, and it made me feel that maybe this is only a very small beginning.

I hope that, in the future, more people can build together in the age of AI and create a Digital World that belongs to this new era, and to all of us.
