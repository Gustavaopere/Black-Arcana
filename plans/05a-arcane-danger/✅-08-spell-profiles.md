# 05A.08 — Spell Danger Profiles

## Objective
Allow dangerous spells to declare risk through bounded data instead of requiring a new Java class for every combination of backlash/corruption/strain rules.

## Registry
Create a server-owned `ArcaneDangerProfileRegistry` keyed by canonical `ArcanaSpellId`. Keep it separate from frozen `ArcanaSpellDefinition` so Stage 02 binary/domain contracts are not unnecessarily widened.

A spell without a profile is treated as non-hazardous only when that absence is intentional for its content family. Dangerous/forbidden content must fail validation if it lacks a required profile.

## Data path
Use a dedicated bounded datapack schema such as `data/<namespace>/black_arcana/hazards/<spell_path>.json`. Do not overload the existing presentation-only spell JSON with executable semantics.

## Allowed fields
Bounded declarative fields may include danger tier, forbidden semantic, aggregation mode/coefficients, backlash floors/ceilings, corruption and strain coefficients, minimum/recommended resistance, below-minimum policy, delayed-damage ownership, snapshot policy, emergency-protection allowance and profile version. No scripts, commands, class names, reflective methods or arbitrary predicates.

## Validation
Reject negative/non-finite values, hard-ceiling violations, unknown fields/enums, resource-id/path mismatch, impossible floors/caps, dangerous linear profiles that configure away the zero-resistance invariant and delayed ownership without bounded lifetime semantics. Reload is atomic.

## Migration
Spell/profile IDs use explicit deterministic cycle-free migrations parallel to existing runtime migration infrastructure. Persistent delayed effects that reference a profile must carry a version/migration route.

## RED
Tests cover valid parse/round-trip, unknown fields, non-finite/out-of-range data, zero-resistance invariant, atomic reload, explicit missing-profile behavior, deterministic migrations and inability of clients to submit profile values.

## GREEN
Implement registry, strict codec/parser, reload listener and validation after pure hazard contracts exist.

## REFACTOR
Keep formula/effect execution in code-owned bounded strategies selected by enum/id. Datapacks choose among safe strategies; they do not implement them.

## Acceptance
A dangerous test spell can acquire its complete risk profile from a datapack reload, while malformed or malicious data fails closed without partial runtime mutation.
