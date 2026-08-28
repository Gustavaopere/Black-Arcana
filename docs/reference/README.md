# Reference catalog

This directory contains clean-room planning material. Reference names may appear here only to identify publicly documented behavior; they are not player-facing Black Arcana identifiers and must not leak into registries, localization, assets, lore, or implementation names.

## Rules

1. Use public documentation, changelogs and observable gameplay behavior.
2. Do not decompile Mahou Tsukai or inspect its implementation source/assets.
3. Describe mechanics at the level of inputs, outputs, constraints, fantasy and risk.
4. Before coding a retained mechanic, use the Black Arcana specification in `classification-matrix.md`, not the reference implementation.
5. Host-mod capabilities are planning evidence, not permission to depend on unstable internals. Stage 03 must verify real APIs before writing adapters.

## Documents

- `mahou-observable-catalog.md` — behavioral inventory of candidate ideas.
- `host-capability-map.md` — current overlap/extension map for Iron's, Ars Nouveau, Eidolon: Repraised and Malum.
- `classification-matrix.md` — Black Arcana disposition and original target design.
