# Ars Nouveau — Craft

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_craft`
- Display name: Craft
- School: Manipulation
- Default tier: 1
- Default mana cost: 50
- Compatible augments: none

## Provider-native behavior

Opens a remote crafting menu for a real player caster. Ars provides a crafting menu whose validity is not tied to remaining near a workstation.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:crafting_table`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

This provider already owns generic remote crafting. Black Arcana should not add another plain crafting-access spell unless the mechanic materially changes into a forbidden-magic contract rather than duplicating utility.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectCraft`).
