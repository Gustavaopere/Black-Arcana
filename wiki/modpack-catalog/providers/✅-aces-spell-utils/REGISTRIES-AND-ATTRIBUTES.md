# Ace's Spell Utils — registries and attributes

Source scope: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac` (`mod_version=1.2.7.2-1.21.1`).

## Standalone spell registry

The exact source revision contains no `registerSpell(...)` call and no provider spell-registry registration class. The spell-facing source includes helper/base/example classes such as `AbstractSummonSpell` and `ExampleSummonSpell`, but those are not registered as Ace's Spell Utils standalone spells.

**Provider standalone spell count: 0.**

Spell tags are contracts for spells supplied by consumers/other providers; they do not register spells themselves.

## SchoolType registrations — 3

| Registry ID | Source surface | Power/resistance attributes | Damage type | Catalog interpretation |
|---|---|---|---|---|
| `aces_spell_utils:ritual` | `RITUAL` | `ritual_spell_power`, `ritual_magic_resist` | `ritual_magic` | registry identity Ritual; current public display language uses Occult |
| `aces_spell_utils:hydro` | Java supplier named `ABYSSAL` | `hydro_spell_power`, `hydro_magic_resist` | `hydro_magic` | registry identity Hydro; do not infer an `abyssal` registry ID from the stale Java symbol/comment |
| `aces_spell_utils:technomancy` | `TECHNOMANCY` | `technomancy_spell_power`, `technomancy_magic_resist` | `technomancy_magic` | direct |

All three use Iron's `SchoolType` and `EVOCATION_CAST` as the source-observed cast sound.

## Attributes — 19 total

### General runtime attributes — 13

| ID | Type / default | Source bounds | Source runtime role |
|---|---|---:|---|
| `mana_steal` | MagicPercent / `0` | `-100 .. 10000` | gains mana from post-damage; optionally drains a player target's mana |
| `mana_rend` | MagicPercent / `0` | `-100 .. 100` | scales incoming damage according to target max mana above base |
| `goliath_slayer` | Percentage / `0` | `-100 .. 100` | bonus damage against `boss_like_entities` |
| `hunger_steal` | Ranged / `0` | `-100 .. 100` | full-charge melee hunger gain; player target hunger reduction path |
| `spell_res_penetration` | Percentage / `0` | `0 .. 1` | adjusts Iron's spell resistance calculation for spell damage |
| `evasive` | Ranged / `0` | `0 .. 100` | invulnerability-frame behavior; source also has direct `LivingEntity` mixin hooks |
| `magic_damage_crit_chance` | Percentage / `0.05` | `0 .. 10` | generic magic critical chance |
| `magic_damage_crit_damage` | Percentage / `1.5` | `1 .. 100` | generic magic critical multiplier basis |
| `magic_projectile_crit_chance` | Percentage / `0.05` | `0 .. 10` | `AbstractMagicProjectile` critical chance |
| `magic_projectile_crit_damage` | Percentage / `1.5` | `1 .. 100` | projectile critical multiplier basis |
| `magic_projectile_damage` | Percentage / `0` | `0 .. 1` | bonus damage for Iron's magic projectiles |
| `life_recovery` | Percentage / `0` | `0 .. 1` | heals a percentage of attacker's max health after damage |
| `vigor_reap` | Percentage / `0` | `0 .. 1` | heals a percentage of attacker's missing health after qualifying hit |

The exact source adds every registered Ace's Spell Utils attribute to every entity type through `EntityAttributeModificationEvent`. That is a provider-global attribute surface; Black Arcana must not create a shadow copy of these values.

### School power/resistance attributes — 6

- `ritual_magic_resist` — MagicPercent, default `1`, source bounds `-100 .. 100`
- `ritual_spell_power` — MagicPercent, default `1`, source bounds `-100 .. 100`
- `hydro_magic_resist` — same type/default/bounds
- `hydro_spell_power` — same type/default/bounds
- `technomancy_magic_resist` — same type/default/bounds
- `technomancy_spell_power` — same type/default/bounds

## Damage-type keys — 3

- `aces_spell_utils:ritual_magic`
- `aces_spell_utils:hydro_magic`
- `aces_spell_utils:technomancy_magic`

These are provider/Iron's school damage identities. Their existence does not create Black Arcana Corruption, Strain or Arcane Danger events by itself.

## Attachment types — 1

`aces_spell_utils:keep_inv_on_death`:

- Boolean;
- default `false`;
- serialized with `Codec.BOOL`;
- `copyOnDeath()` enabled.

Provider server events and `PlayerMixin` use this attachment for inventory/experience/curio retention behavior around qualifying `IKeepInventoryEntity` entities.

## Particle types — 1

`aces_spell_utils:trail` uses `TrailParticleOptions` codec + stream codec and has a client provider registration.

## Tag contracts — 14

### Item tags — 9

Focus:

- `aces_spell_utils:ritual_focus`
- `aces_spell_utils:hydro_focus`
- `aces_spell_utils:technomancy_focus`

Rune unification:

- `aces_spell_utils:ritual_runes`
- `aces_spell_utils:hydro_runes`
- `aces_spell_utils:technomancy_runes`

Upgrade-orb unification:

- `aces_spell_utils:ritual_upgrade_orbs`
- `aces_spell_utils:hydro_upgrade_orbs`
- `aces_spell_utils:technomancy_upgrade_orbs`

### Entity tags — 3

- `aces_spell_utils:boss_like_entities`
- `aces_spell_utils:mana_steal_whitelist`
- `aces_spell_utils:mana_rend_whitelist`

### Spell tags — 2

- `aces_spell_utils:stomp_like_spell`
- `aces_spell_utils:slash_like_spell`

These are Iron's spell-registry `TagKey<AbstractSpell>` contracts. They are not registered Ace's Spell Utils spells.

## Extended rarities — 8

NeoForge enum extensions add:

- `aces_spell_utils:glacial`
- `aces_spell_utils:aquatic`
- `aces_spell_utils:verdant`
- `aces_spell_utils:cosmic`
- `aces_spell_utils:forbidden`
- `aces_spell_utils:arid`
- `aces_spell_utils:accursed`
- `aces_spell_utils:sculk`

The presence of a rarity named `forbidden` is presentation/item metadata only. It must not be interpreted as Black Arcana forbidden-magic identity, Corruption or Arcane Danger.

## Deduplication consequence

This registry surface occupies shared cross-addon school/attribute/tag/runtime space. A Black Arcana adapter may observe a proven provider state when a real contract requires it, but must not register duplicate Ace's schools, mirror the 19 attributes into a second ledger, reapply provider damage modifiers, or reinterpret provider tags as Black Arcana authorities.
