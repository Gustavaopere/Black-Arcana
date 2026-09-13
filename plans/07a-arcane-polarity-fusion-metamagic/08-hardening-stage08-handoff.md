# 07A.08 — Hardening & Stage 08 Handoff

## State

`PLANNED / NOT IMPLEMENTED`

## Objective

Close 07A with deterministic evidence, bounded performance and a clean handoff to Stage 08 so balance work receives frozen semantics rather than unresolved ownership questions.

## Required test layers

### Unit/contract tests

Cover:

- polarity source/agency/consent resolution;
- fusion compatibility and transformation ordering;
- metamagic admission/conflicts;
- cost/hazard/world-policy transformation math;
- bounded integer/fixed-point accounting where blood/life/resource conversion exists;
- schema validation and reload rejection;
- replay/dedup semantics;
- provider support-state resolution.

### GameTests

Cover representative world/entity behavior:

- fused target selection and caps;
- destructive infusion through WorldEffectPolicy;
- Echo/Anchor session lifecycle;
- Ankh/Soul Anchor exactly-once composition;
- Sanguine Harvest and 07.08 blood accounting with no duplicate credits;
- ritual material reservation and cancellation;
- sigil presentation events cannot mutate server state;
- logout/death/dimension/reload cleanup;
- boss/PvP protection rules;
- bounded scheduler saturation behavior.

### Provider integration tests

For every selected provider adapter, test supported and fail-closed paths using exact-version fixtures/contracts available to the project. Do not mark real renderer or real-modpack behavior PASS from mocks alone.

### Build/runtime gates

On the final reconciled branch HEAD:

- unit/JUnit suite;
- NeoForge build;
- built-JAR inspection;
- all required GameTests;
- dedicated-server smoke;
- static/provenance checks;
- current provider audit drift checks applicable to 07A.

## Performance budgets

Before Stage 08 handoff, freeze structural ceilings even if exact balance numbers remain tunable:

- maximum fusion secondary targets;
- maximum fusion/Metamagic scheduled work per cast;
- maximum Echo count = bounded, initial architecture one;
- maximum channel/session lifetime;
- maximum sigil primitive/payload counts;
- maximum ritual offering slots/material entries;
- no global player/entity/chunk scans;
- no chunk forcing for targets, rituals or sigils;
- no unbounded recursive composition.

Representative performance evidence is required later wherever existing project validation convention defers final real-modpack measurement under D031.

## Stage 08 handoff package

For every 07A mechanic, Stage 08 receives:

- stable mechanic id and original player-facing name;
- canonical domain/authority;
- polarity resolution mode;
- resource/cost formula inputs;
- cooldown inputs;
- target/range/area/target-count ceilings;
- hazard coefficients/transform inputs;
- boss/PvP policy;
- progression gate hooks;
- provider dependency/support status;
- world-effect mode;
- config surface;
- explicit anti-exploit notes;
- deterministic tests;
- provenance reference.

Stage 08 chooses final quantitative curves, tiers and progression placement. Stage 08 does not redesign who owns the cast, ritual, resource or hazard runtime.

## Explicit exploit cases to close

- fusion child double-cost/double-refund;
- fusion/echo duplicate XP/Mastery/loot/procs;
- reconnect/reload repetition of ritual/unlock/Ankh charge;
- PvP consent laundering through party/team state;
- Sanctify laundering an extractive source into Luminal presentation;
- Predation resource-positive loops;
- Blood/Hematic Reserve/Vampirism rounding minting;
- arbitrary sigil payload/network amplification;
- provider absent -> free cost/protection/effect;
- provider generic event + specific event double-processing;
- recursive fusion/metamagic combinations;
- stale cached provider capability after reload/lifecycle invalidation.

## Promotion rule

Do not rename/promote Stage 07A tasks merely because plan files exist or code compiles. Promotion requires the task's runtime on the latest reconciled branch, relevant deterministic gates green, review complete and merge to `main`. Final manual/real-modpack rows remain explicit if deferred under D031.

## Acceptance

Stage 07A hands off only when:

- all eight work packages are implemented or explicitly rescoped by reviewed decision;
- no known architecture/provider ownership ambiguity remains;
- exact Mahou reference disposition is complete for all adopted mechanics;
- no protected Mahou asset/code/content is shipped;
- final branch is synchronized with latest main and all applicable gates rerun after that synchronization;
- STATUS/DECISIONS/provenance docs record the exact final state and SHAs.
