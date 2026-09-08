# Access Ender Inventory

- Registry ID: `ars_nouveau:glyph_ender_inventory`
- Source class: `EffectEnderChest`
- School: Manipulation
- Default tier: **2**
- Default mana: **50**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

When resolved by a real `Player` rather than a fake player, this effect opens that player's personal Ender Chest inventory through the provider-owned menu path. It has no compatible augments in the exact 5.13.1 class.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:ender_chest`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns this remote Ender-inventory access surface. Black Arcana must not create a second Ender-inventory authority or bypass normal player/container permissions under the guise of a generic remote-storage spell.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.