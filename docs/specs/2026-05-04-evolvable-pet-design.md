# Evolvable Pet System Design

Date: 2026-05-04

## Summary

This design extends the current Codex pet workflow into a lightweight evolvable pet system without modifying Codex Desktop itself. The system keeps Desktop as a manual pet picker, while adding a separate growth and evolution workflow driven by skill logic, persisted local state, and explicit user collaboration.

The new system has four core properties:

1. Pets continue to be packaged as independent folders under `~/.codex/pets/` so Desktop can present them as normal selectable pets.
2. Pet growth state, lineage history, and evolution working data live outside the Desktop-facing package directory in a dedicated `~/.codex/pet-machinespace/` workspace.
3. The existing `hatch-pet` workflow is expanded and renamed to `hatch-evolution-pet`, which becomes the main authoring and evolution workflow skill.
4. Pet system rules live in a dedicated rules file inside the skill. `AGENTS.md` should only tell Codex when to read and follow that file, not embed the whole pet system contract inline.

## Goals

- Create an evolvable pet system that works with the current Codex Desktop pet picker.
- Keep old and newly unlocked forms available side by side instead of forcing replacement.
- Let users co-design pet evolution only when evolution becomes available, rather than locking a full evolution tree up front.
- Make pet growth depend on actual Codex usage over time.
- Keep the system generic enough to support Digimon-like growth as one example, not a hardcoded theme.

## Non-Goals

- No Codex Desktop code changes in the first version.
- No automatic avatar switching after evolution.
- No hidden background daemon requirement in the first version.
- No pre-generated full evolution tree requirement.
- No dependence on symlinks for Desktop pet switching.

## System Boundaries

The system is split into four layers:

### 1. Desktop-facing pet packages

`~/.codex/pets/` stores packaged, selectable pets. Each unlocked form is a normal pet package with its own folder, `pet.json`, and `spritesheet.webp`.

Desktop treats these as normal pets. The evolution system does not try to replace this mechanism.

### 2. Pet machinespace

`~/.codex/pet-machinespace/` stores all internal working state for the pet system, including:

- evolution ledger
- pet line profile and background
- evolution briefs
- generation records
- intermediate references
- unlocked-form history

This directory is the pet system's internal workspace and source of truth.

### 3. Workflow skill

The current `hatch-pet` capability evolves into a new skill named `hatch-evolution-pet`. This skill is the single user-facing workflow surface for:

- creating a new pet line
- collecting background and identity data
- generating and validating initial pets
- detecting and running evolution sessions
- generating new unlocked forms
- maintaining machinespace state

The new skill should live in a new skill folder rooted under:

`/Users/weizhongjin/develop_program/lines/personal/projects/active`

### 4. Global Codex awareness

`~/.codex/AGENTS.md` should not contain the full pet system logic. Instead it should include a short rule telling Codex:

- a pet system exists
- where its rules file lives
- when to read that rules file
- when to use the `hatch-evolution-pet` workflow

This keeps the system modular and easier to maintain.

## File Layout

### Desktop-facing packages

```text
~/.codex/pets/
  gigimon/
    pet.json
    spritesheet.webp
  guilmon/
    pet.json
    spritesheet.webp
  ...
```

### Machinespace

```text
~/.codex/pet-machinespace/
  evolution-state.json
  lines/
    <line-id>/
      profile.json
      evolution-briefs/
      references/
      generation-history/
```

### Skill

```text
/Users/weizhongjin/develop_program/lines/personal/projects/active/
  <new-skill-root>/
    SKILL.md
    rules/
      pet-system-rules.md
    scripts/
    references/
```

The exact skill folder name can be chosen during implementation, but the workflow name exposed to Codex should be `hatch-evolution-pet`.

## Core Data Model

The primary state file is:

`~/.codex/pet-machinespace/evolution-state.json`

Recommended first-version structure:

