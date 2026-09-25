# Dungeon's Delight 1.5.1 — exact source magic-surface inventory

Status: `EXACT SOURCE PIN / REGISTRY BOUNDARY CLOSED / ZERO SPELL-RITUAL-ABILITY REGISTRY`

## Source authority

`Yirmiri/Dungeons-Delight@0c2d621ebc7dcce3df5dad0ea485209ef2396f9c`

Tree:

`3b7135c479ad2ee53b6e6a17c0fcb1238d57eaed`

The exact pin declares `mod_version=1.5.1`.

## Entrypoint registry families

`DungeonsDelight` registers:

| Registry surface | Provider owner |
|---|---|
| particles | Dungeon's Delight |
| blocks | Dungeon's Delight |
| items | Dungeon's Delight |
| mob effects | Dungeon's Delight |
| block entities | Dungeon's Delight |
| recipe serializers/types | Dungeon's Delight |
| menus | Dungeon's Delight |
| creative tabs | Dungeon's Delight |
| entities | Dungeon's Delight |
| sounds | Dungeon's Delight |
| enchantment data components | Dungeon's Delight |
| features | Dungeon's Delight |
| advancement criteria | Dungeon's Delight |
| optional integration items | Dungeon's Delight integrations |

No spell, ritual, rite or ability registry is registered by the provider entrypoint.

## Mob effects — exact 12

From `DDEffects.MOB_EFFECTS`:

- `feral_bite`
- `serrated`
- `putrid_scent`
- `ravenous_rush`
- `pouncing`
- `exudation`
- `swift_step`
- `rotgut`
- `decisive`
- `voracity`
- `tenacity`
- `burrow_gut`

All twelve are `MobEffect` registrations.

## Enchantments — exact 2

`DDEnchantments` defines and bootstraps:

- `ricochet`
- `serrated_strike`

Both are Minecraft enchantments over equipment, not standalone player magical actions.

## Recipe infrastructure

`DDRecipeRegistries` registers:

- recipe serializer `monster_cooking`;
- recipe serializer `monster_food_serving`;
- recipe type `monster_cooking`.

## Negative spell/action registry evidence

Exact-source search returns no hits for the spell-provider signatures used in Black Arcana's current Iron's/addon audits:

- `registerSpell`;
- `SpellRegistry`;
- `AbstractSpell`;
- provider ritual registrar;
- provider ability registrar.

The exact source tree also exposes no provider-owned spell/ritual resource namespace.

## Semantic disposition

Dungeon's Delight has supernatural/magic-themed mechanics, but the current Black Arcana semantic metric does not count:

- food consumption as a spell;
- mob-effect identities as player action identities;
- enchantments as spells;
- weapon/item interactions as spells;
- recipe types as rituals.

Therefore:

- independent spell identities: **0**;
- independent ritual/rite identities: **0**;
- independent equivalent discrete magic-action registry: **0**;
- strict semantic delta: **+0**.

## Runtime caveat

The current physical distribution is 1.5.1 while the sibling records internal installed metadata as 1.5.0. The exact source pin declares 1.5.1. This catalog closes source semantics and ownership, not installed binary equality or runtime metadata reconciliation.
