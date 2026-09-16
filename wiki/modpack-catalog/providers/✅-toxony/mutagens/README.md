# Toxony 0.10.7 — Mutagens, Affinities and thresholds

## Status

`7/7 MUTAGEN EFFECT IDS / 11/11 AFFINITIES / PLAYER THRESHOLD MODEL AUDITED / 6 PLAYER AFFINITY CANDIDATES + 1 MOB PATH / IRON'S MODIFIERS SOURCE-OBSERVED / LICENSE+RUNTIME QA PENDING`

Exact source checkpoint: `MrFrostyDev/Toxony_Mod@881bf7fe632659e748c279966a2bf49b99f7503f`.

## Mutagen registry — 7/7

| ID | Acquisition role |
|---|---|
| `toxony:beast_mutagen` | player Affinity-selected candidate |
| `toxony:spirit_mutagen` | player Affinity-selected candidate |
| `toxony:aqua_mutagen` | player Affinity-selected candidate |
| `toxony:hollow_mutagen` | player Affinity-selected candidate |
| `toxony:necrotic_mutagen` | player Affinity-selected candidate |
| `toxony:infernal_mutagen` | player Affinity-selected candidate |
| `toxony:mob_mutagen` | separate mob-toxicity transformation path; not mapped by player Affinities |

## Player threshold model

Source constants:

- Tolerance min `10`;
- Tolerance default `30`;
- Tolerance max `999`;
- maximum stored Mutagen entries `3`;
- threshold multiplier `100`;
- initial threshold goal `100`.

The provider's goal formula is:

`((threshold + 1) * (threshold + 2) / 2) * 100`

The source advances only while `tox > thresholdGoal`, therefore the three reachable promotion boundaries under max Tolerance 999 are:

1. `tox > 100`;
2. `tox > 300`;
3. `tox > 600`.

If several thresholds are crossed by one Toxicity change, provider selection runs once per threshold delta before clearing Affinities.

## Affinity registry — 11/11

| ID | Index | Candidate Mutagens |
|---|---:|---|
| `toxony:moon` | 1 | Beast, Spirit, Hollow |
| `toxony:sun` | 2 | Beast, Infernal |
| `toxony:ocean` | 3 | Aqua |
| `toxony:forest` | 4 | Beast |
| `toxony:wind` | 5 | Aqua |
| `toxony:cold` | 6 | Hollow, Necrotic |
| `toxony:soul` | 7 | Spirit, Necrotic |
| `toxony:decay` | 8 | Necrotic |
| `toxony:nether` | 9 | Infernal |
| `toxony:end` | 10 | none |
| `toxony:heat` | 11 | Infernal |

Selection adds each Affinity's accumulated integer weight to every mapped candidate and chooses the greatest total. If no candidate is produced, the source falls back to Beast Mutagen. The Affinity map is cleared after the threshold-change selection pass.

### Equal-score blocker

The located selector stores candidate scores in a `HashMap` and updates the winner only when a later score is strictly greater. Equal scores have no explicit stable tie-break contract. Do not build Black Arcana progression logic that depends on a particular tie result until provider runtime/API behavior is verified.

## Duplicate Mutagen semantics

The provider stores up to three entries. A fourth removes the oldest. Duplicate entries are permitted; rebuilding active Mutagen effects reapplies duplicates as increased MobEffect amplifier.

Accordingly, this catalog uses:

- stage 0 = amplifier 0;
- stage 1 = amplifier 1;
- stage 2 = amplifier 2.

These stages belong to Toxony and are not RPG Skill Tree mastery tiers.

## Beast Mutagen

Source-observed behavior:

- stage 0: successful attacks can grant Speed for 40 ticks;
- stage 1: `+15%` attack damage; if Iron's Nature Spell Power attribute exists, `+20%` Nature Spell Power;
- stage 2: at night, `+30%` movement speed while the provider night-predator state is active; attacks apply `toxony:hunt` for 100 ticks;
- stage 1+ food handling distinguishes cooked versus raw meat/fish in the executable path rather than providing a uniform meat bonus.

The food path deserves runtime QA because its source operations do not reduce cleanly to the older generic catalog wording.

## Aqua Mutagen

- stage 0: Oxygen Bonus `+2` additive;
- stage 1: Submerged Mining Speed `+4.0` multiplied-total, NeoForge Swim Speed `+0.4` multiplied-total, and `+20%` Iron's Ice Spell Power when present;
- stage 2: additional Oxygen Bonus `+2.0` multiplied-total, maintains short Regeneration while in water/rain/bubble, fire-tag damage `×1.3`, and provider water-splash state can multiply a qualifying knockback strength by `3` with a 40-tick cooldown.

