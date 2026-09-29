# Provider folder status normalization — 2026-09-29

## Purpose

This checkpoint separates **catalog coverage** from **strict runtime activation** for provider directory names.

The directory prefix answers one question only:

> Is the current provider's semantic/action denominator fully cataloged and materialized?

It does not answer whether every identity is enabled, survival-reachable or strict-counted in the deployed pack.

## Promotion rule

A provider can use `✅-` when:

1. its current semantic/action denominator is closed;
2. every identified object has an object-level card or equivalent explicit disposition;
3. aliases/subactions/support objects are deduplicated or excluded;
4. remaining deployment/config/reachability conditions are explicitly documented.

A provider remains `⚠️-` when the **catalog itself** is incomplete, such as missing current scripts, unresolved current artifact/provenance, an open denominator, or missing object-level materialization.

No promotion in this checkpoint changes the strict semantic numerator.

## Promoted to ✅

| Provider | Closed object coverage | Remaining non-catalog gate |
|---|---:|---|
| Asterism Arcanum | 11/11 spell identities | Astral Gateway deployed survival state |
| Corail Tombstone | 22/22 action families | deployed `allow_*` values for 12 castable families |
| Gaze | 27/27 metric-relevant action objects | deployed `disableGazeRites` state for 26 rites |
| Mowzie's Mobs | 11/11 discrete player powers | deployed `enableTunneling` |
| Not Enough Glyphs | 40/40 registered primitives | effective deployed enabled state for 39 source-enabled candidates |
| ShadowsZ | 10/10 supernatural roots | deployed attunement policy and Fusion state |
| Simply More | 24/24 current action roots | deployed Awakening/acquisition/Mimicry/config reachability |
| Simply Swords: Cataclysm | 4/4 supernatural weapon abilities | deployed STARTUP config activation |
| Somake Spells | 83/83 current 1.0.9 registry identities | deployed host/lock config and survival reachability |

New directory names:

- `✅-asterism-arcanum`
- `✅-corail-tombstone`
- `✅-gaze`
- `✅-mowzies-mobs`
- `✅-not-enough-glyphs`
- `✅-shadowsz`
- `✅-simply-more`
- `✅-simply-swords-cataclysm`
- `✅-somake-spells`

## Intentionally still ⚠️

| Provider | Why the catalog is still incomplete |
|---|---|
| Ice and Fire CE | object-level action-card PR #458 is still open |
| Iron's Spellbooks KubeJS | current-pack script-defined Iron's inventory is unavailable |
| KubeJS Ars Nouveau | current-pack KubeJS Ars mutation inventory is unavailable |
| Simply Swords | object-level action-card PR #456 is still open |
| Traveloptics | current physical artifact/provenance and current registry delta are unresolved |

## Structural result

Before normalization:

`115 providers = 101 ✅ + 14 ⚠️`

After normalization:

`115 providers = 110 ✅ + 5 ⚠️`

## Post-materialization follow-up — PRs #456 and #458

The two remaining providers whose only catalog blocker was missing object-level materialization are now closed on `main`:

| Provider | Object coverage now materialized | Folder result | Remaining non-catalog gate |
|---|---:|---|---|
| Simply Swords 1.70.2 | 66/66 action roots | `✅-simply-swords` | deployed Awakening/config/acquisition/compat reachability |
| Ice And Fire CE 2.1.2 | 9/9 magic-action families | `✅-ice-and-fire-ce` | deployed `tools.phantasmalBladeAbility` for Ghost Sword plus runtime QA |

Evidence:

- PR #456 merged after synchronization to the then-current `main`; post-sync Black Arcana CI run `36638143201` completed successfully;
- PR #458 was then synchronized to the new `main`; post-sync Black Arcana CI run `36638910371` completed successfully.

Current structural result after these two promotions:

`115 providers = 112 ✅ + 3 ⚠️`

The three intentionally catalog-open folders are:

- `⚠️-irons-spellbooks-kubejs` — current-pack script-defined Iron's inventory remains unavailable;
- `⚠️-kubejs-ars-nouveau` — current-pack KubeJS Ars mutation inventory remains unavailable;
- `⚠️-traveloptics` — current physical row #550 and SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` are confirmed by the current sibling dossier; that physical hash differs from the audited publisher baseline, so exact-current provenance/registry delta remain unresolved.

This is a folder-status normalization only. It does not change registry IDs, spell/action counts, strict semantic totals, runtime compatibility claims or Black Arcana provider authority.
