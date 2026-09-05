# 07 — Spell Domains

Implement the approved Stage 01 catalog using the frozen core, integration, safety, UX and ritual contracts.

## Rule for every spell
Specification must state: fantasy, host integration, invocation, target rules, resource cost, cooldown, scaling equation, progression gate, world-effect mode, boss/PvP behavior, config surface, tests and provenance link.

## Domains
- Blood & Curses
- Souls & Death
- Projection & Arsenal
- Space & Displacement
- Black Flame
- Forbidden Domains
- Familiars & Divination

## Implementation state

Stage 07 is being promoted as sequential domain-scoped work to keep review and validation surfaces bounded.

- **07.01 Blood & Curses** — canonical on `main` via PR #45; automated branch and post-merge validation are GREEN. Final real-modpack/manual acceptance remains deferred under D031.
- **07.02 Souls & Death** — canonical on `main` via PR #47 at merge `998186beed3522a0821a7dbb911f5e31cd6a9e1d`; exact-SHA post-merge workflow `33981437469` passed JUnit, diff sanity, NeoForge build, JAR inspection, all 40 required GameTests, dedicated-server smoke and canonical QA artifact publication. Provider-native Malum death-to-spirit harvesting and player-specific Eidolon unlock remain explicitly fail-closed where verified hooks lack the required causal/value or caster-identity contracts. Final real-modpack/manual host acceptance remains deferred under D031.
- **07.03 Projection & Arsenal** — implemented on PR #50 from fresh latest-`main` ancestry. Integrated workflow `33990511277` (#986) passed JUnit, diff sanity, NeoForge build, JAR inspection, all 58 required GameTests and dedicated-server smoke. The implementation remains isolated from 07.04: Rift Blades uses canonical Stage 04 world-safety primitives without importing `content/space`. Real-modpack/provider host acceptance remains deferred and is not inferred as PASS. This domain becomes canonical only after PR #50 is merged and the exact post-merge `main` pipeline is green.
- **07.04–07.07** — pending and must follow sequentially from the latest canonical `main`.

Historical stacked Stage 07 branches/PR #22 are reviewed source material only and are not canonical integration ancestry. Each later domain must start from the latest canonical `main` after its predecessor is promoted.

The stage may be split into sequential domain branches if the review surface becomes too large; 07.01 established that pattern, 07.02 continued it and 07.03 preserves the same isolation discipline.
