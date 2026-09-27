# Release-bounded lower-bound audit — Reliquified L_Ender's Cataclysm 0.1.1

Checkpoint: 2026-09-27

## Disposition

`LOWER_BOUND 7 / +0 STRICT`

The audit deliberately does not use `COUNTED_RELEASE_BOUNDED`. Exact-current 0.1.1 completeness is not proven.

## Physical authority

- installed runtime: `0.1.1`;
- installed JAR: `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`;
- installed SHA-1: `be89d697455f04a1531ed81b45bcc038354430c8`;
- sibling checkpoint: `neoforge-rpg-skilltree@ac23fc1c67937deeffe982ae971c21d4f3561bc5`.

## Publisher release line

CurseForge project `1232116` contains two public 1.21.1 release files:

| File | Version | Upload | Publisher change |
|---|---|---|---|
| `6415478` | `0.1` | 2025-04-12 | Initial release |
| `6882649` | `0.1.1` | 2025-08-13 | Fixed compatibility with OctoLib 0.6 |

The compatibility-only changelog is not treated as a proof of complete content equality.

## Initial-release source baseline

Official public repository:
`Octo-Studios/reliquified-lenders-cataclysm`

Release-day checkpoint:
`291f066c0471e44f50fe78ea8e7d786f6775446e`

The checkpoint declares `mod_version=0.1`, registers five relic items and exposes seven localized owner-scoped ability roots:

| Owner | Ability root | Display name |
|---|---|---|
| Scouring Eye | `glowing_scour` | Pursuit |
| Void Vortex in Bottle | `spawn_vortex` | Void Tornado |
| Void Cloak | `void_invulnerability` | Invulnerability |
| Void Cloak | `void_rune` | Call of the Void |
| Void Cloak | `seismic_zone` | Final Cry |
| Vacuum Glove | `vacuum_slowdown` | The Edge |
| Void Bubble | `protective_bubble` | Protective Bubble |

This proves a release-line lower bound of seven semantic ability roots.

## Current assembled-stack corroboration

Project Library log `latest(20260908-134522).log` contains exactly ten occurrences of `reliquified_lenders_cataclysm/items/relics/`, representing two load/transform phases over the same five item classes:

1. Void Cloak;
2. Scouring Eye;
3. Void Vortex in Bottle;
4. Vacuum Glove;
5. Void Bubble.

No additional relic item class under that namespace appears in that log.

This corroborates the five known current classes but is not a formal registry-completeness proof. The compatibility coremod may only log classes it transforms, and a hidden/additional semantic root could theoretically exist outside that logged surface.

## Why the strict ledger remains unchanged

The strict ledger requires a reconstructible complete denominator for a provider row. Current evidence does not exclude:

- an undocumented 0.1.1-only ability root;
- an additional root in one of the five classes not represented by the initial 0.1 baseline;
- a provider action outside the compatibility transformer's logged class surface.

Therefore **7 is a lower bound**, not a strict contribution.

## Clean-room boundary

Upstream is All Rights Reserved. This audit uses public source metadata/registry/localization facts, publisher release metadata and current-pack logs. No provider implementation is copied, and no ARR bytecode is decompiled merely to force closure.

## Closure requirement

Require exact-current 0.1.1 source, a bounded exact-artifact registry proof compatible with clean-room rules, or deterministic complete assembled-registry evidence before changing this provider to ✅.
