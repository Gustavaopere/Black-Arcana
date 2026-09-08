# Ars Nouveau — Name

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_name`
- Display name: Name
- School: Manipulation
- Default tier: 2
- Default mana cost: 25
- Compatible augments: none

## Provider-native behavior

Name derives a new name first from an available Name Tag through the Ars inventory manager, otherwise from the held caster tool's configured spell name. It can rename entities, held off-hand items, dropped item stacks, skull ownership text and nameable container blocks. Named mobs are marked persistent.

## Authority / deduplication

Ars Nouveau owns this naming/persistence utility. Black Arcana should not duplicate generic remote naming or silently manipulate Ars-associated persistence through a second effect path.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectName`).
