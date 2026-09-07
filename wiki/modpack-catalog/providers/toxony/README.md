# Toxony 0.10.7 — toxicology, oils and mutagen authority

## Status

`EXACT INSTALLED ARTIFACT 0.10.7 / EXACT PUBLIC SOURCE VERSION PIN 881bf7fe / 5 HARMFUL EFFECTS / 9 OILS / 7 MUTAGEN EFFECTS / 11 AFFINITIES / THRESHOLD MODEL AUDITED / IRON'S+VAMPIRISM+WEREWOLVES COMPAT SOURCE-OBSERVED / LICENSE CONFLICT GPLv3↔LGPLv3 / RUNTIME+API QA PENDING / FAIL-CLOSED FOR PROVIDER-SPECIFIC IMPLEMENTATION`

## Runtime identity

Current physical modlist authority:

- provider: **Toxony**;
- installed JAR: `toxony-0.10.7.jar`;
- mod id: `toxony`;
- runtime version: `0.10.7`;
- mixin config: `toxony.mixins.json`;
- SHA-1: `d92e0d0ae2ece85c353f22463fbc7c61595fca20`;
- CurseForge/package fingerprint: `1401862999`;
- loader/game: NeoForge 1.21.1;
- role: `TOXICITY / ALCHEMY / MUTAGEN / OIL PROVIDER`.

The modlist remains authoritative for the binary actually installed in the pack.

## Exact public source checkpoint

Official public repository: `MrFrostyDev/Toxony_Mod`.

Exact version-line commit audited:

`881bf7fe632659e748c279966a2bf49b99f7503f`

At that commit:

- `minecraft_version=1.21.1`;
- `neo_version=21.1.221`;
- `mod_id=toxony`;
- `mod_version=0.10.7`;
- Curios build dependency `9.5.1+1.21.1`;
- Iron's build dependency `1.21.1-3.16.0`.

The commit itself performs the public `0.10.6 -> 0.10.7` version bump and includes the 0.10.7 Plaguebringer recipe correction/update line.

### License conflict — implementation gate

The exact source checkpoint contains contradictory publisher evidence:

- `gradle.properties` declares `GNU LGPL 3.0`;
- public release metadata also identifies the project/release as LGPLv3;
- the root `LICENSE` file at the same commit contains the **GNU GPL v3** license text.

Black Arcana therefore treats the source as usable for **read-only factual cataloging**, but not as an implementation-derivation authority until the upstream licensing conflict is reconciled.

Consequences:

- no Toxony code/assets are copied or adapted;
- source-visible classes/methods are not promoted automatically to supported API contracts;
- provider-specific adapters remain fail-closed;
- source-observed formulas and hooks remain separate from installed-runtime validation.

See [Technical audit](TECHNICAL-AUDIT.md).

## Provider identity and authority

Toxony is not an Iron's spell school and not a Black Arcana resource provider. It owns a preparation/transformation system around:

- player Toxicity and Tolerance;
- threshold progression;
- ingredient knowledge;
- weighted Affinities;
- persistent Mutagen state;
- harmful toxin/corrosion effects;
- Oils and delivery items/projectiles;
- Mortar & Pestle, Crucible, Alembic and Alchemical Forge progression;
- monster-hunter weapons/armor and compatibility behavior.

Black Arcana must not create a second generic Toxicity bar, duplicate Mutagen ledger or parallel Oil registry.

## Canonical subcatalogs

- [Effects — 5/5](effects/README.md)
- [Oils — 9/9](oils/README.md)
- [Mutagens + Affinities + thresholds](mutagens/README.md)
- [Technical/API/provenance audit](TECHNICAL-AUDIT.md)
- [Black Arcana integration rules](INTEGRATION-RULES.md)

## Registry counts at the exact 0.10.7 source checkpoint

### Harmful effects — 5

1. `toxony:hunt`
2. `toxony:toxin`
3. `toxony:acid`
4. `toxony:flammable`
5. `toxony:cripple`

### Oils — 9

