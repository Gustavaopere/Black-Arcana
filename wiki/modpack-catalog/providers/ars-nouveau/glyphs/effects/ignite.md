# Ignite

- Registry ID: `ars_nouveau:glyph_ignite`
- Source class: `EffectIgnite`
- School: Elemental Fire
- Default tier: **1**
- Default mana: **15**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Ignite sets entities on fire for a configurable duration and can light/create fire around block targets using provider AOE/depth calculations and claim checks. Sensitive changes the block path to Ars Nouveau's short-lived magic fire, which the provider describes as non-spreading/non-destructive. It can also light compatible candles/campfires.

Compatible augments: Extend Time, AOE, Pierce, Reduce Time, Sensitive. Sensitive is limited to 1 by default.

## Boundary

Normal or magic fire created by Ars remains provider-owned. Black Arcana fire/world mutations must still route through `WorldEffectPolicy`; Sensitive's provider behavior is not a universal proof of world-safety for other spells.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.