# Ars Elemental 0.7.10.1 — mixin boundaries

Status: `16/16 MIXINS CLASSIFIED / INSTALLED-JAR CONFLICT QA PENDING`

Mixin config declares 14 common mixins and 2 client mixins.

## Common gameplay mixins

- `ChillingPerkMixin`: augments Ars Chilling Perk tier 3; a valid damaging effect against a fully frozen target applies provider Frozen for 20 ticks and cancels the original perk callback path.
- `KindlingPerkMixin`: augments Ars Ignite Perk tier 3; valid damaging effects apply provider Magic Fire for 20 ticks.
- `CutMixin`: wraps core Ars Cut damage. When provider Air-focus check succeeds, replaces the damage source with `ars_elemental:beheading` using Ars fake-player attribution.
- `EvaporateMixin`: extends core Ars Evaporate; Mud is converted to Clay when Ars `destroyRespectsClaim` permits it, then the original path is cancelled for that block.
- `FlareMixin`: extends core Ars Flare eligibility so a LivingEntity with provider Magic Fire can be damaged by the Flare path.
- `GrowMixin`: makes core Ars Grow expose `IDamageEffect` eligibility for non-allied undead targets when provider Earth-focus check succeeds.
- `LightningMixin`: prevents Ars `LightningEntity` from calling `thunderHit` on ItemEntity and ExperienceOrb; other entities keep the original call.
- `LivingEntityMixin`: changes travel friction while provider `ICE_SLIDE` is active, adding up to 0.38 over base friction and clamping to 1.075.
- `ItemEntityMixin`: protects an item carrying provider `P4E` flag from non-bypass damage by redirecting the ItemEntity invulnerability check.
- `RitualAwakeningMixin`: extends Ars Ritual of Awakening search to Flashing Archwood; a >=50-block matching structure inside the local search can select provider Flashing Weald Walker and destroy the found tree through the Ars ritual path.
- `ServerLevelMixin`: when `always_thunder` is enabled, adds provider non-visual-only FlashLightning attempts during server chunk ticks in the provider flashing-biome tag while raining.
- `DynamicLightMixin`: extends Ars dynamic-light lookup so LivingEntity with Magic Fire returns light level 15.

## Accessor/invoker mixins

- `FoxInvoker`: access bridge used by Charm's fox trust path; it is not an independent gameplay system.
- `ZombieInvoker`: access bridge used by Watery Grave's Zombie-to-Drowned conversion trigger; it is not an independent gameplay system.

## Client mixins

- `EntityRenderDispatcherMixin`: renders the provider Magic Fire world overlay/effect on living entities that carry the effect.
- `SpellBookTextureMixin`: when the client netherite-texture option is enabled and the provider `P4E` data component flag is set, selects an alternate Ars Nouveau spellbook texture by base color.

Client mixins and dynamic-light presentation are not gameplay authority.

## Black Arcana boundary

These hooks change Ars/vanilla provider behavior directly. Integration must observe the final provider result rather than applying parallel transformations. In particular, do not duplicate Fire/Frozen procs, Cut damage-type substitution, Mud conversion, lightning, item protection or Ritual of Awakening behavior.