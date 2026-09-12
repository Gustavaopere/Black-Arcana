# Phase 2BG — Leyline Spellbooks 1.0.3 exact checkpoint

## Baseline

- branch base: `main@91fe79e8479f7c82a7e922f64d4806a3e7abafe1`;
- physical modlist: 595 top-level entries, SHA-1 `7aaece7acbfb07ba4d0c66029042f36c50d046f0`;
- Minecraft `1.21.1`, NeoForge `21.1.248`, Java 21;
- canonical semantic minimum entering Phase 2BG: **874**;
- canonical provider-component closure entering Phase 2BG: **55/100 = 55%**.

These baseline values remain canonical until the durable Phase 2BG PR is merged and exact post-merge CI is green.

## Exact provider evidence

Physical artifact:

- `leylines-1.0.3.jar`;
- mod id/runtime `leylines` / `1.0.3`;
- CurseForge project/file `1636676 / 8565076`;
- SHA-1 `dfa6908731f432905caaaa1e53b4aedeaa26ed59`.

Temporary non-merge evidence PR #194 produced three independent hash-gated text artifacts:

1. primary registry audit — run `34666436710`, artifact `10289437099`;
2. targeted reachability audit — run `34666652534`, artifact `10289292617`;
3. school/loot-gate audit — run `34667641655`, artifact `10289184487`.

## Closure result

The exact JAR closes **14 unconditional `AbstractSpell` registrations** under one provider `DeferredRegister<AbstractSpell>`. Exact resource IDs are recorded in [`../providers/leyline-spellbooks/EXACT-1.0.3-SPELL-INVENTORY.md`](../providers/leyline-spellbooks/EXACT-1.0.3-SPELL-INVENTORY.md).

The former nine-name publisher list is superseded as the registry ceiling; it remains useful historical publisher evidence only.

Active/survival eligibility is materially stronger than registry membership alone:

- exact Leylines spell classes do not override Iron's `allowLooting()` or `isEnabled()`;
- exact Ley school construction uses Iron's seven-argument `SchoolType` constructor;
- exact Iron's 3.16.3 source pin `e4056af90302d37eb1739f5ff05020b020e6e252` defines that constructor with `requiresLearning=false` and `allowLooting=true`;
- Iron's empty spell filter enumerates enabled spells and its randomize-spell loot function defaults to that filter;
- exact Iron's survival loot includes unfiltered randomized scrolls;
- Leylines also adds a dedicated `charge_leyline` scroll injection.

No provider-specific spell-lock/config eligibility gate analogous to Somake was established. The six observed `LeylinesConfig` values govern spell behavior rather than registration/learning eligibility.

## Candidate semantic/component delta

On this branch only, Phase 2BG proposes:

- Leyline Spellbooks semantic delta: **+14**;
- Iron's ecosystem subtotal: **527 -> 541**;
- strict reconstructible semantic minimum: **874 -> 888**;
- provider-component closure: **55/100 -> 56/100**;
- component #56: Leyline Spellbooks 1.0.3.

Arithmetic candidate: `199 + 541 + 42 + 55 + 25 + 26 = 888`.

The global semantic denominator remains incomplete, so no semantic percentage is declared.

## Remaining fail-closed boundaries

This catalog closure does not claim:

- final assembled-pack numerical spell config values or balance QA;
- exact loot probabilities after all datapack/modifier interactions;
- exact pillar/rift persistence, packet schema or multiplayer ownership internals;
- stable provider-native Black Arcana adapter/API hooks;
- runtime acceptance in the complete modpack.

Leyline owns its spell/school/progression/portal/anchor/rift state. Iron's owns the host casting/mana/scroll substrate. Black Arcana must not duplicate either authority and retains its own canonical server-authoritative casting, Arcane Danger, Corruption, Strain, rituals, hazards and `WorldEffectPolicy`.

## Promotion gate

Candidate values become canonical only after:

1. durable Phase 2BG diff contains no temporary audit/generation workflows or provider binaries;
2. Black Arcana CI is GREEN on the exact clean PR HEAD;
3. latest `main` is reconciled immediately before merge;
4. the PR merges with the validated expected HEAD;
5. Black Arcana CI is GREEN on the exact merge SHA, including main-only QA artifact publication;
6. final evidence is recorded without inventing CI/merge identifiers.

PR #194 remains evidence-only and must be closed without merge after durable/final evidence is canonical.
