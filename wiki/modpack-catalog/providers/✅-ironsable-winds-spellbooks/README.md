# IronSable X Wind's Spellbooks — 1.0.0

Status: `✅ CATALOGED / RELEASE-PINNED 1.0.0 / ZERO_SEMANTIC_BRIDGE / FOUR DOCUMENTED WIND-SPELL PHYSICS ADAPTATIONS / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling physical authority records:

- JAR: `ironsable-wind-1.0.0.jar`;
- mod id: `ironsable_wind`;
- runtime: `1.0.0`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `c09c73a83deaf6439f2d33652898eb610dbfa4f3`.

Required current providers recorded by the pack:

- IronSable `1.2.0`;
- Wind's Spellbooks `1.0.5`;
- Sable `2.0.5`;
- Iron's Spells 'n Spellbooks `3.16.3`.

## Publisher/release boundary

Official CurseForge project: `IronSable X Wind's Spellbooks` / project ID `1643762`.

The project exposes one NeoForge 1.21.1 release:

- file: `ironsable-wind-1.0.0.jar`;
- version: `1.0.0`;
- uploaded: 2026-08-07.

The official description identifies the addon as a bridge between Wind's Spellbooks and IronSable and documents four integrations:

- **Tornado** — provider physics integration;
- **Almighty Push** — repulses simulated blocks;
- **Wind Blade** — can break simulated blocks;
- **Aeropic** — impact/collision integration.

Exact public source/bytecode for 1.0.0 is not used in this catalog. Algorithms, radii, force coefficients, target filters and packet/API signatures remain unverified.

## Semantic disposition

This addon does **not** own a new Wind school or new spell identity. The four named spells are already owned and strict-counted under Wind's Spellbooks 1.0.5:

- `wind_spellbooks:tornado`;
- `wind_spellbooks:almighty_push`;
- `wind_spellbooks:wind_blade`;
- `wind_spellbooks:aeropic`.

The bridge adds an interoperability/physics response to those existing casts. Counting any of the four again here would double-count the same semantic spell identity.

Therefore:

- provider-owned independent spells: **0**;
- provider-owned independent rituals/rites/glyphs: **0 established**;
- semantic delta: **+0**;
- catalog classification: **`ZERO_SEMANTIC_BRIDGE`**.

## Authority boundary

- **Wind's Spellbooks** owns the four spell identities and Wind-school semantics.
- **Iron's Spells** owns host casting, mana, cooldown and generic spell settlement.
- **IronSable / Sable** own simulated-block/physics state and transforms.
- **IronSable X Wind's Spellbooks** owns only the compatibility/adaptation layer between those existing systems.

Black Arcana must not:

- charge mana/cooldown a second time;
- apply a second spell hit because a physics reaction also occurred;
- apply force/break twice through both a Black Arcana listener and this bridge;
- infer cast success from client VFX or physical movement;
- count projectiles/recasts/physics events as new Wind spell identities.

RPG Skill Tree may consume verified progression/gate events through real contracts but does not gain casting or physics authority.

## Runtime QA remains fail-closed

Catalog closure is not an assembled-pack runtime PASS. Required QA remains:

- client + dedicated-server boot with the four current providers;
- Tornado interacts with simulated blocks without duplicate physics;
- Almighty Push applies one physical response per eligible target;
- Wind Blade breaks only eligible simulated blocks and does not duplicate drops;
- Aeropic resolves collision/impact in the correct reference frame;
- moving/rotating sublevels preserve target transforms;
- unload/disassembly invalidates stale targets;
- two players do not duplicate force/break settlement;
- provider mana/cooldown/damage remain exactly-once.

## Clean-room / provenance

Evidence used:

- current sibling physical dossier `PROJECT-INSTRUCTIONS/modlist/✅-ironsable-x-winds-spellbooks.md`;
- current physical JAR identity/SHA recorded there;
- official CurseForge release/description for project `1643762`.

No third-party implementation code or assets are copied into Black Arcana.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_BRIDGE`.**

Strict semantic contribution: **+0**. Wind's Spellbooks remains the sole owner of the four affected spell identities.
