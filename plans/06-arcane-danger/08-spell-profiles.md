# 06.08 — Spell Danger Profiles

## Objective
Allow dangerous spells to declare risk through bounded data instead of requiring a new Java class for every combination of backlash/corruption/strain rules.

## Registry
Create a server-owned `ArcaneDangerProfileRegistry` keyed by canonical `ArcanaSpellId`. Keep it separate from frozen `ArcanaSpellDefinition` so Stage 02 binary/domain contracts are not unnecessarily widened.

A spell without a profile is treated as non-hazardous only when that absence is intentional/valid for its content family. Later dangerous content must fail validation if it claims forbidden/dangerous identity without a profile.

## Data path
Use a dedicated bounded datapack schema, for example:

`data/<namespace>/black_arcana/hazards/<spell_path>.json`

Do not overload the existing presentation-only spell JSON with executable semantics.

## Allowed fields
Bounded declarative fields may include:
- danger tier;
- forbidden flag/derived semantic;
- backlash aggregation mode and coefficients;
- per-cast backlash ceiling/floor;
- corruption base/per-damage values and unavoidable floor;
- strain base/per-damage/channel values;
- minimum/recommended Arcane Resistance;
- below-minimum policy;
- delayed-damage ownership flags for projectile/DoT/chain/summon families;
- snapshot policy enum;
- emergency-protection allowance;
- profile version/id used by telemetry/recovery.

No scripts, commands, class names, reflective methods or arbitrary predicates are accepted from data.

## Validation
Dangerous/forbidden linear profiles must preserve the canonical zero-resistance rule. Profile validation rejects:
- negative/non-finite coefficients;
- values beyond hard safety ceilings;
- unknown fields/enums;
- resource id/path mismatch;
- impossible floors/caps;
- dangerous/forbidden profiles that silently configure zero backlash where the canonical rule applies;
- summon/DoT ownership without bounded lifetime/lease semantics.

Reload is atomic: one malformed profile must not partially publish a new snapshot.

## Migration
Spell/profile IDs need explicit migrations parallel to existing spell/runtime migration infrastructure. Persisted corruption/strain does not depend on old profile objects; any persistent delayed effect that references a profile must carry a version/migration route.

## RED
Tests:
- valid profile round-trip/parse;
- unknown field rejection;
- non-finite/out-of-range rejection;
- dangerous `R=0` invariant cannot be configured away;
- atomic reload on one bad file;
- missing profile behavior is explicit;
- profile ID migration is deterministic/cycle-free;
- client cannot submit/override profile values.

## GREEN
Implement registry, strict codec/parser, reload listener and validation only after pure hazard contracts exist.

## REFACTOR
Keep formula/effect execution in code-owned bounded strategies selected by enum/id. Datapacks choose among safe strategies; they do not implement them.

## Acceptance
A dangerous test spell can acquire its complete risk profile from a datapack reload, while malformed or malicious data fails closed without partial runtime mutation.
