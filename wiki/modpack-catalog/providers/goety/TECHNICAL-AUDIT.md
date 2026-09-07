# Goety 3.1.4 — Technical audit

Status: `EXACT RELEASE-PINNED / PUBLIC DOCUMENTATION AUDITED / EXACT 3.1.4 SOURCE+API+JAR REGISTRY UNVERIFIED / RUNTIME QA PENDING`

## Exact installed identity

Current modpack authority establishes:

- mod id: `goety`;
- JAR: `goety-3.1.4.jar`;
- runtime version: `3.1.4`;
- Minecraft: 1.21.1;
- loader: NeoForge.

The current pack snapshot contains 612 top-level entries including NeoForge. Internal jarjar dependencies are not counted as top-level providers.

## Exact public release

The provider README records the exact 3.1.4 public release identity, including CurseForge file `8689429`, release date `2026-08-20`, Release channel and MIT declaration on the public project/release surface.

That release identity is strong enough to pin **which artifact/version the catalog targets**. It is not source-code equivalence evidence.

## Official source limitation

The official public project links source to `Polarice3/Goety-2`. At the audit checkpoint, the public repository exposes historical branches such as `1.20` and `1.19`, but no auditable official `1.21.1` / `3.1.4` branch or tag corresponding to the installed release was available through the verified source path.

The exact 3.1.4 release also did not expose an additional source archive through the public release surface used in this audit.

Therefore:

- historical `1.20` code is **not** current 3.1.4 authority;
- third-party 1.21.1 forks are **not** silently substituted for official 3.1.4 source;
- no decompilation is used to reverse-engineer exact implementation internals;
- implementation-facing claims that require class/method/registry/API evidence stay fail-closed.

## Evidence classes

| Claim class | Current state |
|---|---|
| installed JAR/version | EXACT |
| exact public 3.1.4 release identity | EXACT |
| provider role: Soul Energy / Focus / ritual / servant / progression | VERIFIED FROM CURRENT PROJECT GUIDE + PUBLIC PROVIDER DOCS |
| 110 base Focus names / 10 families | PUBLIC DOCUMENTATION INVENTORY |
| 12 public Wands/Staffs | PUBLIC DOCUMENTATION INVENTORY |
| 13 public ritual families | PUBLIC DOCUMENTATION INVENTORY |
| 10 public research lines | PUBLIC DOCUMENTATION INVENTORY |
| exact 3.1.4 registry ids | UNVERIFIED |
| exact 3.1.4 per-Focus costs/cooldowns/damage/range | UNVERIFIED except separately documented cases |
| exact 3.1.4 ritual recipe registries | UNVERIFIED |
| exact 3.1.4 stable integration API | UNVERIFIED |
| exact modpack runtime behavior | UNVERIFIED |

## Catalog correction — Focus count

An earlier preparatory document listed 109 base Focus names because the Magic family contained only 24 entries. Current official public inventory evidence includes **Order Focus**, raising Magic to 25 and total base coverage to **110**.

This correction is safe at the public documentation layer. It does not convert the catalog into a `JAR 110/110` claim.

## Clean-room/provenance rule

Goety is a third-party provider and Black Arcana is clean-room. Public documentation may establish observable/player-facing contracts and semantic overlap. Source-derived implementation details may only become implementation-facing specifications when the exact source revision and license/provenance requirements are satisfied.

Because exact 3.1.4 source is not pinned here, Black Arcana must not invent or copy:

- class names;
- methods/signatures;
- registry internals;
- hidden costs/formulas;
- persistence internals;
- network packets;
- event hooks;
- servant ownership storage;
- ritual transaction internals.

## Exact-JAR validation options

Future exact-artifact validation must remain clean-room and purpose-limited. Acceptable evidence can include:

- published metadata/resources intentionally exposed in the JAR;
- public API surfaces shipped for integration;
- datapack/resource registries that are intended as data;
- runtime registry/query output exposed through supported tooling;
- controlled in-game observation with reproducible setup;
- upstream exact-source publication if it later becomes available.

Do not treat unauthorized decompilation as the default path merely to improve catalog completeness.

## Runtime QA priorities

### Resource/settlement

- identify a supported boundary for reading/checking/spending Soul Energy if Black Arcana ever needs direct integration;
- verify that one Goety cast settles exactly once under base and specialized Staff surfaces;
- verify cancellation/failure behavior before attempting any cross-provider transaction bridge.

### Servants

- prove owner identity and lifecycle through supported provider state;
- measure persistence/lifespan/cap rules relevant to planned Black Arcana binding/summon features;
- verify Summon Down behavior before any summon-cap/dedup decision relies on it;
- verify servant kill causality before RPG Mastery or external rewards consume it.

### Rituals

- prove provider completion event/state rather than inferring from visuals or ingredient removal;
- test cancellation/restart/partial-consumption cases;
- test protected-area/world-safety interaction only through real supported hooks.

### Progression

- validate research acquisition and downstream unlock reachability for content Black Arcana may reference;
- validate Lichdom state/lifecycle before treating it as a provider identity or transformation gate.

### Addons

- Goety Iron `3.1` must be audited separately;
- Goety Cataclysm `1.21.1-1.8.2` must be audited separately;
- addon effects must not be counted as base Goety registry coverage.

## Phase 3 disposition

Goety currently proves substantial semantic coverage in death/soul magic, necromancy, servants, summoning, elemental families, utility/control, rituals and witchcraft. That is sufficient to block naive duplicate design.

It is **not** sufficient to authorize exact integration code against unverified Goety internals. Any feature that depends on exact 3.1.4 hooks remains `FAIL-CLOSED / PENDING PROVIDER BOUNDARY` until the necessary surface is verified.
