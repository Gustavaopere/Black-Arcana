# IronSable X Wind's Spellbooks — 1.0.0

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_EXISTING_SPELL_PHYSICS_BRIDGE / +0 STRICT / RUNTIME QA SEPARATE`

## Physical identity

- JAR: `ironsable-wind-1.0.0.jar`;
- mod id: `ironsable_wind`;
- runtime: `1.0.0`;
- physical SHA-1: `c09c73a83deaf6439f2d33652898eb610dbfa4f3`;
- CurseForge project/file: `1643762 / 8598265`.

## Exact semantic boundary

The hash-matched artifact has **14 classes** and **0 provider assets/data files**. Its class inventory is exclusively bridge/core physics-oriented, including:

- `AeropicPhysics`;
- `AlmightyPushPhysics`;
- `TornadoPhysics`;
- `WindBladePhysics`;
- `WindGuard`;
- calibration/hull-wear/dosage support.

A bounded binary reference check is positive for `wind_spellbooks`, `tornado`, `almighty_push`, `wind_blade`, `aeropic`, `ironsable` and `sable`.

Those four spell identities are already owned and counted under Wind's Spellbooks. This addon adds physical response for them; it does not mint a second copy of each spell.

**Semantic contribution: +0 — `ZERO_SEMANTIC_EXISTING_SPELL_PHYSICS_BRIDGE`.**

See [exact audit](EXACT-1.0.0-ZERO-SEMANTIC-AUDIT.md).

## Authority boundary

Wind's Spellbooks owns the spell identities/cast semantics. IronSable/Sable own physical simulation behavior. This bridge owns compatibility wiring only. Black Arcana must not double-settle mana, cooldown, damage or physics.

## Result

**✅ Cataloged.** Exact compatibility bridge over four existing Wind spells; zero new semantic magic identities.
