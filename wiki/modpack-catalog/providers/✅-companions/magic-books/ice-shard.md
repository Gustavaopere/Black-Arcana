# Ice Shard Magic Book

- Provider: **Companions!** (`companions`)
- Version: `1.3.4`
- Registry id: `companions:book_ice_shard`
- Concrete class: `IceShardBook`
- Semantic type: **provider-owned Magic Book action**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`
- Source-default cooldown: **180 ticks**
- Source-level survival acquisition: **Overworld Minion + Copper Coin random reward**

## Action surface

launches the provider ice-shard projectile from the caster; the projectile receives the caster's recent combat target hint when available.

## Registration closure

The exact 1.3.4 source pin registers this item directly in `CompanionsItems` as a concrete `AbstractMagicBook` subclass. No mod-presence/config branch around the nine Magic Book registrations was found.

## Acquisition boundary

The route above is closed at source/catalog level. Effective assembled-pack loot, recipe/datapack mutation, probabilities and deployed config remain runtime QA.

## Soul Mage deduplication

Soul Mage can consume/equip the same Magic Book identity. Its AI goal reuses this action and does not mint a second semantic object.

## Authority boundary

Companions! remains authority for activation, cooldown/config settlement and any projectile/effect/state created by this action. Black Arcana must not replay the provider's damage, healing, summon/projectile or cooldown settlement.

## Evidence boundary

The source-default cooldown and action description are factual metadata from the pinned provider inventory, not deployed-pack measurements. Runtime attribution, protection behavior, multiplayer behavior and lifecycle remain separate QA.

Source: `../SOURCE-1.3.4-MAGIC-BOOK-INVENTORY.md`.
