# Hatch Evolution Pet Start Here

Workspace:

- `/Users/weizhongjin/develop_program/lines/personal/projects/active/hatch-evolution-pet`

Core documents:

- Spec: `docs/specs/2026-05-04-evolvable-pet-design.md`
- Plan: `docs/plans/2026-05-04-evolvable-pet.md`

Current repository layout:

- Project README and showcase assets live at the repository root.
- The installable Codex skill lives in `hatch-evolution-pet/`.
- To install, copy `hatch-evolution-pet/` to `~/.codex/skills/hatch-evolution-pet/`.

Immediate implementation target:

1. Create the new `hatch-evolution-pet` skill structure.
2. Add the standalone pet rules file.
3. Add machinespace ledger helpers under `~/.codex/pet-machinespace/`.
4. Follow the implementation plan task by task.

Important constraints:

- This implementation is not in the `codex` repo.
- New files should be written directly under this workspace.
- Pet system rules should live in the skill's rules file, not inline in `AGENTS.md`.
- `AGENTS.md` should only contain a lightweight hook that points Codex to the rules file.
