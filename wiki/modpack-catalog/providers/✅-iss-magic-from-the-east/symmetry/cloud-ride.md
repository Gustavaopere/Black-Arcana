# Cloud Ride

**Registro físico confirmado (2026-10-13):** ✅ `COUNTED_EXACT` — `iss_magicfromtheeast:cloud_ride` / `net.warphan.iss_magicfromtheeast.spells.symmetry.CloudRideSpell`, school default `MFTESchoolRegistries.SYMMETRY_RESOURCE` ([prova Java 21 #38449995162](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38449995162); [dossiê](../EXACT-BINARY-SPELLS-1.1.5.md)). Os números e comportamentos descritos abaixo continuam derivados da fonte pinada, não aprovados em runtime físico/Survival. **+0 identidade adicional**.

- **ID:** `iss_magicfromtheeast:cloud_ride`
- **School:** Symmetry
- **Levels:** 1–9
- **Min rarity:** Uncommon
- **Cast:** Instant
- **Mana neutral:** 20–68
- **Spell power neutral:** 15–95
- **Cooldown:** 90 s
- **Duration neutral:** 15–95 s
- **Recast count:** 2

## Contract

Spawns `SummonCloudEntity` and registers it through `SummonManager` for `spellPower*20` ticks.

Only the summoner can mount it through normal interaction. While ridden:

- yaw/pitch follow rider look;
- forward input controls horizontal travel;
- when moving forward, vertical input is derived from rider look-angle Y;
- rider receives `CLOUD_BLESS_EFFECT` continuously;
- cloud is immune to ordinary damage and only accepts damage tagged bypass-invulnerability;
- cloud cannot be pushed/leashed and is not fluid-pushed.

This confirms the public “look up/down to control height” behavior.

## Static source quirk

The spell calls `spawn.add(forward.x, 0.25f, forward.z)` without reassigning the immutable Vec3 result. In the audited source the cloud remains initialized at `entity.position()` rather than the intended offset. Treat as QA finding, not a silent documentation fix.

## Dedup

Identity = timed rideable magical cloud with view-controlled vertical movement and Cloud Bless; it is not a generic flight buff.

## Source

`CloudRideSpell.java` + `SummonCloudEntity.java`.
