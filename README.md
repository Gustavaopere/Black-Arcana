# Black Arcana

Black Arcana is a **Minecraft 1.21.1 / NeoForge 21.1.248 / Java 21** forbidden-magic framework and content mod built around server-authoritative casting, bounded power, explicit consequences, ritual preparation and optional integration with the existing magic/RPG ecosystem.

Its design goal is not to create another unlimited-power spell mod. Dangerous magic can remain spectacular, but every high-impact mechanic must have explicit costs, cooldowns, progression gates, world-safety rules and—where appropriate—**Arcane Backlash, Strain and Corruption**.

Black Arcana is a clean-room project. Mahou Tsukai and other mods may be studied through public documentation and observable gameplay, but their code, assets, text, models, sounds and implementation details are not automatically reusable source material.

## Current implementation on `main`

The canonical implementation status is tracked in [`plans/STATUS.md`](plans/STATUS.md). At the current `main` checkpoint:

- **00 Foundation — complete.** Reproducible build/CI, clean-room provenance rules, domain contracts and data/config boundaries.
- **01 Reference Catalog — complete.** 53 reference mechanics classified (`KEEP`, `REIMAGINE`, `MERGE`, `DROP`, `DEFER`), original Black Arcana identity defined, 32 implementation-facing candidates specified, and safety/balance/host-capability audits frozen.
- **02 Arcana Core — complete.** Server-authoritative cast kernel, transactional costs, targeting/effects, channels, cooldowns/charges, persistence, networking and atomic data reload.
- **03 Integration Layer — complete.** Provider/adaptor boundaries for Iron's, Ars Nouveau, Eidolon: Repraised, Malum and RPG progression are frozen behind Black Arcana-owned interfaces.
- **04 World Safety — complete.** Hierarchical destructive-effect policy, per-cast/global budgets, loaded-chunk-only mutation, temporary-block rollback/restart safety, PvP/boss/protection facts and claim extension points.
- **05 Casting & UX — code merged; manual client closure pending.** Direct casting, loadouts/radial/contextual feedback and client configuration are implemented, but the required real-client visual/input matrix remains the formal closure gate.
- **05A Arcane Danger — active.** Core danger, Arcane/Corruption Resistance, Strain and Backlash contracts are substantially implemented; zero-resistance 1:1 backlash for the canonical linear profile is verified. Equipment/provider work has advanced, while the remaining exact closure scope is tracked in `plans/STATUS.md`.
- **06 Rituals — advanced preparatory work exists, not canonical yet.** Promotion remains causally downstream of Stage 05 closure and the frozen 05A contracts.
- **07 Spell Domains — preparatory/stacked work exists, not canonical yet.** Domain implementation must not bypass the Stage 05/05A/06 promotion order.
- **08 Progression & Balance — planned/preparatory.** Final power budgets, mastery/attribute gates, diminishing returns and exploit controls.
- **09 Hardening & Release — planned.** Compatibility, profiling, multiplayer abuse, persistence upgrades and provenance/license release audit.

Planned or stacked downstream work is deliberately distinguished from features already canonical on `main`.

## Core casting architecture

Black Arcana owns a single canonical server execution path for immediate and channelled magic. The client may request/present a cast, but the server owns validation and settlement.

The merged core includes:

- unique cast identities and bounded replay protection;
- server-owned spell/loadout validation;
- immediate and channelled casts converging on one pipeline;
- transactional `check -> reserve -> effect -> commit/refund` resource handling;
- atomic composite costs across multiple providers;
- bounded server-fact target validation and follow-up work scheduling;
- persistent/shared cooldowns and reusable charge pools;
- migration/pruning of persisted state;
- versioned bounded C2S/S2C networking;
- strict atomic datapack reload for data-driven definitions/presentation metadata.

A synthetic Black Arcana spell can execute without requiring any optional magic mod.

## Casting & UX

The intended player workflow avoids a universal staff requirement and avoids adding a permanent duplicate mana HUD when an existing resource provider already owns that concept.

Stage 05 provides/targets:

- direct input and spell loadouts;
- fast radial selection;
- contextual cast/preflight feedback;
- readable failure reasons;
- client accessibility/configuration;
- server-authoritative validation regardless of client UI.

The current code is merged, but Stage 05 remains formally open until its real-client visual/input QA matrix is executed.

## Arcane Danger: power has consequences

Stage 05A makes forbidden magic dangerous independently of ordinary mana/cooldown balancing.

A character may attempt magic before being properly prepared. The spell can still succeed, but insufficient protection can produce:

- **Arcane Backlash** — terminal self-harm derived from eligible confirmed spell damage;
- **Arcane Strain** — persistent/recovery-aware pressure against repeated dangerous casting;
- **Corruption** — a separate persistent consequence channel;
- buildcraft requirements through armor, items, Curios, buffs, rituals, RPG providers and other registered resistance sources.

For the canonical linear dangerous profile:

