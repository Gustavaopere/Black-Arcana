# Capability Matrix Delta — Ars Morph 2.0.0

Status: `SOURCE-PINNED PROVIDER DELTA / RUNTIME QA PENDING`

| Capability | Current Ars Morph coverage | Black Arcana consequence |
|---|---|---|
| Spell-driven morph | Ars Tier-II Morph glyph requests Identity2 morph/clear state from struck entity, Mob Jar or Spawn Egg | generic magical shapeshift into a selected mob is already occupied; BA needs a materially distinct forbidden-magic mechanic to justify overlap |
| Max-health morph gate | glyph config gates candidate form by strict max-health threshold | do not add a second post-resolution authority/gate around the same provider morph |
| Player-target transformation | hitting another player can make that player the morph recipient | multiplayer targeting/consent/safety must be provider-validated before any BA observer reacts |
| Ars Mob Jar → morph | contained entity type has first selection priority | generic 'jar creature becomes form' is occupied |
| Spawn Egg → morph | offhand spawn egg can replace struck type when no Mob Jar-selected type changed the choice | generic spawn-egg form selection is occupied |
| Ars cosmetic carryover | `IDecoratable` cosmetic item is copied into candidate morph NBT | do not create a parallel BA cosmetic serializer |
| Ars creature active abilities | 6 Ars adapters plus optional Firenando reuse Ars spell/effect/entity behavior | ability child casts/effects are provider descendants, not independent BA proc opportunities |
| Identity cooldown/use duration | 11 committed ability assignments carry Identity2 cadence data | RPG/BA must not own a duplicate cooldown ledger for these abilities |
| Morph passive abilities | Whirlisprig passive jump + Identity2 capability tags cover flight/breathing/swim/fire/lava/slow-fall traits | do not mirror these passives into a second attribute/effect system without a distinct mechanic |
| Ars entity variants | 5 Ars + 3 optional Elemental variant adapters preserve colors/tamed/host variants | do not store a competing form-variant record |
| Wilden Stalker flight representation | morph tick handler derives server flight representation and syncs through Identity2 | no BA `isFlying` mirror/network packet |

## Semantic disposition

Ars Morph materially occupies **generic Ars-powered shapeshifting and Ars-creature Identity2 integration**. A darker name, corruption VFX or alternative particles do not create a Black Arcana gap.

A future BA transformation remains viable only when its causal identity is genuinely different — for example a BA-owned forbidden transformation with Corruption/Strain/hazard/world-safety consequences that does not pretend to be, duplicate or overwrite the Identity2 form state. Any coexistence bridge must decide explicitly whether Identity2 remains the body/form authority or whether the BA mechanic is an independent temporary effect with non-overlapping state.

## Authority/dedup rules

- Identity2 form/variant/ability state settles once.
- Ars mana/cast/resolver settles once.
- Ars Morph child projectiles/effects produced by an Identity ability remain descendants of that one provider action.
- RPG Skill Tree may gate/progress through a real contract but does not become morph runtime authority.
- Black Arcana observes provider results only through a real boundary; observation must not replay morph, ability, projectile, potion, cooldown or variant settlement.
