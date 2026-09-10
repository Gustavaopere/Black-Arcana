# Goety 3.1.4 — Technical audit

Status: `OPEN CURRENT REGISTRY / EXACT 3.1.4 JAR-SOURCE RECONCILIATION PENDING / RUNTIME/API QA PENDING`

## Exact installed identity

Current physical modpack authority establishes:

- mod id: `goety`;
- JAR: `goety-3.1.4.jar`;
- runtime version: `3.1.4`;
- physical SHA-1: `a0770e180e4e8b1b87d8fa9c8356e9dbf34d82a7`;
- Minecraft: 1.21.1;
- loader: NeoForge `21.1.248`.

The current pack snapshot contains 612 top-level entries including NeoForge. Internal jarjar dependencies are not counted as top-level providers.

## Exact public release

The exact public release is CurseForge file `8689429`, released `2026-08-20` on the Release channel. The public project/release surface declares MIT.

That release identity is strong enough to pin **which distributed artifact/version the catalog targets**. It is not source-to-binary equivalence evidence, and the CurseForge license declaration must not be generalized over a source tree whose own license file defines mixed scopes.

## Public 1.21.1 source line

The prior statement that only historical `Goety-2` 1.20/1.19 source was public is stale. The public repository [`Vivideru/Goety-3`](https://github.com/Vivideru/Goety-3) is the 1.21.1+ source line.

Audited checkpoints:

| Checkpoint | Source metadata | Role in this audit |
|---|---|---|
| `4230e3bce2842779a6667ae6e5bfef8f53a27541` | Minecraft 1.21.1 / Goety 3.1.0 | earliest audited 3.1.x registry checkpoint |
| `6c41a04f2d712097c4461f969a6bb8ee277149ef` | Goety 3.1.1 | latest audited public source checkpoint |

No public checkpoint/tag matching distributed Goety `3.1.2` or the installed `3.1.4` has been established. The source line therefore cannot be promoted to `SOURCE-PINNED 3.1.4`.

Historical `1.20` code is not current 3.1.4 authority, and third-party 1.21.1 forks are not silently substituted for exact official 3.1.4 source. Implementation-facing claims that require exact class/method/registry/API evidence remain fail-closed.

## Focus registry evidence

Audited file:

`src/main/java/com/Polarice3/Goety/common/items/ModItems.java`

The file has identical blob SHA at both audited endpoints:

`db3c63b366803e2d46aa4a996b5bb0f358437a7f`

Read-only factual enumeration yields **123 active Focus item registrations**:

- Magic: 26
- Necromancy: 11
- Geomancy: 11
- Frost: 9
- Wild: 12
- Wind: 9
- Storm: 11
- Abyss: 9
- Nether: 11
- Void: 14

Total: **123**.

The legacy Wiki catalog contains 110 names. The 13 source-registered IDs omitted there are:

`illuminate_focus`, `earth_punch_focus`, `smack_stone_focus`, `ministrous_focus`, `carrion_focus`, `razor_wind_focus`, `surging_focus`, `sprightly_focus`, `thunderstorm_focus`, `water_whip_focus`, `hogging_focus`, `stellar_focus`, `void_flash_focus`.

Consequently, the Wiki list is not a complete registry authority for the public 1.21.1 source line.

## Historical catalog correction — Wiki Focus count

An earlier preparatory document listed 109 base Focus names because the Magic family contained only 24 entries. Public Wiki inventory evidence includes **Order Focus**, raising the legacy documentary Magic subset to 25 and its total base list to **110**.

That historical correction remains valid at the public-documentation layer. The new 123-entry source-registry evidence supersedes only the claim that 110 is a complete current registry; it does not erase the 109→110 correction and does not convert either count into an exact installed-JAR claim.

## What the registry evidence does and does not prove

It proves, for the audited public 3.1.0/3.1.1 source interval:

- the existence of 123 active Focus item registrations in the audited registry file;
- their category distribution;
- that at least 13 registry identities were missing from the prior 110-name Wiki inventory;
- blob stability of that registry file between the two audited source checkpoints.

It does **not** prove:

- that installed 3.1.4 has the same 123-entry registry;
- that every item registration is survival-reachable/player-facing as a distinct semantic action in 3.1.4;
- that there are exactly 123 semantic spells under Black Arcana's metric;
- exact 3.1.4 costs, cooldowns, damage, range, duration, targeting, settlement or networking behavior;
- a stable 3.1.4 integration API/event boundary;
- exact ritual identity totals from the 13 documented ritual categories.

Therefore the global semantic total remains **796** and Goety remains non-additive at this checkpoint.

## License and clean-room provenance

`Vivideru/Goety-3/LICENSE.txt` is mixed-license:

- original code under `src/main/java/com/Polarice3/` is stated as MIT;
- additions under `src/main/java/com/Vivideru/` are All Rights Reserved unless specifically stated otherwise.

The audited `ModItems.java` resides under `com/Polarice3`, so its factual registry identities/counts can be recorded under the observed MIT scope. That does not make the entire repository MIT.

Goety is a third-party provider and Black Arcana remains clean-room. Black Arcana uses the audited source read-only for factual catalog/provenance/deduplication evidence. No Goety implementation, assets, text, models or sounds are copied or adapted, and source inspection does not transfer Goety runtime authority to Black Arcana.

Because exact 3.1.4 source is not pinned here, Black Arcana must not invent or copy unverified implementation contracts such as:

- class names outside the explicitly audited factual path;
- methods/signatures;
- registry internals beyond the factual item registrations actually inspected;
- hidden costs/formulas;
- persistence internals;
- network packets;
- event hooks;
- servant ownership storage;
- ritual transaction internals.

## Evidence classes

| Claim class | Current state |
|---|---|
| installed JAR/version/hash | EXACT PHYSICAL |
| exact public 3.1.4 release identity | EXACT PUBLIC RELEASE |
| provider role: Soul Energy / Focus / ritual / servant / progression | VERIFIED FROM CURRENT PROJECT GUIDE + PUBLIC PROVIDER DOCS |
| public 1.21.1 source-line identity | VERIFIED |
| public source checkpoints | 3.1.0 + 3.1.1 VERIFIED |
| `ModItems.java` blob across audited checkpoints | STABLE / VERIFIED |
| 123 active Focus item registrations in audited public source | VERIFIED FACTUAL REGISTRY EVIDENCE |
| 110 Wiki names / 10 families | LEGACY PUBLIC DOCUMENTATION SUBSET |
| 12 public Wands/Staffs | PUBLIC DOCUMENTATION INVENTORY |
| 13 public ritual families/types | PUBLIC DOCUMENTATION INVENTORY; NOT DISCRETE RITUAL COUNT |
| 10 public research lines | PUBLIC DOCUMENTATION INVENTORY |
| exact 3.1.4 Focus registry | UNVERIFIED |
| exact 3.1.4 semantic Focus inventory | UNVERIFIED |
| exact 3.1.4 ritual identity inventory | UNVERIFIED |
| exact 3.1.4 per-Focus costs/cooldowns/damage/range | UNVERIFIED except separately documented cases |
| exact 3.1.4 stable integration API | UNVERIFIED |
| exact modpack runtime behavior | UNVERIFIED |

## Exact-JAR/source reconciliation requirement

The remaining decisive gate is the installed `goety-3.1.4.jar` versus an exact matching official source revision or another legitimate current registry/runtime evidence surface.

Future exact-artifact validation must remain clean-room and purpose-limited. Acceptable evidence can include:

- an upstream exact 3.1.4 source/tag if published;
- published metadata/resources intentionally exposed in the exact JAR;
- public API surfaces shipped for integration;
- datapack/resource registries that are intended as data;
- supported runtime registry/query output;
- controlled in-game observation with reproducible setup.

Do not silently extrapolate from 3.1.1 to 3.1.4. Do not treat unauthorized decompilation or copying as the default path merely to improve catalog completeness.

## Runtime QA priorities

### Resource/settlement

- identify a supported boundary for reading/checking/spending Soul Energy if Black Arcana ever needs direct integration;
- verify that one Goety cast settles exactly once under base and specialized Staff surfaces;
- verify cancellation/failure behavior before attempting any cross-provider transaction bridge.

### Focus reachability and semantic eligibility

- reconcile exact 3.1.4 Focus registry identity;
- determine player-facing/survival reachability for the 13 IDs newly exposed by source evidence;
- distinguish aliases, technical/support items or other non-additive identities before semantic counting;
- preserve one causal cast/action as one provider-owned semantic object.

### Servants

- prove owner identity and lifecycle through supported provider state;
- measure persistence/lifespan/cap rules relevant to planned Black Arcana binding/summon features;
- verify Summon Down behavior before any summon-cap/dedup decision relies on it;
- verify servant kill causality before RPG Mastery or external rewards consume it.

### Rituals

- enumerate discrete ritual identities rather than treating 13 ritual categories as 13 rites;
- prove provider completion event/state rather than inferring from visuals or ingredient removal;
- test cancellation/restart/partial-consumption cases;
- test protected-area/world-safety interaction only through real supported hooks;
- preserve Goety settlement and Black Arcana `WorldEffectPolicy` boundaries rather than creating a second destructive-effect pipeline.

### Progression

- validate research acquisition and downstream unlock reachability for content Black Arcana may reference;
- validate Lichdom state/lifecycle before treating it as a provider identity or transformation gate.

### Addons

- Goety Iron `3.1` must be audited separately;
- Goety Cataclysm `1.21.1-1.8.2` must be audited separately;
- addon Focuses/effects must not be counted as base Goety registry coverage.

## Phase 3 disposition

Goety currently proves substantial provider coverage in death/soul magic, necromancy, servants, summoning, elemental families, utility/control, rituals and witchcraft. That is sufficient to block naive duplicate design.

It is **not** sufficient to authorize exact integration code against unverified 3.1.4 internals. Any feature that depends on exact Goety hooks remains `FAIL-CLOSED / PENDING PROVIDER BOUNDARY` until the necessary current surface is verified.

Canonical provider state after this reconciliation:

`OPEN CURRENT REGISTRY / EXACT 3.1.4 JAR-SOURCE RECONCILIATION PENDING`.