1. `toxony:poison_oil`
2. `toxony:toxin_oil`
3. `toxony:fatigue_oil`
4. `toxony:fire_resistance_oil`
5. `toxony:glowing_oil`
6. `toxony:acid_oil`
7. `toxony:smoke_oil`
8. `toxony:regeneration_oil`
9. `toxony:witchfire_oil`

### Mutagen effects — 7

1. `toxony:beast_mutagen`
2. `toxony:spirit_mutagen`
3. `toxony:aqua_mutagen`
4. `toxony:hollow_mutagen`
5. `toxony:necrotic_mutagen`
6. `toxony:infernal_mutagen`
7. `toxony:mob_mutagen`

`mob_mutagen` is a distinct mob-toxicity transformation path. It is not one of the six player Affinity-selected candidates.

## Toxicity / Tolerance / threshold state

The exact source checkpoint stores synchronized player state for:

- Toxicity;
- Tolerance;
- current threshold;
- Affinity weights;
- up to three Mutagen entries;
- known ingredients;
- death state.

Source constants:

| Field | 0.10.7 source value |
|---|---:|
| minimum Tolerance | `10` |
| default Tolerance | `30` |
| maximum Tolerance | `999` |
| maximum Mutagen entries | `3` |
| threshold multiplier | `100` |
| initial threshold goal | `100` |

Threshold goal uses the provider triangular-number function:

`goal(threshold) = ((threshold + 1) * (threshold + 2) / 2) * 100`

Because advancement checks use strict `tox > goal`, the practical player threshold crossings inside the 999 Tolerance ceiling are:

- first: `tox > 100`;
- second: `tox > 300`;
- third: `tox > 600`.

A requested Toxicity value above current Tolerance is clamped to Tolerance and marks provider `deathState=true`. Toxicity at or below zero resets threshold progression. This state remains entirely Toxony-owned.

## Affinity registry — 11/11

| Affinity | Source index | Player Mutagen candidates |
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

When a player gains one or more thresholds, the provider sums accumulated Affinity weights into each candidate Mutagen. Every candidate linked to an Affinity receives that Affinity's full weight. The greatest score wins, then Affinities are cleared.

If several thresholds are skipped at once, selection is repeated once per skipped threshold **before** the shared Affinity map is cleared, so the same weighting basis may produce multiple entries.

If no candidate exists, the source falls back to Beast Mutagen.

### Tie-order QA blocker

The located selection path uses a `HashMap` and replaces the winner only on a strictly greater score. It defines no explicit stable tie-break for equal scores. Black Arcana must not rely on a deterministic provider tie outcome until runtime/API behavior is verified.

## Mutagen stacking identity

The provider stores at most three Mutagen entries. Adding a fourth removes the oldest entry. Duplicate entries are not rejected; when the active Mutagen effects are rebuilt, duplicate entries stack the MobEffect amplifier.

For catalog terminology:

- amplifier `0` = first copy / stage 0;
- amplifier `1` = second copy / stage 1;
- amplifier `2` = third copy / stage 2.

Do not convert these stages into Black Arcana progression levels.

## Important correction — Necrotic resurrection

Previous catalog text described a **2-day lockout**. That is not the executable 0.10.7 source value.

The exact source sets:

`DEFAULT_RESURRECTION_COOLDOWN = 200`

with `48000` present only as a commented historical value. At 20 ticks/s, the source-observed cooldown is **10 seconds**.

At Necrotic stage 2, when the provider resurrection gate is active and the entity is dead/dying, health is restored to half maximum and the 200-tick cooldown starts.

This is a high-impact runtime QA item because a stale description would materially change balance/dedup conclusions.

## Iron's Spell Power compatibility — source-observed

The Toxony 0.10.7 source was built against Iron's `1.21.1-3.16.0`; the current pack uses Iron's `1.21.1-3.16.3`.

At Mutagen amplifier >=1, five source classes attempt to resolve an Iron's attribute and add `0.20` with `ADD_MULTIPLIED_TOTAL`:

