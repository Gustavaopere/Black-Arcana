# Ars Morph 2.0.0 — Morph glyph

Status: `1/1 SOURCE REGISTRATION CLOSED / INSTALLED RUNTIME QA OPEN`

## Registry identity

`ArsNouveauRegistry.registerGlyphs()` registers exactly one production spell part:

- registry id: `ars_morph:glyph_morph`;
- display name: Morph;
- implementation: `EffectMorph`.

Source defaults:

| Field | Exact source value |
|---|---|
| Tier | II |
| Mana | 200 |
| School | Conjuration |
| Compatible augments | none |
| Config key | `max_hp_morph` |
| Config default | 100 |
| Config range | 20 .. `Integer.MAX_VALUE` |

The health check is `candidateMorph.getMaxHealth() < max_hp_morph`. Equality does not pass.

## Server-authoritative resolution path

`onResolveEntity` mutates identity only when all of the following are true:

- level is `ServerLevel`;
- shooter is `ServerPlayer`;
- Ars `isRealPlayer(shooter)` passes;
- struck target is a `LivingEntity`.

`FamiliarEntity` is explicitly rejected.

No client path owns the morph mutation.

## Target/form-selection precedence

The exact source chooses the candidate type in this order:

1. If the caster's offhand item is an Ars `MobJarItem` and `MobJarItem.fromItem(...)` produces a `LivingEntity`, use the contained entity's type.
2. Otherwise start from the struck living entity's type.
3. If the selected type is still the struck living entity's type and the offhand item is a `SpawnEggItem`, replace it with the spawn egg's type.

This means a valid Mob Jar wins over a Spawn Egg.

## Recipient semantics

- If the struck living entity is a `ServerPlayer`, that target player is the recipient of a non-player morph.
- Otherwise the caster is the recipient.
- If the struck living entity is a player and the selected type is `EntityType.PLAYER`, the provider calls `IdentityProgression.clearMorph(targetPlayer)`.

This is not a self-only glyph.

## Morph transaction

For a non-clear operation:

1. create a new entity instance from the selected `EntityType` in the server world;
2. abort if creation returns null;
3. require candidate max health strictly below the glyph config threshold;
4. if candidate and struck living entity both implement Ars `IDecoratable`, copy the struck entity's cosmetic item to the candidate;
5. call Identity2:
   `IdentityProgression.morph(recipient, entityTypeId, candidate.serializeNBT(candidate.registryAccess()))`;
6. emit smoke particles only if Identity2 reports success.

Identity2 therefore remains the authority over accepting/persisting the morph. Ars Morph supplies the requested type/NBT and bridge logic.

## Deduplication boundary

Black Arcana/RPG integrations must not:

- perform a second Identity2 morph call around the same glyph resolution;
- debit or refund Ars mana independently of the Ars cast pipeline;
- duplicate the max-health gate as an independent post-cast authority;
- serialize a competing variant/state record;
- treat smoke particles as confirmation if the Identity2 operation itself failed;
- bypass Identity2 acquisition/state semantics with a second morph ledger.

## Runtime QA cases

- entity target, no offhand selector;
- valid Mob Jar selector;
- Spawn Egg selector;
- valid Mob Jar + Spawn Egg precedence impossible in one offhand stack but selection logic must remain as source-defined;
- target player morph;
- target player clear-to-player;
- FamiliarEntity rejection;
- threshold `max-1`, `max`, `max+1` health;
- null/invalid candidate creation where reproducible;
- cosmetic copy for Ars decoratable entities;
- Identity2 rejection path produces no success smoke;
- multiplayer permission/friendly-target behavior under current Identity2/provider configuration.
