# Ars Nouveau — Conjure Water

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_conjure_water`
- Display name: Conjure Water
- School: Elemental Water
- Default tier: 2
- Default mana cost: 80
- Compatible augments: AOE, Pierce, Extend Time, Sensitive
- Default Sensitive limit: 1
- Source default Soaked duration: 20 s
- Source default Extend Time increment: 10 s

## Provider-native behavior

Conjure Water places water at eligible block targets outside ultra-warm dimensions and extinguishes burning entities. With duration amplification through Extend Time it can apply Ars `Soaked`; Sensitive can place water at a target entity's feet. Block placement respects claim checks and supports `LiquidBlockContainer` waterlogging/placement semantics.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:water_essence` + `minecraft:water_bucket`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns generic magical water placement/extinguishing and its Soaked status. Black Arcana must not duplicate provider water placement or use this as permission to bypass its own world-effect policy for independent fluid mutations.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectConjureWater`).
