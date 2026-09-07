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
- **07.02 Souls & Death** — canonical on `main` via PR #47 at merge `998186beed3522a0821a7dbb911f5e31cd6a9e1d`; exact-SHA post-merge workflow `33981437469` passed the full pipeline. Provider-native gaps remain explicitly fail-closed where verified hooks are insufficient.
- **07.03 Projection & Arsenal** — canonical on `main` via PR #50 at merge `8631c614e7e319a46ab6b29fe7ab33b3903fc2ef`; final PR-head and post-merge full CI were GREEN. Real-modpack/provider host acceptance remains deferred.
- **07.04 Space & Displacement** — canonical on `main` via PR #52 at merge `a567419f1cccd3a33db95402fcb267c0ad79bc67`; exact-SHA post-merge full CI was GREEN. Real-modpack/provider/manual acceptance remains deferred.
- **07.05 Black Flame** — canonical on `main` via PR #54 at runtime merge `f57f2547977e48ac2bbd3bb912371913784ea1ba`; PR-head and exact-SHA post-merge full CI were GREEN. Real-modpack/provider/manual acceptance remains deferred.
- **07.06 Forbidden Domains** — canonical on `main` via PR #59 at runtime merge `836623d39d3060de1b8830000c43d493305cd740`; PR-head and exact-SHA post-merge full CI were GREEN. D032 keeps the implementation bounded to localized fields in already-loaded dimensions.
- **07.07 Familiars & Divination** — `IN PROGRESS`. PR #72 merged the bounded server Noetic/familiar/gaze/sanctuary substrate at `5c818c12bb6f580893e44f31fd0e17b9c1fe5840`, with exact-SHA CI GREEN and 103/103 GameTests. Production camera/HUD/input and the complete per-spell specification gate are still missing for Astral Severance/Borrowed Sight, so 07.07 is **not** promoted as a completed domain.

Historical stacked Stage 07 branches/PR #22 remain reviewed source material only and are not canonical integration ancestry. Every canonical domain is integrated sequentially from the then-current `main`.

Stage 08 Progression & Balance must not start from 07.07 as canonical balance input until the missing 07.07 production mechanics and per-spell specifications are completed and reviewed.