```json
{
  "version": 1,
  "activePetId": "gigimon",
  "observedSelectedAvatarId": "custom:gigimon",
  "petDisplayName": "Gigimon",
  "customName": "Xiao Ji",
  "totalXp": 0,
  "level": 1,
  "currentEvolutionStage": 0,
  "maxEvolutionStages": 5,
  "upgradeReady": false,
  "upgradeReadySince": null,
  "lastUpgradePromptedAt": null,
  "dialoguesSinceUpgradePrompt": 0,
  "xpPenaltyActive": false,
  "evolutionMilestones": [5, 12, 22, 35, 50],
  "unlockedPetIds": ["gigimon"],
  "dailyUsage": {},
  "evolutionHistory": []
}
```

Field intent:

- `activePetId`: the pet form the growth system currently treats as the active lineage anchor for progression bookkeeping
- `observedSelectedAvatarId`: the Desktop avatar currently observed in local Codex state, used only for awareness and messaging

### Naming Model

The system keeps two distinct names:

- `customName`: the user-facing companion name
- `petDisplayName`: the current species or form name

This allows reminders such as:

```text
Your Xiao Ji has reached level 12 and can evolve.
Current form: Gigimon.
You can start a new conversation to upgrade your companion.
```

## Pet Creation Workflow

Initial pet creation becomes a three-stage workflow:

1. Background collection
2. Base image confirmation
3. Full pet generation

### Background collection

The system must collect enough information to support later evolution decisions. At minimum:

- custom companion name
- origin/background
- core personality
- must-keep visual anchors
- growth tendency

The goal is not lore for lore's sake. The goal is to create a stable identity that later evolution suggestions can build from.

### Base image confirmation

Before generating the full spritesheet, the system generates a base image and asks the user to confirm that the pet identity feels right.

Full pet generation only begins after that confirmation.

## Evolution Workflow

Evolution is not a forced skin replacement and not a pre-written tree.

Instead:

1. The pet reaches an evolution milestone.
2. Codex reminds the user that evolution is available.
3. The user starts a new conversation to evolve the companion.
4. Codex collaborates with the user on the next-form direction.
5. A subagent runs the generation workflow.
6. A new pet package is produced and added to `~/.codex/pets/`.
7. The new form is unlocked, but the user may keep using the old form.

### Evolution suggestions

Evolution suggestions must be grounded in the existing pet line. Suggestions should consider:

- original background
- current form and silhouette
- must-keep traits
- previously unlocked forms
- previously chosen evolution tendencies

The system should not propose arbitrary upgrades disconnected from the pet's established identity.

### Confirmation point

Evolution should also include a base-image confirmation step before full spritesheet generation:

1. agree on direction
2. generate evolution base image
3. user confirms base image
4. run full pet generation

## XP Model

XP is computed globally by day across all Codex Desktop usage, not per project and not per thread.

### Source data

The design assumes we can derive global daily token usage by aggregating Desktop session data across the day.

### Daily rules

- under `50,000` total tokens: `0 XP`
- at or above `50,000` total tokens: grant `100 XP`
- at `1,000,000` total tokens: cap at `300 XP`
- daily XP cap: `300`

Recommended formula:

```text
if tokens < 50_000:
    xp = 0
elif tokens >= 1_000_000:
    xp = 300
else:
    xp = 100 + floor((tokens - 50_000) / 4_750)
```

This gives:

- `50,000` tokens -> `100 XP`
- `1,000,000` tokens -> `300 XP`

### XP penalty after ignored evolution prompt

Reaching an evolution milestone does not immediately reduce XP.

Penalty starts only after:

1. the user has reached an evolution milestone
2. the first evolution reminder has been shown
3. the user still does not start evolution

After that point, XP gain is reduced by `50%` until the relevant evolution flow is completed.

## Level Curve and Evolution Milestones

The chosen milestone targets are:

- first evolution at `Lv5`
- second evolution at `Lv12`
- third evolution at `Lv22`
- fourth evolution at `Lv35`
- fifth evolution at `Lv50`

