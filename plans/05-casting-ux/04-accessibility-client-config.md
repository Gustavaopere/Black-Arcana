# 05.04 — Accessibility & Client Configuration

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

## Canonical options

`BlackArcanaClientConfig` currently exposes:

- contextual HUD enable/disable;
- HUD scale and anchor;
- selection and feedback durations;
- feedback level (`MINIMAL`, `STANDARD`, `VERBOSE`);
- radial behavior (`TOGGLE`, `HOLD`);
- client particle-density multiplier;
- reduced-motion preference;
- reduced-flashes preference.

## Authority rule

These values are registered as `ModConfig.Type.CLIENT`. They may reduce or reshape presentation but never alter server damage, spell power, cooldown, resource cost, progression, target admission or world-effect policy. They are not authority inputs to cast validation packets.

## Deferred acceptance

Local persistence, missing-entry migration/default behavior and the perceptual quality of reduced-motion/reduced-flash presentation remain part of the real-client manual matrix where direct observation is required.
