# Ace's Spell Utils — API and runtime surfaces

Source scope: exact public version pin `a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`.

## Reusable API families

Ace's Spell Utils exposes reusable building blocks rather than a second standalone spell catalog. Current source includes, among other provider-facing families:

### Spellcasting/boss entities

- `UniqueAbstractSpellCastingMob`
- `UniqueAbstractMeleeCastingMob`
- `GenericBossEntity`
- `GenericUniqueBossEntity`
- `WizardSpellComboGoal`
- phase/music interfaces including `IPhaseEntity` and `IPhaseMusicEntity`
- `IKeepInventoryEntity`

These are helper/base contracts. A consuming addon owns concrete mobs and their spell semantics.

### Spell/domain helpers

- `AbstractSummonSpell`
- `ExampleSummonSpell`
- `AbstractDomainEntity`
- custom casting-animation helpers

`AbstractDomainEntity` is a third-party domain helper, not Black Arcana's canonical domain runtime. Source-observed behavior includes synchronized radius/refinement/open/transported/clash state, local AABB scans, refinement-based clash resolution, owner lifecycle, optional transport/sure-hit callbacks, NBT state and a forced chunk region ticket on activation.

Its `handleDomainClash`, `handleSureHit` and transportation behavior are extension points for consuming addons. Black Arcana must not use this helper to create a parallel magic runtime or bypass `WorldEffectPolicy`.

### Item helper families

Current source exposes reusable curio/staff/weapon/mace patterns including:

- imbueable/preset imbue curios;
- sheath curio;
- flat-cooldown passive ability curio;
- passive ability spellbook / unique spellbook helpers;
- imbueable/preset imbue staves;
- active+passive ability sword and magic-sword helpers;
- magic gun casting helper;
- extended/imbueable/preset-imbue mace and mace-staff families introduced/expanded in the 1.2.7.2 release line;
- custom loot-bag and rendering/VFX support classes.

These classes make it easier for other Iron's addons to own concrete items. They do not transfer the consuming addon's item/casting authority to Ace's Spell Utils or to Black Arcana.

## Source-owned event runtime

`AcesSpellUtilsServerEvents` implements shared behavior for the provider attributes and utilities.

### Cast initiation helper

`MagicGunItem` right-click handling resolves Iron's `SpellSelectionManager` selection and calls the selected spell's `attemptInitiateCast(...)`. Iron's spell/mana/cooldown/learning checks remain the underlying cast authority.

Black Arcana must not intercept this path and initiate the same selected spell a second time.

### Attribute event families

The exact source contains provider handlers for:

1. Mana Steal — post-damage mana gain; optional player-target mana drain; bounded by attacker's max mana.
2. Mana Rend — incoming damage scaling based on target max mana above base.
3. Goliath Slayer — damage bonus against `boss_like_entities`.
4. Hunger Steal — full-charge melee hunger transfer/gain path.
5. Spell Resistance Penetration — adjusts Iron's spell-damage resistance math.
6. Evasive — provider invulnerability-frame handling; see mixin note below.
7. Magic Damage Critical Chance/Damage — generic spell-damage crit path at lowest event priority.
8. Magic Projectile Critical Chance/Damage — `AbstractMagicProjectile` crit path at lowest priority.
9. Magic Projectile Bonus Damage — low-priority projectile damage multiplier.
10. Life Recovery — post-damage healing based on attacker's max health.
11. Vigor Reap — post-damage healing based on attacker's missing health.

These are shared provider runtime semantics, not Black Arcana perk implementations. RPG Skill Tree must not mirror or recalculate them unless a real integration contract explicitly delegates a gate/modifier without taking ownership of the event pipeline.

## Keep-inventory helper runtime

Source behavior combines `IKeepInventoryEntity`, the `keep_inv_on_death` attachment, server events and `PlayerMixin` to preserve qualifying player inventory/experience/curios around death.

Observed event surfaces include:

- XP-drop cancellation;
- Curios drop-rule override;
- clone-time inventory/experience copy and attachment cleanup;
- death-time proximity check for `IKeepInventoryEntity`;
- `Player.dropEquipment` cancellation through mixin while attachment state is active.

Black Arcana must not create a second death-copy/drop-cancellation pipeline for the same provider condition.

## VFX runtime maintenance

Server tick/stopping/tracking handlers maintain trail/ribbon state and resend tracking state as needed. The associated custom network payloads are client-bound visual transport, not a client-authoritative spell/cast channel.

## Config surface — 5

Common config exposes:

- `Mana Steal drains mana` — default `true`;
- `Refinement victory factor` — default `1.5`;
- `Enable Dev mode` — default `false`;
- `Mana Rend entity blacklist` source field/variable is used as whitelist enable switch — default `true`;
- `Mana Steal entity blacklist` source field/variable is used as whitelist enable switch — default `true`.

The source comments/keys use mixed whitelist/blacklist terminology. Catalog semantics follow actual tag/field use and preserve the naming mismatch rather than silently rewriting the provider contract.

## Event-ordering risk

The exact source contains both an `evasiveEvent(...)` listener and `LivingEntityMixin` injections that modify invulnerability behavior. This is provider-owned internal behavior. Black Arcana must neither normalize it into a guessed single formula nor add another iframe layer on provider-caused events.

Likewise, crit, recovery, mana and projectile modifiers run on NeoForge/Iron's event surfaces with explicit priorities in places. Future adapters must preserve causal owner and avoid double-processing.

## Authority boundary

Ace's Spell Utils owns its shared utility runtime. Iron's owns spell casting/mana/cooldown substrate. Concrete consuming addons own their spells/entities/items built on the API. Black Arcana owns only Black Arcana runtime and may integrate through verified boundaries without cloning any of these pipelines.