This keeps early evolution accessible, then slows later growth naturally.

The desired pacing is:

- first evolution after roughly two full-XP days
- second evolution after roughly one week of full-XP days
- third evolution after roughly three weeks of full-XP days
- fourth and fifth may slow down more noticeably

### First 30 levels: proposed XP curve

```text
Lv1  -> Lv2   120
Lv2  -> Lv3   140
Lv3  -> Lv4   160
Lv4  -> Lv5   180

Lv5  -> Lv6   180
Lv6  -> Lv7   190
Lv7  -> Lv8   200
Lv8  -> Lv9   210
Lv9  -> Lv10  220
Lv10 -> Lv11  240
Lv11 -> Lv12  260

Lv12 -> Lv13  300
Lv13 -> Lv14  330
Lv14 -> Lv15  360
Lv15 -> Lv16  390
Lv16 -> Lv17  420
Lv17 -> Lv18  420
Lv18 -> Lv19  450
Lv19 -> Lv20  480
Lv20 -> Lv21  510
Lv21 -> Lv22  540

Lv22 -> Lv23  550
Lv23 -> Lv24  580
Lv24 -> Lv25  610
Lv25 -> Lv26  640
Lv26 -> Lv27  670
Lv27 -> Lv28  700
Lv28 -> Lv29  730
Lv29 -> Lv30  760
```

The implementation may tune exact values later, but should preserve the agreed pacing targets.

## Reminder Rules

When a user reaches an evolution milestone:

1. mark `upgradeReady = true`
2. wait until the first subsequent user conversation
3. show the first reminder
4. if still not evolved, enable XP penalty
5. re-prompt every 10 conversations

The first conversation of a day is not special beyond being part of the normal conversation count.

Recommended reminder copy:

```text
Your <customName> has reached level <level> and can evolve.
Current form: <petDisplayName>.
You can start a new conversation to upgrade your companion.
```

## Unlocking vs Using a Form

Completing an evolution session unlocks a new pet form. It does not force the user to switch to it.

This distinction is intentional:

- progress state tracks what forms are unlocked
- Desktop avatar selection tracks what form is currently displayed

`activePetId` in the ledger should therefore not be treated as "the avatar currently displayed on screen". That display state remains independent and may still point at an older unlocked form.

A user may continue using an old form after a new one has been unlocked.

## Skill Responsibilities

The new `hatch-evolution-pet` skill should own:

- initial pet creation workflow
- background collection
- base image confirmation
- evolution prompt handling
- evolution direction collaboration
- evolution brief writing
- subagent execution for generation
- packaging new unlocked forms into `~/.codex/pets/`
- updating machinespace state

The skill should provide two high-level workflow surfaces:

- create a new pet line
- evolve an existing pet line

## Rules File Responsibilities

The pet system rules should live in a dedicated file inside the skill, for example:

```text
rules/pet-system-rules.md
```

That rules file should define:

- state file locations
- XP rules
- reminder rules
- evolution flow rules
- naming rules
- unlock-vs-display semantics

## AGENTS.md Responsibilities

`~/.codex/AGENTS.md` should only contain a lightweight integration hook describing:

- where the pet rules file lives
- when to consult it
- when to invoke the `hatch-evolution-pet` skill

It should not duplicate the pet system's full logic.

## Testing and Validation

The first implementation should verify:

- daily token aggregation is stable
- XP accounting is idempotent
- repeated reads do not double-award XP
- unlock state advances only after successful evolution completion
- old and new pet forms remain selectable independently
- failed evolution generation does not corrupt the ledger

## Open Implementation Decisions

These are intentionally deferred to planning and implementation:

- exact on-disk skill folder name under `/Users/weizhongjin/develop_program/lines/personal/projects/active`
- exact profile JSON schema
- exact evolution brief schema
- exact subagent prompt template shape
- exact Desktop session data aggregation script

They do not block the architecture or workflow design above.
