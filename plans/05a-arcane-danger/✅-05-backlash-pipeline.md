# 05A.05 — Arcane Backlash Pipeline

## Objective
Implement dedicated `ARCANE_BACKLASH` damage and causal accounting from confirmed Black Arcana spell damage without using generic reflection.

## Damage ownership
All Black Arcana damage that may feed hazard accounting must pass through a Black Arcana-owned damage/provenance gateway or attach equivalent provenance before the damage event fires.

Each eligible damage attempt carries root `ArcanaCastId`, unique `ArcanaDamageInstanceId`, caster UUID, spell/profile snapshot identity, damage family and profile eligibility flags. Damage without valid Black Arcana provenance is not silently attributed to a root cast.

## Confirmed damage
Backlash basis uses the NeoForge 1.21.1 post-damage hook representing actual health damage after mitigation. The exact accessor/signature must be locked by compilation/GameTest against the project NeoForge pin before implementation is considered green. Never use nominal spell damage, pre-armor requested damage or client values as authoritative backlash basis.

## Ledger
Maintain a bounded per-root-cast ledger of confirmed raw eligible damage, profile-aggregated eligible damage, backlash already settled, seen damage-instance IDs and delayed-effect lease/expiry.

For aggregation function `F`:

`deltaEligible = max(0, F(newConfirmedTotal) - F(previousConfirmedTotal))`

`backlash = deltaEligible * profileBacklashMultiplier * residualArcaneResistance`

Then apply explicit unavoidable floors/hard caps. All math is finite/saturating.

## Canonical zero-resistance rule
For canonical `DANGEROUS`/`FORBIDDEN` linear profiles, `F(D)=D`, base multiplier is `1.0`, and `R=0` yields exactly one backlash damage for each one confirmed eligible health damage. AoE/multi-hit profiles may choose explicit bounded aggregation, but zero resistance still returns 100% of their resulting eligible causal damage.

## Delayed ownership
DoT/projectile/chain hits retain the original root hazard session and immutable snapshot; each tick/impact gets a unique damage-instance ID. Summon damage is ineligible by default unless a profile explicitly opts it in with bounded ownership/lifetime rules.

## Dedicated backlash damage
Black Arcana owns a dedicated internal backlash damage source/family. It cannot recurse, count as normal offensive damage, crit, lifesteal, award offensive mastery or feed BA-owned offensive proc chains. Exact vanilla/NeoForge damage tags are chosen and tested against 1.21.1 during implementation.

## Settlement order
For Black Arcana-owned sustain: offensive damage → confirmed health loss → backlash ledger/settlement → corruption/strain settlement → BA-owned lifesteal/sustain → final observers/telemetry. Backlash never creates sustain credit.

## RED
Mandatory tests cover exact zero-resistance 1:1 backlash, resistance curve, non-recursion, offensive-credit exclusions, deterministic AoE/multi-hit aggregation, delayed ownership, duplicate IDs, snapshot immutability after gear swap, summon opt-in, overflow/NaN rejection and lethal backlash source/message.

## GREEN
Implement provenance gateway, bounded ledger, NeoForge post-damage adapter, dedicated damage type/source and backlash application.

## REFACTOR
Keep causal math independent from NeoForge event objects. The event adapter translates confirmed Minecraft damage into pure hazard records.

## Acceptance
A synthetic forbidden spell can damage multiple real entities, receive backlash from only confirmed eligible health loss, and prove through GameTests that backlash itself is terminally non-recursive/non-offensive.