| Mutagen | Iron's attribute | Source modifier |
|---|---|---:|
| Beast | `nature_spell_power` | `+0.20` |
| Aqua | `ice_spell_power` | `+0.20` |
| Spirit | `evocation_spell_power` | `+0.20` |
| Necrotic | `blood_spell_power` | `+0.20` |
| Infernal | `fire_spell_power` | `+0.20` |

These are Toxony-owned provider bonuses. Black Arcana and RPG Skill Tree must not add a second copy to “represent” the same Mutagen.

Exact behavior with Iron's 3.16.3 remains runtime QA pending.

## Vampirism / Werewolves silver compatibility — source-observed

The exact source declares provider tag keys:

- `vampirism:vampire`;
- `werewolves:werewolf`.

Its silver-damage helper multiplies damage by `1.5` when the target EntityType matches either tag. At the audited source pin, direct usages located include the Toxony Flintlock Ball and Flail Ball damage paths.

Do not generalize this to “all silver items in the pack deal +50%” without separate evidence.

## Curios compatibility

Public provider documentation/release history identifies the Toxicity Gauge as Curios Charm-compatible. Curios remains authority for slot/equipment state. Black Arcana must not poll or mirror that state into a second equipment ledger.

## Witchcraft / domain deduplication consequences

Toxony materially occupies:

- lethal toxin and corrosion families;
- flammability priming;
- weapon coatings and projectile chemical delivery;
- player Toxicity/Tolerance progression;
- affinity-weighted transformations;
- persistent Mutagen stages;
- spirit-themed combat adaptation;
- personal fire adaptation;
- conditional resurrection;
- toxic ingredient discovery/alchemy.

Consequently:

- Hexalia/Black Arcana witchcraft may consume or react to provider-owned Toxony state only through a verified boundary;
- Black Arcana must not introduce duplicate generic Poison/Toxin/Acid oils;
- Black Arcana must not build a second affinity-to-mutagen progression graph;
- Infernal Mutagen does not occupy the planned external Nether-fluid reservoir architecture, but it does occupy personal fire immunity/ignition adaptation;
- Spirit Mutagen does not become a Black Arcana soul resource merely because it summons Guided Spirits;
- Necrotic resurrection is a genuine overlap for resurrection/life-preservation semantics and must be accounted for in capability deduplication.

## Safe integration posture

- Toxony owns Toxicity, Tolerance, thresholds, Affinities, Mutagen state and Oil state.
- No Black Arcana resource conversion may silently mutate those values.
- No duplicate Iron's Spell Power modifier for an already-applied Mutagen.
- No Mastery from continuous Toxicity/Mutagen ticks.
- No double-processing of Toxony oil/projectile damage/effects.
- The existence of `xyz.yfrostyf.toxony.api.*` packages is not, by itself, proof of a stable supported external API contract.
- Source event classes are useful evidence of provider architecture but remain `NOT APPROVED AS ADAPTER BOUNDARY` until licensing, compatibility and runtime gates are reconciled.

## Remaining open gates

1. reconcile the GPLv3 root `LICENSE` versus LGPLv3 metadata/release declarations;
2. verify installed JAR/runtime equivalence with source commit `881bf7fe...` where integration depends on internals;
3. validate Toxony 0.10.7 against the pack's Iron's 3.16.3 rather than source baseline 3.16.0;
4. execute runtime QA for threshold/tie behavior, duplicate Mutagen stacking and Necrotic resurrection cooldown;
5. enumerate/cross-check player-facing recipes/acquisition for Oils and key alchemical blocks where needed for Wiki completeness;
6. verify supported public API/event stability before implementing an adapter;
7. validate Vampirism/Werewolves tag behavior against the exact installed provider versions.

## Phase 3 gate

Toxony now has a strong exact-version **factual** catalog, but provider-specific integration remains:

`BLOCKED / FAIL-CLOSED`

until license provenance, supported API boundary and exact-pack runtime compatibility are resolved. Source visibility is not implementation permission and source catalog completion is not runtime validation.
