# 07A.05 — Mahou Reference Disposition & Provider Routing

## State

`PLANNED / REFERENCE ROUTING ONLY / NOT IMPLEMENTED`

## Objective

Convert the complete latest Mahou 1.21.1 reference identity inventory into explicit Black Arcana dispositions without importing Mahou's system, item progression, recipes or assets.

Canonical identity inventory: `docs/reference/mahou-v1.36.28-structural-catalog.md`.

## Routing rules

Every reference concept receives one of:

- `REUSE_EXISTING_BA` — an existing Black Arcana mechanic already covers the fantasy; extend/specify it rather than duplicate it;
- `BA_NATIVE_NEW` — implement original Black Arcana semantics through canonical runtime;
- `PROVIDER_HOSTED_BA_AUTHORITY` — provider supplies invocation/presentation/resource surface but Black Arcana owns dangerous semantics;
- `PROVIDER_NATIVE_FIRST` — provider already expresses the fantasy safely; do not rebuild it in Black Arcana unless a distinct Black Arcana requirement exists;
- `RITUAL_UNLOCK` — high-impact/permanent effect belongs in Stage 06 ritual orchestration;
- `DROP_OR_MERGE` — reference mechanic does not justify distinct content;
- `PENDING_BEHAVIOR_PROVENANCE` — identity is proven by exact artifact, but behavior must be established from public/observable evidence before any implementation.

## Provider roles

### Iron's Spells 'n Spellbooks 3.16.3

Preferred host for fixed active combat spells where the existing exact-version Black Arcana adapter can preserve server authority, resource transaction, target validation, cooldown, hazard and causality.

Candidate families: fixed projectiles, barriers, combat displacement, high-telegraph destructive casts and other discrete active spells.

### Ars Nouveau 5.13.1

Provider-native first for modular utility/elemental/compositional magic already expressible by glyphs/augments. 07A must not mirror the Ars grammar.

Candidate use: elemental aspects for approved fusion only if an exact adapter can preserve the required semantic identity. Otherwise use Ars natively outside Black Arcana fusion or implement an original bounded Black Arcana semantic effect.

### Eidolon: Repraised 0.5.0.2

Preferred occult ritual presentation for stationary circles, bargains, wards and permanent/high-preparation unlocks when exact callback identity is sufficient.

Black Arcana Stage 06 still owns authoritative ritual sessions/completion for Black Arcana mechanics. Player-specific rewards remain fail-closed when Eidolon cannot prove the caster/session.

### Malum 1.8.2

Preferred source for spirits/spirit costs and spirit-flavored ritual materials through the verified adapter. Malum does not become Black Arcana's cast engine or generic ritual authority.

### Goety 3.1.4

Potential provider for summon/minion presentation only where exact ownership/lifecycle contracts are sufficient. Similar necromantic theme is not enough to bridge.

### RPG Skill Tree

Progression/gating only through real query contracts. No cast, ritual, hazard or resource authority transfers to the RPG project.

## High-impact dispositions

### Drain Life

`REUSE_EXISTING_BA` -> Stage 07.01 `Sanguine Harvest`; 07.08 for blood reserve/Vampirism composition. Non-consensual drain is Umbral.

### Death Collection / death avoidance

`REUSE_EXISTING_BA` -> Stage 07.02 Mortal Ledger / Soul Anchor family. The Ankh of Continuance is a new presentation/ritual focus over this single authority.

### Reality Marble / bounded domain arena

`REUSE_EXISTING_BA` -> Stage 07.06 Forbidden Domains. Do not create dimensions by default; D032 remains authoritative.

### Black Flame

`REUSE_EXISTING_BA` -> Stage 07.05 Black Flame. Do not recreate Mahou's implementation/presentation.

### Familiar sight / astral viewing

`REUSE_EXISTING_BA` -> Stage 07.07 Noetic/Borrowed Sight/Astral Severance contracts after that domain is complete.

### Fallen Down

`PROVIDER_HOSTED_BA_AUTHORITY + RITUAL_UNLOCK` -> original **Ruinous Zenith** concept. Stage 06 unlock/preparation, Iron's preferred active presentation if safe, Black Arcana owns target/damage/world/hazard semantics.

### Geas / coercive contract

`BA_NATIVE_NEW + RITUAL_UNLOCK` only after public behavior provenance and exact agency/consent rules are specified. Coercive variants are Umbral and require strict PvP/player-agency policy.

### Probability Alter

`PENDING_BEHAVIOR_PROVENANCE`; if adopted, must use bounded deterministic probability hooks rather than global RNG manipulation or broad provider mixins.

### Selective Displacement

Likely `REUSE_EXISTING_BA` through Stage 07.04 if the verified observable behavior maps cleanly. No new displacement engine.

## Ritual conversion rules

Circle-based preparation from the reference does not imply copying its drawing/input system.

For adopted grand/ritual concepts:

- use Black Arcana Stage 06 ritual sessions;
- use original local sigils/geometry;
- use placed provider-native ingredients/resources where appropriate;
- do not require self-cutting;
- do not reproduce Mahou recipes;
- do not require Mahou scrolls/staves;
- preserve exactly-once completion/replay semantics;
- all world mutation goes through `WorldEffectPolicy`.

## Item-bound reference mechanics

The exact artifact also contains behavior-bearing item identities such as Caliburn, Clarent, Morgan, Rhongomyniad, Ripper, Replica, Rule Breaker, William-related content and multiple staves/mystic codes.

These are **reference inventory only**. 07A does not import those items, recipes, names or assets. If a distinct observable mechanic is valuable, it must receive a separate public/observable behavior specification and then be re-expressed as an original spell, ritual, progression mechanic or dropped/merged.

## Gate before implementation

No row may leave `PENDING_BEHAVIOR_PROVENANCE` solely because a class/field/localization key exists in the exact artifact. Structural identity proves presence, not behavior.

For every adopted mechanic record:

- public/observable behavior source;
- original Black Arcana name;
- chosen canonical domain/capability;
- provider host/resource if any;
- polarity/source semantics;
- cost/cooldown/target/scaling/progression/world/boss-PvP/config/test contracts;
- provenance and license boundary.

## Acceptance

- every exact circle/reference identity has a disposition;
- no adopted row requires Mahou runtime/content files;
- existing Black Arcana mechanics are reused instead of duplicated;
- provider routing is exact-version-gated and fail-closed;
- no protected reference asset/text/name is needed to understand the implementation spec.
