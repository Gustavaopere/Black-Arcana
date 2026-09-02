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

- **07.01 Blood & Curses** — implemented on fresh latest-`main` PR #45; automated branch validation is GREEN, including JUnit, NeoForge build, JAR inspection, 34 required GameTests and dedicated-server smoke. Final real-modpack/manual acceptance remains deferred under D031.
- **07.02–07.07** — not implemented by PR #45 and remain pending.

Historical stacked Stage 07 branches/PR #22 are reviewed source material only and are not canonical integration ancestry. Each later domain must start from the latest canonical `main` after its predecessor is promoted.

The stage may be split into sequential domain branches if the review surface becomes too large; 07.01 establishes that pattern.