## Spirit Mutagen

- stage 0: Fall Damage Multiplier `-0.5`; damage from provider spirit-resistant entity types is also halved;
- stage 1: `+20%` Iron's Evocation Spell Power when present; 20% chance to null eligible incoming damage and grant Invisibility for 200 ticks; provider Guided Spirit attack support with a 400-tick readiness cooldown;
- stage 2: maintains Slow Falling, takes `×1.3` damage from the source's magic-family tag check, and a ready offensive trigger summons three Guided Spirits instead of one.

Guided Spirits are Toxony-owned summons. Their damage must not be double-processed as a second Black Arcana cast.

## Hollow Mutagen

- all stages: Movement Efficiency `+1.5` multiplied-total and Knockback Resistance `+0.2` additive;
- stage 1+: incoming damage `×0.85`;
- stage 2: additional `+0.3` Knockback Resistance, wall-climb behavior, maintained Night Vision and Weakness under direct daylight/sky conditions.

## Necrotic Mutagen

- stage 0: raw meat/raw fish/rotten flesh can heal 4 health; Hunger is rejected;
- stage 1: `+20%` Iron's Blood Spell Power when present; Poison and Wither effects rejected; Regeneration rejected; attackers can receive Poison; direct Wither damage is nulled;
- stage 2: attacks apply Wither for 100 ticks, direct daylight can maintain Weakness, and the provider resurrection gate can restore a dead/dying entity to half maximum health.

### Correct 0.10.7 resurrection cooldown

Executable source constant:

`DEFAULT_RESURRECTION_COOLDOWN = 200`

At 20 ticks/s this is **10 seconds**. `48000` appears only as a comment beside the active constant and must not be treated as runtime behavior. Older catalog text describing a two-day lockout was incorrect for the exact 0.10.7 source checkpoint.

## Infernal Mutagen

- stage 0/1: `ON_FIRE` damage is halved until stage 2;
- stage 1: `+20%` Iron's Fire Spell Power when present; attackers and struck victims can be ignited for 6 seconds; crouch-right-click may convert an item that matches a smelting recipe producing Charcoal into one Charcoal;
- stage 2: clears fire continuously, fire-tag damage is set to zero, and water/rain/bubble exposure periodically applies Weakness.

This occupies personal fire adaptation. It does not create or own Black Arcana's planned external Nether-fluid reservoir economy.

## Mob Mutagen

`toxony:mob_mutagen` is a separate mob transformation surface. Source-observed modifiers:

- Max Health `+1.0` multiplied-base;
- Movement Speed `+0.25` multiplied-base.

The provider mob-toxin helper applies this Mutagen when a mob's toxin amount exceeds its maximum health and it does not already have Mob Mutagen. No player Affinity maps to this effect.

## Iron's compatibility matrix

The exact Toxony source line builds against Iron's `1.21.1-3.16.0`; the current pack uses `1.21.1-3.16.3`.

At stage 1+:

| Mutagen | Iron's attribute | Modifier |
|---|---|---:|
| Beast | `nature_spell_power` | `+0.20 ADD_MULTIPLIED_TOTAL` |
| Aqua | `ice_spell_power` | `+0.20 ADD_MULTIPLIED_TOTAL` |
| Spirit | `evocation_spell_power` | `+0.20 ADD_MULTIPLIED_TOTAL` |
| Necrotic | `blood_spell_power` | `+0.20 ADD_MULTIPLIED_TOTAL` |
| Infernal | `fire_spell_power` | `+0.20 ADD_MULTIPLIED_TOTAL` |

Hollow and Mob Mutagen do not expose an Iron's School Spell Power modifier in the audited paths.

## Authority and deduplication

- Toxony owns Toxicity, Tolerance, threshold selection, Affinity weights, Mutagen entry order and active Mutagen effects.
- Black Arcana does not create a second Mutagen tracker.
- RPG Skill Tree may gate/consume progression only through a real integration contract; it does not become authority for Toxony transformation state.
- Black Arcana must not add a duplicate School Spell Power bonus for an already-active Toxony Mutagen.
- Necrotic resurrection is provider-owned and must not trigger a second Black Arcana resurrection/refund path.
- Guided Spirit damage and other Mutagen-triggered effects require causal deduplication if ever observed for progression.

## Validation status

The registry/formulas above are source-observed at the exact public 0.10.7 version checkpoint, not installed-runtime acceptance. License conflict, Iron's 3.16.3 drift, selector tie behavior and live cooldown/effect semantics remain QA gates.
