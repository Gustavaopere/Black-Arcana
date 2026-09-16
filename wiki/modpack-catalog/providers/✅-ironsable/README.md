# IronSable — provider catalog

## Installed identity

- Mod ID: `ironsable`
- Installed JAR: `ironsable-1.2.0.jar`
- Runtime: `1.2.0`
- Minecraft: `1.21.1`
- Loader: NeoForge
- CurseForge project: `1625528`
- Exact installed release: file `8598255`, `ironsable-1.2.0.jar`, published 2026-08-07.
- Required systems: Iron's Spells 'n Spellbooks + Sable.
- Current pack also contains Wind's Spellbooks `1.0.5`.

## Audit state

`RELEASE-PINNED 1.2.0 / RUNTIME REGISTRY 7/7 OBSERVED / SEMANTIC CATALOG 7/7 COMPLETE / JAR BYTECODE QA PENDING`

The public project page states that IronSable 1.2.0 adds **7 new spells** and physicalizes **10 existing Iron's spells**. Historical runtime logs from this pack independently expose all seven `ironsable:*` spell IDs. The linked public GitHub repository contains issue templates and a README but no mod source tree, so this provider is **not source-pinned**. Exact bytecode/API signatures remain unverified until the installed JAR can be extracted.

## Seven IronSable-owned spells

Because Wind's Spellbooks `1.0.5` is installed, the 1.2.0 release explicitly assigns Wind school to three spells:

### Wind classification active in this pack

- [Maelstrom](wind/maelstrom.md) — `ironsable:maelstrom`
- [Tempest's Grasp](wind/tempests-grasp.md) — `ironsable:tempests_grasp`
- [Downburst](wind/downburst.md) — `ironsable:downburst`

### School not verified from exact 1.2.0 artifact/public metadata

- [Gyroscopic Spin](school-unverified/gyroscopic-spin.md) — `ironsable:gyroscopic_spin`
- [Stasis Lock](school-unverified/stasis-lock.md) — `ironsable:stasis_lock`
- [Kinetic Barrier](school-unverified/kinetic-barrier.md) — `ironsable:kinetic_barrier`
- [Elastic Tether](school-unverified/elastic-tether.md) — `ironsable:elastic_tether`

## Physicalized existing spells

IronSable also adds Sable-ship interaction to 10 existing spells without taking ownership of their normal spell stats. See [PHYSICALIZED-BASE-SPELLS.md](PHYSICALIZED-BASE-SPELLS.md).

Provider-native authority is split deliberately:

- Iron's Spells owns normal spell registration, damage, mana, cooldown, ordinary entity targeting and base spell semantics for those 10 existing spells.
- IronSable owns the additional ship/physics response.
- Black Arcana bridges must not apply a second force/rotation/orbit/tether effect when IronSable has already handled the physics object.

## Acquisition

The public IronSable description states that all seven new spells:

- use the same loot ecosystem as Iron's Spells;
- can be made at the Scroll Forge;
- appear in the IronSable creative tab with scrolls at every level.

Exact loot-table weights, Scroll Forge ingredient costs and rarity distributions: **NÃO VERIFICADO**.

## Version 1.2.0 deltas relevant to this pack

- Wind school for Tempest's Grasp, Downburst and Maelstrom when Wind's Spellbooks is installed — condition satisfied in the current pack.
- Public physics API for companion mods — API existence confirmed; exact classes, methods and signatures are **NÃO VERIFICADO** without source/JAR extraction.

## Mandatory QA gates before runtime reuse

- exact levels, rarity, mana, cooldown, cast/channel timings and numerical formulas for all seven spells;
- exact schools of Gyroscopic Spin, Stasis Lock, Kinetic Barrier and Elastic Tether;
- Sable physics API hook/signatures and server/client authority;
- ship ownership/friendly-fire/self-ship rules;
- chunk/sublevel/dimension lifecycle behavior;
- idempotence/deduplication when multiple physics bridges observe the same cast;
- optional Create Aeronautics behavior, especially Raise Hell balloon inflation;
- Wind school resource identity used at runtime.

See [TECHNICAL-AUDIT.md](TECHNICAL-AUDIT.md).