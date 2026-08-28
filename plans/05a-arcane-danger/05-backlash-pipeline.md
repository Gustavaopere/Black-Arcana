# 06.05 — Arcane Backlash Pipeline

## Objective
Implement dedicated `ARCANE_BACKLASH` damage and causal accounting from confirmed Black Arcana spell damage without using generic reflection.

## Damage ownership
All Black Arcana damage that may feed hazard accounting must pass through a Black Arcana-owned damage/provenance gateway or attach equivalent provenance before the damage event fires.

Each eligible damage attempt carries:
- root `ArcanaCastId`;
- unique `ArcanaDamageInstanceId`;
- caster UUID;
- spell id/profile snapshot id;
- damage family: direct, projectile, AoE, chain, DoT, summon, environmental, backlash;
- eligibility flags defined by the profile.

Damage without valid Black Arcana provenance is not silently attributed to a root cast.

## Confirmed damage
Backlash basis uses the NeoForge 1.21.1 post-damage hook representing actual health damage after mitigation. The exact accessor/signature must be locked by compilation/GameTest against the project NeoForge pin before implementation is considered green.

Never use nominal spell damage, pre-armor requested damage or client values as the authoritative backlash basis.

## Ledger
Maintain a bounded per-root-cast ledger:
- confirmed raw eligible damage;
- profile-aggregated eligible damage;
- backlash already settled;
- bounded seen damage-instance IDs/dedupe structure;
- expiry/lease associated with delayed effect lifetime.

For aggregation function `F`, each confirmed hit settles only:

`deltaEligible = max(0, F(newConfirmedTotal) - F(previousConfirmedTotal))`

`backlash = deltaEligible * profileBacklashMultiplier * residualArcaneResistance`

Then apply explicit unavoidable floors/hard caps. All math is finite/saturating.

## Canonical zero-resistance rule
For canonical `DANGEROUS`/`FORBIDDEN` linear profiles:
- `F(D)=D`;
- base multiplier is `1.0`;
- `R=0` therefore yields exactly one backlash damage for each one confirmed eligible health damage.

AoE/multi-hit profiles may choose explicit bounded aggregation, but zero resistance still returns 100% of their resulting eligible causal damage.

## DoT/projectiles/chains
Delayed hits lease/reference the original root hazard session. They never create a new root cast. Each tick/impact has a new damage-instance ID but shares the immutable resistance/profile snapshot.

A persistent delayed effect cannot outlive its hazard attribution lease. If later content survives restart, its recovery contract must restore the immutable hazard snapshot or clean the effect; silently losing backlash ownership is forbidden.

## Summons
Summon/servant damage is ineligible by default. A profile must explicitly opt a summon damage family into the root cast and define a bounded lifetime/ownership rule.

## Dedicated backlash damage
Add a Black Arcana damage type/source whose semantics are internal arcane backlash. By default:
- vanilla armor/toughness do not mitigate it through the specialized BA calculation;
- generic magic resistance does not automatically substitute for Arcane Resistance;
- it cannot be eligible Black Arcana offensive damage;
- it cannot recurse;
- it cannot crit, lifesteal, grant offensive mastery or feed offensive proc chains through BA-owned hooks.

Exact vanilla damage tags are chosen/tested against 1.21.1 during implementation; do not guess them from another Minecraft version.

## Lifesteal/order
For Black Arcana-owned sustain:
1. offensive damage is applied;
2. post-damage confirms health loss;
3. ledger records/settles backlash;
4. corruption/strain damage-linked deltas settle;
5. only then may BA-owned lifesteal/sustain consume the confirmed-damage credit.

Backlash never creates sustain credit. External-mod lifesteal ordering is compatibility-tested; Black Arcana still marks backlash as non-offensive even if an external mod ignores provenance.

## Death
If backlash kills the caster, the death source/message identifies self-consumption by dangerous arcana. Add English and PT-BR localization. Death does not award offensive credit/mastery to the caster or victim.

## RED
Mandatory tests:
- zero resistance -> exact 100% backlash;
- resistance reduces backlash using the frozen curve;
- backlash cannot recursively produce backlash;
- backlash cannot create offensive proc/mastery/lifesteal credit;
- AoE aggregation is deterministic;
- multi-hit order does not alter total settlement;
- DoT ticks retain one root cast but unique damage IDs;
- duplicate damage instance is ignored once;
- projectile impact retains snapshot after gear swap;
- summon damage is ineligible by default and eligible only by explicit profile;
- overflow/NaN cannot escape the ledger;
- lethal backlash produces the dedicated death source/message.

## GREEN
Implement provenance gateway, bounded ledger, NeoForge post-damage adapter, dedicated damage type/source and backlash application.

## REFACTOR
Keep causal math independent from NeoForge event objects. Event adapter translates confirmed Minecraft damage into pure hazard records.

## Acceptance
A synthetic forbidden spell can damage multiple real entities, receive backlash from only the confirmed eligible health loss, and prove through GameTests that the backlash itself is terminally non-recursive/non-offensive.
