# Apprentice's Codex — effects and attribute registry catalog

## Status

`SOURCE-PINNED 0.9.7.1 / 20 STATIC EFFECT IDS FROZEN / 25 SCHOOL-AFFINITY EFFECT SLOTS AUDITED / 1 PROVIDER ATTRIBUTE ID FROZEN / INDIVIDUAL EFFECT RUNTIME QA PARTIAL`

Source pin: `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`.

This page covers provider effects/attribute identity not already owned by the exact item and block catalogs.

## Static mob effects — 20

The exact `EffectRegistry` registers these static effect IDs under namespace `apprenticecodex:`:

- `arcane_charge`
- `casting_mobility`
- `craftsmans_delight_mobility`
- `divine_possession`
- `intelligence`
- `long_stride_mobility`
- `mana_regeneration`
- `mist_form`
- `palette_reception`
- `echo_spell`
- `phalanx_stance`
- `sense_sensor`
- `spectral_wing`
- `thermal_processing`
- `penetrated_armor`
- `frost_trapped`
- `notched_frozen`
- `gravity_bound`
- `inert_mana_shield`
- `blood_engraved`

Registry identity does not imply identical lifecycle semantics. The relevant spell/item page remains authoritative when one of these effects is a downstream state of a specific provider cast or item.

Examples already source-audited in the spell catalog include Arcane Charge, Long Stride mobility, Mirage/other mobility state, Blood Engraved interactions and provider mana-regeneration paths. A future integration that needs an effect's exact stacking, immunity, tick logic or attribute modifiers must inspect that exact 0.9.7.1 effect class before implementation.

## School Affinity dynamic effects — 25 registered slots

School Affinity pre-registers **25 slot-backed dynamic effect identities**:

- 9 fixed slots assigned to Iron's builtin schools;
- up to 16 additional eligible loaded schools.

The exact assignment, temporary school-power modifier and potion variants are audited separately in [`SCHOOL-AFFINITY.md`](SCHOOL-AFFINITY.md).

These 25 effects are not additional spell schools and are not RPG Skill Tree Masteries.

## Provider attribute — 1

The exact attribute registry adds one synced ranged attribute:

`apprenticecodex:max_enchantment_table_level`

Exact source range:

- default: `0.0`;
- minimum: `0.0`;
- maximum: `2048.0`;
- client synchronization enabled.

This attribute belongs to Apprentice's Codex. Similar RPG progression concepts must not create a second attribute with the expectation that the provider will read it automatically.

## Boundary rules

1. Iron's remains authority for its own school spell-power and standard magic attributes.
2. Apprentice's Codex owns the effect identities above and its `max_enchantment_table_level` attribute.
3. Black Arcana must not convert these effects into Corruption, Strain, Arcane Resistance, Corruption Resistance or Backlash state without an explicit bridge.
4. RPG Skill Tree must not treat effect presence/ticks as Mastery generation absent a real causal event contract.
5. An observed provider modifier must not be re-applied by an integration.
6. Dynamic School Affinity assignment remains provider-owned and capped by the exact slot model.

## Related exact catalogs

- [`ITEM-CATALOG.md`](ITEM-CATALOG.md) — 167/167 item registry IDs;
- [`BLOCK-CATALOG.md`](BLOCK-CATALOG.md) — 20/20 block registry IDs;
- [`SCHOOL-AFFINITY.md`](SCHOOL-AFFINITY.md) — dynamic affinity slot/effect semantics.

## Confidence

`SOURCE-PINNED REGISTRY IDENTITY / STATIC EFFECT COUNT EXACT / AFFINITY SLOT COUNT EXACT / ATTRIBUTE ID+RANGE EXACT / INDIVIDUAL EFFECT BEHAVIOR AUDIT ONLY WHERE A REAL BRIDGE REQUIRES IT`