# Cooldown, network and config — Apothic Attributes 2.10.1

## AbilityCooldowns

`AbilityCooldowns` is the provider's public cooldown entry point. Its source contract states cooldown state is server-side only and queries must run on the logical server.

Public operations:

- `isOnCooldown(entity, id, baseCooldown)`
- `startCooldown(entity, id)`
- `getRemaining(entity, id, baseCooldown)`
- `applyCDR(entity, baseCooldown)`
- `clear(entity, id)`

State lives in the serialized/synchronized/copy-on-death `cooldowns` attachment.

`applyCDR` computes `baseCooldown * (1 - cooldown_reduction)`, rounds to ticks and keeps a positive cooldown at a minimum of one tick. The `cooldown_reduction` attribute is capped at 0.95 on its positive side in the central attribute registration.

### Black Arcana boundary

Black Arcana has its own server-owned cooldown/charge subsystem and persistence semantics. `apothic_attributes:cooldown_reduction` affects the provider's `AbilityCooldowns` contract; it must not be applied to BA cooldown groups without a separately verified and approved integration contract.

## Network surface — 2 clientbound payloads

### `apothic_attributes:config`

- PLAY protocol;
- CLIENTBOUND;
- protocol/provider version string `1`;
- payload field: `knowledgeMultiplier` float;
- client handler updates the synchronized provider config value.

### `apothic_attributes:crit_particle`

- PLAY protocol;
- CLIENTBOUND;
- protocol/provider version string `1`;
- payload field: target entity id;
- client handler renders the provider critical-hit presentation.

No provider C2S cast-intent payload was observed. These packets are not Black Arcana cast confirmation or authority signals.

## Config surface

Provider config is stored under the Apotheosis config directory as `apothic_attributes.cfg` and reloads through a resource-manager listener.

Observed settings include:

- Enable Attributes GUI — client-authoritative;
- Enable Potion Tooltips — client-authoritative;
- Ancient Knowledge Multiplier — default 4.0, range 1..1024, synchronized;
- Hidden Attributes — client-authoritative list with namespace wildcards and `!` negation support;
- GUI Button Offset;
- Protection Formula — configurable expression;
- A-Value Formula — configurable expression;
- Armor Formula — configurable expression;
- Armor Toughness Formula — configurable expression;
- Negative Armor Factor — default 0.015, range 0..1.

The provider validates custom formula expressions and falls back when invalid/default. These formula/config surfaces remain Apothic authority; BA must not mirror or silently override them.
