# 06.02 — Arcane Resistance

## Objective
Create the canonical internal-resilience stat used to mitigate Arcane Backlash without conflating it with generic magic resistance or vanilla armor.

## Formula
Initial canonical residual-backlash curve:

`residual(R) = K / (K + clamp(R, 0, R_MAX))`

Defaults:
- `K = 40`;
- `R_MAX = 240`;
- effective resistance is finite and non-negative;
- output is clamped to `[0,1]` before profile floors/multipliers;
- `R=0` is exactly `1.0` residual backlash.

No resistance path may produce healing, NaN, infinity or arithmetic overflow.

## Source model
Create a registered provider system. Each contribution reports at least:
- stable provider/source id;
- source category/bucket;
- bounded amount;
- optional diagnostic label/metadata.

Expected buckets include native/base, Black Arcana armor/items, Curios, buffs/effects, rituals, RPG and external providers. Each bucket has an explicit ceiling and the final sum has `R_MAX`; no unlimited additive stacking.

Provider queries are read-only and server-side. One failing provider is isolated, diagnosed and contributes zero rather than crashing the cast or granting arbitrary resistance.

## Snapshot
`ArcaneResistanceSnapshot` stores:
- effective resistance;
- residual multiplier;
- complete bounded source breakdown;
- curve/profile version or constants needed for reproducibility.

The snapshot is captured at hazard-session activation and is immutable for that root cast.

## Explicit exclusions
By default none of these contribute automatically:
- vanilla armor;
- armor toughness;
- generic magic damage resistance;
- Enshrouded/Shroud state;
- Volcanoes heat/respiration/toxicity stats.

A future bridge may intentionally contribute through a registered provider, but never implicitly.

## RED
Tests:
- `0 resistance -> exactly 1.0 residual`;
- increasing resistance monotonically lowers residual;
- diminishing returns are demonstrable;
- negative/NaN/infinite values cannot create healing or invalid output;
- bucket/global caps prevent absurd stacking;
- provider ordering does not change the result;
- provider exception is isolated;
- snapshot remains unchanged after provider/equipment state changes.

## GREEN
Implement curve, provider registry, contribution aggregation and immutable snapshot only.

## REFACTOR
Share finite/clamp math with Corruption Resistance where useful, but keep the two channels semantically and registrationally separate.

## Acceptance
A player can reach the same effective Arcane Resistance through multiple build compositions, but no trivial provider combination can exceed hard ceilings or erase the canonical zero-resistance rule.