```text
effective Arcane Resistance = 0
-> 100% of eligible confirmed damage becomes Arcane Backlash
```

Arcane Backlash is its own Black Arcana damage family. It does not recurse, crit, lifesteal, award normal offensive mastery or start ordinary on-hit proc chains.

### Resistance model

The initial Arcane Resistance curve is:

```text
residualBacklash(R) = K / (K + clamp(R, 0, R_MAX))
```

with initial defaults `K = 40` and `R_MAX = 240`. Corruption Resistance is a different channel with its own providers/caps.

Dangerous casts snapshot resistance/provider facts before effects can deal eligible delayed damage, preventing gear/perk swapping after cast commitment from retroactively evading risk.

## World safety

Every dangerous world effect is constrained by Black Arcana's shared safety layer rather than each spell inventing ad-hoc grief rules.

The canonical policy supports escalating modes such as:

- `OFF`
- `COSMETIC`
- `TEMPORARY`
- `LIMITED`
- `FULL`

while still enforcing hard ceilings, loaded-chunk-only execution and bounded scheduler work.

Temporary world mutations are transactionally owned, persisted when required and restored with compare-and-set semantics so later player/third-party edits are not overwritten blindly. PvP, team, boss, invulnerability and protected-area facts are server-derived inputs to the same policy.

## Optional integration philosophy

Black Arcana owns cross-cutting safety, transactions, persistent identities, hazards and fallback execution. Host mods remain authorities only for systems they genuinely expose.

- **Iron's Spells 'n Spellbooks 3.16.3:** preferred host/API for active spell lifecycle and optional mana/spell attributes when appropriate.
- **Ars Nouveau 5.13.0 baseline:** composable utility/teleport/familiar ecosystem; Black Arcana avoids duplicating generic Blink/Warp/familiar ownership and focuses on genuinely forbidden variants.
- **Eidolon: Repraised 0.5.0.2:** occult/ritual thematic host where supported extension points can express the contract.
- **Malum 1.8.2:** spirit/soul economy and current Spirit Rite model where supported.
- **RPG Skill Tree:** attributes, mastery and perk gates through a provider boundary; it is not the Black Arcana cast engine.
- **Curios 9.5.1+1.21.1:** optional snapshot-only equipment/resistance contributions; no global per-tick Curios scan.

Optional providers must fail safely when absent or incompatible. The core does not leak host implementation classes across its domain boundaries.

## Rituals — roadmap

Rituals are reserved for meaningful occult preparation rather than routine combat casting. Planned uses include:

- permanent knowledge unlocks;
- soul contracts and bargains;
- rare transformations;
- domain creation/upgrades;
- high-impact grand world effects;
- Eidolon-backed occult rites where a verified extension seam exists;
- Malum spirit components where the current 1.8.x model supports them;
- native Black Arcana grand rituals for gaps that external APIs cannot safely express.

Ritual execution must remain transactional, recoverable and subject to progression/world-safety/hazard contracts.

## Spell domains — roadmap

The approved design catalog is organized into:

- **Blood & Curses**
- **Souls & Death**
- **Projection & Arsenal**
- **Space & Displacement**
- **Black Flame**
- **Forbidden Domains**
- **Familiars & Divination**

Every spell specification must define fantasy, invocation/targeting, host integration, cost, cooldown, scaling, progression gate, danger profile, world-effect mode, boss/PvP behavior, configuration, tests and provenance. A thematic idea does not enter production without those contracts.

## Progression & balance — roadmap

Final balance is designed around knowledge/unlocks, RPG attributes/masteries, quantitative tier budgets, caps/diminishing returns and exploit controls rather than endless mana-cap grinding. Server presets will include conservative defaults suitable for the target large modpack.

## Toolchain and build

- Minecraft 1.21.1
- NeoForge 21.1.248
- Java 21
- ModDevGradle 2.0.144

```bash
./gradlew test
./gradlew build
```

CI includes the applicable JUnit suite, NeoForge build/JAR inspection, GameTests and dedicated-server smoke.

## Plans and project memory

The complete design/engineering roadmap lives under [`plans/`](plans/README.md). Implementation sessions should read:

1. [`plans/README.md`](plans/README.md)
2. [`plans/STATUS.md`](plans/STATUS.md)
3. [`plans/DECISIONS.md`](plans/DECISIONS.md)
4. the active stage/task documents.

Reference classification and host-capability evidence lives under [`docs/reference/`](docs/reference/README.md).

## License and clean-room provenance

Black Arcana is currently distributed as **All Rights Reserved**; see [`LICENSE`](LICENSE).

Third-party references/dependencies are indexed in [`SOURCES.md`](SOURCES.md) and governed by [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). The release hardening plan contains a fail-closed provenance/license audit.

No entry in a reference catalog, compatibility matrix or source link authorizes copying third-party code or assets. Substantial derivation requires an exact source revision, file-level mapping and a license/permission that permits the intended public distribution.