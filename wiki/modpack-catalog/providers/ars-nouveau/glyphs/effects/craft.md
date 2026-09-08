# Ars Nouveau — Craft

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_craft`
- Display name: Craft
- School: Manipulation
- Default tier: 1
- Default mana cost: 50
- Compatible augments: none

## Provider-native behavior

Opens a remote crafting menu for a real player caster. Ars provides a crafting menu whose validity is not tied to remaining near a workstation.

## Authority / deduplication

This provider already owns generic remote crafting. Black Arcana should not add another plain crafting-access spell unless the mechanic materially changes into a forbidden-magic contract rather than duplicating utility.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectCraft`).
