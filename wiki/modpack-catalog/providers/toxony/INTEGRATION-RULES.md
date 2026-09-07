# Toxony 0.10.7 — Black Arcana integration rules

## Authority split

### Toxony owns

- Toxicity;
- Tolerance;
- threshold progression;
- Affinity weights and selection;
- Mutagen list/order/amplifier state;
- harmful toxin/corrosion statuses;
- Oil registry and coating/delivery semantics;
- Toxony alchemical processing/progression;
- provider-owned compatibility modifiers and summons.

### Black Arcana owns

- its canonical cast pipeline;
- resource transactions for Black Arcana casts;
- Arcane Danger;
- Arcane Resistance;
- Corruption Resistance;
- Arcane Strain;
- Arcane Backlash;
- Black Arcana Corruption state;
- Black Arcana rituals/domains/world-effect policy.

### RPG Skill Tree

RPG Skill Tree may remain a progression/mastery/perk provider when a real integration contract exists. It does not become authority for Toxony Toxicity, Affinities or Mutagens.

## No duplicate state

Black Arcana must not create:

- a second Toxicity bar;
- a second Tolerance value;
- a mirrored Mutagen ledger;
- a duplicate Affinity-selection system;
- a second Oil/coating registry;
- shadow cooldowns for Toxony-owned Mutagen mechanics.

A Black Arcana feature may query or transact with a provider-owned value only through a verified boundary that preserves Toxony's settlement semantics.

## No duplicate effect settlement

Toxony damage/status/equipment/projectile paths remain provider-owned.

Do not:

- rerun an Oil effect after observing a hit;
- treat every toxin tick as a new Black Arcana cast;
- attribute Guided Spirit damage as a second player cast without causal provider evidence;
- start Black Arcana Backlash merely because a Toxony Mutagen performs damage;
- trigger normal offensive proc chains from any Black Arcana consequence layer attached to an external event.

## Iron's School Spell Power

Five Mutagens source-observably add Iron's School Spell Power at stage 1+:

- Beast → Nature;
- Aqua → Ice;
- Spirit → Evocation;
- Necrotic → Blood;
- Infernal → Fire.

Black Arcana/RPG Skill Tree must not add a second copy to represent the same Mutagen.

The installed pack uses Iron's 3.16.3 while the exact Toxony 0.10.7 source line builds against 3.16.0. Until runtime QA proves compatibility, any adapter relying on those exact attributes remains fail-closed.

## Resurrection deduplication

Necrotic Mutagen stage 2 contains provider-owned fatal-damage recovery. If Black Arcana later exposes its own resurrection/life-preservation capability:

1. each provider keeps its own admission/cost/cooldown authority;
2. a single lethal event must not be settled twice accidentally;
3. provider ordering/priority must be explicit if both systems can respond;
4. Black Arcana must never reset or mutate Toxony's resurrection cooldown directly;
5. the exact provider cooldown must be runtime-verified before compatibility claims.

## Corruption and Strain remain separate

Toxony Toxicity is not Black Arcana Corruption.

Toxony Tolerance is not Arcane Resistance or Corruption Resistance.

A Mutagen stage is not Arcane Strain.

Conversion between these channels requires an explicit design decision and transactional provider contract; thematic similarity is insufficient.

## Progression / Mastery

If RPG/Black Arcana progression later reacts to Toxony actions:

- use discrete provider events with proven player/caster identity;
- deduplicate one causal action into one progression settlement;
- do not award Mastery from periodic effect ticks, passive Mutagen presence, Toxicity polling or equipment possession;
- automated/dispenser/projectile paths without stable player provenance must fail closed for player progression.

## Candidate API surface

The exact source contains `ChangeToxEvent`, `ChangeToleranceEvent` and `ChangeThresholdEvent` under an `api` namespace and posts them on the NeoForge bus.

These are **candidate integration seams only**. They are not approved as Black Arcana adapter boundaries until:

- upstream license conflict is reconciled;
- exact installed-JAR equivalence is confirmed;
- API stability/support is established;
- behavior is tested with the current pack versions.

Do not couple Black Arcana core to Toxony implementation classes.

## World safety

Toxony provider effects remain Toxony-owned even when they alter entities or local gameplay. Black Arcana's `WorldEffectPolicy` governs destructive effects initiated by Black Arcana; it does not retroactively claim authority over provider-native Toxony mutations/effects.

If Black Arcana deliberately initiates a cross-provider action that can cause world mutation, the Black Arcana side must still satisfy its normal world-safety admission before invoking the provider boundary.

## Fail-closed rule

Current provider-specific implementation status:

`DISABLED / FAIL-CLOSED`.

The Phase 2 catalog is sufficient for semantic deduplication and future boundary design, not for silently adding a runtime adapter.
