# Ars Controle

Status: `CURRENT HIGH-IMPACT GLYPHS VERIFIED FROM ARS 1.21.1 PROVIDER-AWARE GUIDE; FULL ADDON AUDIT CONTINUES`

- Current JAR: `ars_controle-1.21.1-1.6.15.jar`
- Mod id: `ars_controle`
- Runtime version: `1.21.1-1.6.15`
- Provider class: `ARS GLYPH / SYSTEM PROVIDER`
- Primary casting authority: Ars Nouveau.

## Current verified glyph surface

The current Ars 1.21.1 guide exposes addon ownership by registry namespace. The following `ars_controle:` entries are verified in the current guide:

| Glyph | Registry id | Tier | Base cost | Semantic role |
|---|---|---:|---:|---|
| Filter: Above | `ars_controle:glyph_filter_above` | 1 | 0 | resolve only above caster |
| Filter: Below | `ars_controle:glyph_filter_below` | 1 | 0 | resolve only below caster |
| Filter: Level | `ars_controle:glyph_filter_level` | 1 | 0 | resolve at caster elevation |
| Filter: NOT | `ars_controle:glyph_filter_not` | 1 | 0 | invert next filter result |
| Filter: OR | `ars_controle:glyph_filter_or` | 1 | 0 | resolve if either following filter is true |
| Filter: Random | `ars_controle:glyph_filter_random` | 1 | 0 | probabilistic resolution gate |
| Filter: XNOR | `ars_controle:glyph_filter_xnor` | 1 | 0 | resolve when two following filter results are equal |
| Filter: XOR | `ars_controle:glyph_filter_xor` | 1 | 0 | resolve when exactly one following filter is true |
| Precise Delay | `ars_controle:glyph_precise_delay` | 2 | 0 | deterministic tick-scale delayed continuation |

## Filter: Random — exact public probability semantics

The current public guide documents:

- base resolution chance: **50%**;
- with net Amplification `A`: `100% - 50% / (2^A)`;
- with net Dampening `D`: `50% / (2^D)`.

This is not merely random visual selection. It is a genuine player-composable probability gate in the installed pack.

## Deduplication impact

### Chaos

This addon proves that **probability manipulation already exists** in the current pack at the spell-composition level. Black Arcana Chaos cannot be approved on the premise that “sometimes the effect happens” or “the player can raise/lower a random chance” is unique.

A candidate Chaos mechanic now needs a stronger delta, for example one or more of:

- weighted families of outcomes rather than a binary resolve/fail gate;
- persistent entropy/instability state carried between casts;
- probability debt/compensation over repeated events;
- controlled rule corruption in a bounded domain;
- transactional world/entity state distortion with canonical rollback;
- cross-provider outcome selection with explicit authority and deduplication.

Those are design directions only; they remain blocked until all related providers are cataloged.

### Order

The boolean filters (`NOT`, `OR`, `XNOR`, `XOR`) already allow logical spell constraints. Order therefore cannot claim generic “logic” as unique either. Its remaining candidate identity must involve authoritative imposed laws/seals/constraints at gameplay-state level, not just boolean composition inside one Ars spell chain.

### Timing

`Precise Delay` directly occupies deterministic spell scheduling. Order/Chaos/temporal designs must avoid reproducing simple delayed execution.

## Provenance / confidence

- Presence/version: current modlist — HIGH.
- Registry ids, tiers, costs and public semantics above: current Ars 1.21.1 guide — HIGH.
- Full addon inventory beyond the verified entries above: still under Phase 2 audit.
- No Java bytecode was decompiled.
