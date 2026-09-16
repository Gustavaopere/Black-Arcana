# Ars Nouveau — Name

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_name`
- Display name: Name
- School: Manipulation
- Default tier: 2
- Default mana cost: 25
- Compatible augments: none

## Provider-native behavior

Name derives a new name first from an available Name Tag through the Ars inventory manager, otherwise from the held caster tool's configured spell name. It can rename entities, held off-hand items, dropped item stacks, skull ownership text and nameable container blocks. Named mobs are marked persistent.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:name_tag`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this naming/persistence utility. Black Arcana should not duplicate generic remote naming or silently manipulate Ars-associated persistence through a second effect path.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectName`).
