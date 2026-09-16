# Gravity

Status: `SOURCE-PINNED 5.13.1 / RANGE-EFFECT RITUAL`

- Registry id: `ars_nouveau:ritual_gravity`
- Class: `RitualGravity`
- Effect: provider `GRAVITY_EFFECT`
- Effect duration: `60 × 20 = 1200 ticks`
- Range: `60` blocks
- Source cost declaration: `200`
- Class constants: `renewInterval = 20`, `renewThreshold = 200`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Gravity extends Ars Nouveau's `RangeEffectRitual`, sharing its server-only range admission and Source-backed refresh semantics. The ritual applies the provider `GRAVITY_EFFECT`, described as forcing nearby players to the ground, and can refresh the effect while the player remains within range.

A successful `RangeEffectRitual.attemptRefresh` marks the ritual as needing Source, so effect application and Source settlement remain coupled inside Ars Nouveau's ritual runtime.

## Black Arcana boundary

Gravity-effect application, refresh cadence and Source debit are Ars Nouveau authority. Black Arcana must not add a second gravity state or charge a second resource when observing the ritual.

The capability overlaps battlefield control/Space thematically but does not transfer Ars' effect state into Black Arcana's domain runtime.

## QA

The source class and shared range-effect contract are pinned to 5.13.1. Exact external refresh scheduling and interactions with flight/mobility providers remain runtime QA.