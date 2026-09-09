# Monsters & Spellbooks — runtime and safety boundaries

## Casting authority

The provider registers `AbstractSpell` implementations into Iron's spell registry. That makes Iron's the host casting framework for normal cast admission, spell data, mana/cooldown settlement and spell lifecycle.

Black Arcana must not invoke a Monsters & Spellbooks effect by bypassing Iron's cast settlement and then separately debit mana/cooldown. A bridge may only enter through a verified provider/host route that preserves exactly-once execution.

## Summons, forms and persistent effects

The 98-registration inventory includes source identities whose classes clearly represent summons, forms, fields, mines, projectiles and terrain-oriented effects. Their names are enough to identify them as QA/deduplication candidates, but **not** enough to prove exact mechanics, ranges, ownership rules, persistence or cleanup in the installed binary.

Therefore:

- provider-created summons remain provider-owned entities/lifecycles;
- provider-created forms/status effects remain provider-owned state;
- Black Arcana must not duplicate a provider summon or reapply a provider form as a second independent effect;
- exact entity caps, durations, damage formulas, targeting and cleanup remain `NÃO VERIFICADO` where no exact 0.0.16.3 class evidence is pinned.

## World-effect boundary

Names such as `TUNDRA_TERRAIN`, `REDSTONE_MINES`, `GRAVEYARD_FISSURE`, `SPACE_RUPTURE` and summon/field identities flag possible world or area interaction, but the catalog does not infer mutation semantics from names alone.

If Black Arcana casts or delegates to a provider-native spell, provider-native mutation must not be replayed through a second Black Arcana effect path.

If Black Arcana itself performs a destructive mutation inspired by a capability, the mutation still requires canonical `WorldEffectPolicy`, protection, loaded-chunk and budget admission. Provider presence does not waive Black Arcana's world-safety contracts.

## Resource and cooldown boundary

Exact 0.0.16.3 mana values, cooldown groups/values and level scaling are not promoted from the stale-version public source metadata.

No Black Arcana integration may:

- create a second mana pool for these spells;
- debit Iron's mana twice;
- mirror provider cooldowns into an independently authoritative Black Arcana cooldown for the same cast;
- accept client-authored damage/cost/range values;
- treat a tooltip/display name as an API contract.

## Necro and Black Arcana state are distinct

The provider's Necro school, effects and equipment do **not** automatically cause or consume:

- Black Arcana Corruption;
- Black Arcana Arcane Strain;
- Arcane Danger;
- Souls & Death ledgers;
- sibling RPG Skill Tree Mastery.

Any relationship requires an explicit causal adapter with a real server-safe hook. Without one, the integration is fail-closed.

## Deduplication rule

The 98 registrations are provider spell identities, not 98 automatically distinct Black Arcana gaps. Phase 3 may only consume them after semantic comparison against the rest of the provider catalog. Similar names such as teleport, summon, field, drain, slash, nova, aspect or intervention do not establish equivalence by themselves.
