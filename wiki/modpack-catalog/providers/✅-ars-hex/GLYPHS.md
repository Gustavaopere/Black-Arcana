# Ars Hex 5.0.4b — Glyphs

Status: `SOURCE-PINNED / PRODUCTION REGISTRY 1/1 CLOSED / INSTALLED RUNTIME QA OPEN`

## Production registration

`ArsNouveauRegistry.registerCompatGlyphs()` registers exactly one Ars spell part when `malum` is loaded:

`ars_hex:glyph_soul_shatter` — **Soul Shatter**

Malum is present in the physical pack, so this registration path is eligible in the installed runtime. Physical runtime confirmation remains deferred.

## Soul Shatter

| Property | Exact source behavior |
|---|---|
| Type | `AbstractEffect`, `IDamageEffect` |
| Tier | II |
| Default mana | 30 |
| Source-default damage | 5.0 |
| Amplify value | +3.0 per Ars amp multiplier unit |
| Explicit Amplify limit | 2 |
| Compatible augments | Amplify, Dampen |
| Damage authority | Ars damage helper using Malum `VOODOO` damage type |
| Ars school with Ars Elemental loaded | Necromancy |
| Target exclusion | does not resolve damage on `ItemEntity` |

Executable damage before Ars/provider downstream handling is computed as:

`damage = DAMAGE + AMP_VALUE * spellStats.getAmpMultiplier()`

The effect then delegates damage through Ars `attemptDamage(...)` with a Malum Voodoo `DamageSource`. It does not implement a second Black Arcana-style damage transaction.

## School behavior

When `ars_elemental` is loaded, `getSchools()` returns exactly Ars `SpellSchools.NECROMANCY`. The current physical pack contains Ars Elemental 0.7.10.1, so Necromancy is the relevant source path for installed QA.

If Ars Elemental is absent, Soul Shatter delegates to its inherited/default school behavior; Phase 2W does not invent a replacement school.

## Learning recipe

The generated source recipe is Malum-conditioned:

- type: `ars_nouveau:glyph`;
- XP: 55;
- inputs:
  - `ars_nouveau:manipulation_essence`;
  - `malum:wicked_spirit`;
  - `malum:soul_stained_steel_sword`;
- output: `ars_hex:glyph_soul_shatter`.

See [`ACQUISITION.md`](ACQUISITION.md).

## Spirit-release wording boundary

The source book description says Soul Shatter damages the enemy soul “with the chance of releasing the spirits inside.” The audited `EffectSoulShatter` class itself contains no explicit spirit-release RNG/formula; it only performs the Voodoo damage call.

Therefore Phase 2W records:

- the player-facing claim exists;
- the exact spirit-release causal formula is **not established by this class**;
- no numeric spirit-drop chance/reward is inferred;
- installed Malum/Ars event behavior must be observed before describing exact spirit settlement.

## Black Arcana consequence

A simple Malum-backed soul-damage spell and its provider-native spirit consequences already occupy part of the soul-damage design space. That does **not** eliminate Black Arcana's Souls & Death domain: BA mechanics remain valid when their identity is genuinely different — e.g. BA-owned Mortal Ledger/Soul Anchor/Arcane Danger contracts — and they must not replay Soul Shatter or Malum spirit settlement.
