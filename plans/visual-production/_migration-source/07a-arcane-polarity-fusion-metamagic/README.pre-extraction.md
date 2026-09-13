# 07A — Arcane Polarity, Fusion & Metamagic

## State

`PLANNED / NOT IMPLEMENTED / SEQUENCED AFTER STAGE 07`

This stage is a cross-domain layer inserted between Stage 07 and Stage 08. It does not add an eighth spell domain and does not make any runtime described here canonical merely because this plan exists.

Planning baseline: `main@2449f4c2d472a9c93d783a701a94933c1f9320f3`.

Stage 07.07 is still incomplete and 07.08 is planned after it. Stage 07A may begin implementation only after Stage 07 is canonical through 07.08, or after an explicit reviewed rescope says which Stage 07 contracts are no longer prerequisites.

## Goal

Add a coherent semantic layer for **white / black / neutral arcana**, bounded **spell fusion**, and **metamagic** while preserving Black Arcana's single canonical cast/ritual/hazard/world-safety authority.

The stage also closes the current Mahou Tsukai reference gap by cataloguing the latest Minecraft 1.21.1 artifact as reference-only and routing selected observable fantasies into the installed providers that best fit them without importing Mahou's mana-growth system, recipes, scrolls, staves, self-cutting activation, code, assets, models, sounds or implementation.

## Non-goals

- no Mahou dependency;
- no Mahou mana-growth or blood-circle activation system;
- no copy of Mahou recipes, scrolls, staves, textures, models, animations, sounds, text or binary assets;
- no second cast pipeline, cooldown ledger, replay identity, resource reservation system, ritual engine, corruption state, strain state or world-effect policy;
- no generic clone of Ars Nouveau's glyph grammar or native augments;
- no assumption that thematic similarity implies a provider bridge;
- no RPG Skill Tree ownership of Black Arcana magic runtime;
- no arbitrary spell combinator that can bypass target, cost, hazard, world-safety or progression contracts;
- no remote-URL sigil/projector feature in the first implementation.

## Required predecessors

Implementation must start from a fresh synchronized `main` and re-read:

- `plans/STATUS.md`;
- `plans/DECISIONS.md`;
- `plans/06-rituals/README.md`;
- `plans/07-spell-domains/README.md` and all canonical 07 domain specifications;
- `plans/07-spell-domains/08-hematic-reservoirs-vampiric-sustenance.md` once implemented/rescoped;
- current provider audit evidence for Iron's Spells, Ars Nouveau, Eidolon: Repraised, Malum, Goety and RPG Skill Tree;
- `SOURCES.md`, `THIRD_PARTY_NOTICES.md` and the latest Mahou reference catalog.

## Architectural authority

### Black Arcana owns

- the polarity classification contract and its server-side derivation;
- fusion admission, fusion semantics and the final resolved Black Arcana cast specification;
- metamagic admission, compatibility, hazard deltas and canonical cast-plan transformation;
- ritual completion, unlock identity, persistence, replay protection and resurrection semantics;
- `WorldEffectPolicy`, Arcane Danger, Corruption, Strain and Backlash;
- original sigil metadata and any Black Arcana-native presentation protocol;
- all fail-closed decisions when an external provider cannot prove the required hook.

### Providers keep their authority

- **Iron's Spells 'n Spellbooks** — provider-native mana, schools, ordinary spell host behavior and presentation where the exact adapter contract is proven;
- **Ars Nouveau** — its mana/Source/glyph/augment grammar and native compositional casting;
- **Eidolon: Repraised** — its own altar/ritual/theurgy content and presentation where a safe exact-version callback exists;
- **Malum** — spirits and spirit-arcana resources where the exact bridge is proven;
- **Goety** — Soul Energy/minion semantics where an explicit bridge is selected and proven;
- **Vampirism** — vampire identity, thirst/player-blood state and native feeding, as already constrained by 07.08;
- **RPG Skill Tree** — progression/query/gates only through real contracts; it never executes Black Arcana spell runtime.

Provider presentation does not transfer semantic authority. A spell visually hosted by Iron's or a ritual visually hosted by Eidolon still executes Black Arcana-owned dangerous semantics through the canonical Black Arcana pipeline when the mechanic belongs to Black Arcana.

## Polarity model

White and black magic are **not damage schools**.

The classification is derived from how power is sourced and whose agency is consumed:

- `LUMINAL` / white — self-owned power, explicitly consensual transfer, restorative/warding use of owned resources, or bounded ambient use that does not parasitize a living/soul/agency owner;
- `UMBRAL` / black — non-consensual extraction of life, soul, mana/resource, agency, identity or world-state; coercive contracts; parasitic transfer; forced sacrifice; theft-backed empowerment;
- `ARCANE` / neutral — manipulation whose source/agency is not intrinsically extractive, such as many elemental, projective, spatial or informational effects.

Polarity is distinct from **danger/forbidden severity**. A Luminal resurrection can still be forbidden/high-danger because it manipulates death and persistence. An Umbral life drain can be low-area but still black because its power source is stolen life.

The same broad fantasy may resolve to different polarity based on validated consent/source. Example: a bounded voluntary life transfer may be Luminal or neutral; the same transfer forcibly siphoned from an unwilling entity is Umbral.

Polarity is metadata/gating/presentation plus an input to canonical hazard policy where explicitly specified. It must never create a second Corruption/Strain system.

## White and black identity surfaces

### Umbral Codex

The user's shorthand `Darkhold` is a useful design role but is not adopted as player-facing identity. The planned original Black Arcana surface is the **Umbral Codex**: a knowledge/progression/grimoire surface for extractive techniques, bargains, consequences and forbidden lore.

The Codex is not a resource pool and not a second cast engine. Unlocks remain server-owned and Stage 08 determines final progression/balance gates.

### Ankh of Continuance

The planned **Ankh of Continuance** is a ritual focus/presentation surface for the existing Souls & Death resurrection authority. It must compose with the canonical Mortal Ledger / Soul Anchor semantics rather than introduce a second resurrection system.

Self/consensual anchoring is Luminal by default, but resurrection remains high-danger and charge-bounded. Exact item/block form, refill cost and progression gate are Stage 08 inputs.

Eidolon may present the ritual only when the exact installed integration can prove caster/session identity. If its callback cannot do that, Black Arcana's Stage 06 ritual engine remains authoritative and the Eidolon-specific path stays fail-closed.

## Blood theft and vampiric composition

Black life stealing does not create a new spell if Stage 07.01 already supplies the mechanic. `Sanguine Harvest` is the canonical starting point for non-consensual bounded life drain and is classified Umbral when it steals from unwilling targets.

Stage 07.08 remains authoritative for Hematic Reserve and Vampirism composition. Stage 07A must not create a competing blood storage or feeding economy. Any metamagic that redirects cost into stolen blood must use the 07.01/07.08 resource contracts and preserve thirst-first accounting for vampires.

## Fusion model

Fusion is a **bounded semantic composition layer**, not arbitrary nested casting.

A fusion definition combines one admitted base capability with one admitted aspect/reaction. The server resolves the composition before cost reservation into **one canonical cast plan** with:

- one `ArcanaCastId`;
- one replay claim;
- one authoritative target resolution;
- one composite resource reservation/commit path;
- one canonical cooldown decision;
- one hazard preflight/commit path;
- one world-safety admission;
- one progression/reward causality identity.

A fused spell must not execute child casts that independently spend cost, start cooldown, award progress, trigger normal offensive proc chains or bypass WorldEffectPolicy.

Planned first-class examples are intentionally bounded, such as a tendril/control capability infused with fire, frost or blood only when provider catalogs prove a safe source for those aspects. The fusion system must use allowlists/conflict rules rather than allowing every spell to combine with every effect.

Ars Nouveau already owns a native glyph/augment grammar. Black Arcana fusion must not reimplement Amplify/AOE/Extend/Pierce/Split. When an Ars-hosted spell already expresses a combination natively and safely, provider-native composition wins. Black Arcana fusion is for cross-domain semantics that must still pass Black Arcana danger/world-safety contracts.

## Metamagic model

Metamagic changes how an admitted Black Arcana cast is resolved without creating another spell engine.

Initial planned doctrines:

- **Overchannel** — bounded potency/duration increase with sharply increased canonical Strain/Corruption and hard caps;
- **Concentrate** — trade area/target count for precision or bounded potency;
- **Sanctify** — where a spell contract allows it, replace extractive sourcing with self-owned/consensual sourcing at higher cost/slower execution; polarity changes only if the entire resolved source graph qualifies;
- **Predation** — permit explicit eligible external life/blood sourcing; always Umbral, heavily gated, target/consent checked, and routed through canonical blood/resource contracts;
- **Echo** — one bounded delayed re-resolution inside the original causal cast/session; it must not become a second reward/cost/proc identity;
- **Anchor** — trade mobility for a more stable bounded channel/field where the spell contract permits it.

Every metamagic requires an allowlist, mutual-exclusion rules, hard numeric caps, a resource/hazard transformation, progression gate and deterministic tests. Unsupported provider semantics fail closed.

## Ritual and provider routing philosophy

Do not send every Mahou circle to Eidolon. Route by behavior:

1. stationary wards/fields -> Black Arcana field/domain runtime; Eidolon may supply occult presentation;
2. grand/high-preparation effects -> Stage 06 Black Arcana Grand Ritual; Eidolon presentation only if safe;
3. bargains/contracts/unlocks -> Black Arcana ritual completion with optional Eidolon surface;
4. soul/spirit costs -> Malum resources only through verified adapter contracts;
5. fixed active combat spells -> Iron's preferred presentation/host where the exact adapter remains proven;
6. modular elemental/utility composition -> Ars provider-native first where its glyph system already expresses the fantasy;
7. summons/minions -> Goety or other installed provider only when ownership/lifecycle hooks are sufficient; otherwise Black Arcana-native bounded runtime or fail closed.

No route may require Mahou recipes, Mahou staves, Mahou scrolls or self-cutting. Ritual setup uses original Black Arcana sigils plus provider-native materials/resources where appropriate.

## High-power reference: Ruinous Zenith

The destructive ray/sky-strike fantasy referenced from Mahou's `Fallen Down` is reimagined as **Ruinous Zenith**; the reference name is documentation-only.

Preferred architecture:

- Black Arcana owns unlock identity, danger profile, targeting, damage/world-effect semantics, replay protection and caps;
- Stage 06 Grand Ritual performs the permanent/high-preparation unlock;
- Eidolon or Malum may provide ritual presentation/material language where exact adapters are safe; neither becomes runtime authority;
- Iron's is the preferred active casting/presentation host if the exact 3.16.3 adapter can preserve one canonical Black Arcana cast transaction;
- RPG Skill Tree may provide level/mastery/perk gates only through a real read-only contract;
- long server-owned telegraph/channel, high atomic provider cost, long cooldown, severe canonical Strain/Corruption, bounded range/area/duration and boss/PvP caps are mandatory;
- destructive world behavior always passes `WorldEffectPolicy` and defaults to safe/limited modes unless server policy explicitly permits more;
- no global scans, no force-loaded impact area, no unbounded beam duration and no per-tick reward/proc farming.

Exact numbers belong to Stage 08 after deterministic performance evidence.

## Sigil and ritual presentation layer

Create an original **Arcane Sigil Presentation Layer** with local data-driven geometry/palette/animation metadata. It is presentation only: the client renders a server-authored ritual/cast state and never determines ritual success.

The layer may be reused by Black Arcana rituals, compatible Eidolon-hosted surfaces and Iron's telegraphs. Ars integration is optional and requires a verified hook.

All geometry, textures, shaders, particles, sounds and animations must be original or separately licensed. Mahou's projector/mandala assets are not copied. Remote arbitrary image URLs are out of scope for the first implementation.

## Mahou 1.21.1 reference baseline

The latest verified Minecraft 1.21.1 build at planning time is `mahoutsukai-1.21.1-v1.36.28.jar` (CurseForge project 342543, file 8860405). It is **not installed in the physical modlist** and is reference-only.

A clean-room exact-artifact structural audit was run on isolated branch `audit/mahou-1.21.1-v1.36.28-exact-artifact` and is intentionally non-merge. The audited artifact hashes are:

- SHA-1 `9049114ceea69d35e7469838f5a23d2655ebf133`;
- SHA-256 `0f79fcf98680fdba8d4bb96e85f2d715bdd22dfa67906712d8181a99dc075a43`.

The evidence retained only metadata facts, class/resource identities, localization keys, serializer names, signatures and counts. It retained no implementation bodies, recipe ingredients, localization prose, textures, models, animations, sounds or reconstructed source.

See `docs/reference/mahou-v1.36.28-structural-catalog.md` for the complete 53 circle/reference identities observed in that exact artifact and their Black Arcana dispositions.

## Work packages

1. `01-polarity-source-agency.md` — freeze polarity/source/consent semantics and migration of existing spell metadata.
2. `02-white-black-surfaces.md` — Umbral Codex, Ankh of Continuance, life-drain/resurrection composition.
3. `03-spell-fusion.md` — bounded fusion data/runtime contract and single-transaction resolution.
4. `04-metamagic.md` — metamagic allowlists, transformations, hazards and anti-proc rules.
5. `05-mahou-disposition-provider-routing.md` — complete latest Mahou reference disposition and provider-native routing.
6. `06-sigils-ritual-presentation.md` — original sigil/mandala presentation and ritual UX.
7. `07-provider-contract-verification.md` — exact-version API/JAR gates and fail-closed adapters.
8. `08-hardening-stage08-handoff.md` — exhaustive deterministic/integration tests and balance handoff.

## TDD / implementation order

For each package:

1. synchronize with the latest `origin/main` and record its SHA;
2. write contract tests first and observe RED for the missing behavior;
3. implement the minimal server-authoritative behavior to GREEN;
4. add GameTests/integration tests for world/entity/provider cases;
5. run NeoForge build, unit tests, GameTests and dedicated-server smoke as applicable;
6. re-fetch `origin/main`, reconcile concurrent changes semantically and rerun every relevant gate on the reconciled HEAD;
7. only then promote the package or Stage state.

## Stage acceptance

Stage 07A may become canonical only when all of the following are proven:

- polarity is server-derived and cannot be client-forged;
- existing Stage 07 spells have explicit polarity disposition without changing unrelated runtime semantics;
- fusion and metamagic enter one canonical cast transaction and cannot double-charge, double-cooldown, double-reward or create normal proc chains from child effects;
- no fusion/metamagic path bypasses `WorldEffectPolicy`, target caps, `BoundedWorkScheduler`, Arcane Danger or replay protection;
- Luminal/Umbral classification and forbidden severity remain independent dimensions;
- Sanguine Harvest/Hematic Reserve/Vampirism composition has no duplicate life/blood accounting;
- Ankh uses the single canonical Soul Anchor/Mortal Ledger authority;
- exact provider integrations are proven for the physically installed versions or remain explicitly fail-closed;
- the 1.21.1 v1.36.28 Mahou reference catalog is complete at the identity level and every adopted behavior has separate public/observable provenance before implementation;
- no Mahou protected asset or implementation is shipped;
- original sigil presentation is read-only/client presentation over server-authored state;
- all deterministic tests, GameTests, build, JAR inspection and dedicated-server smoke are green on the final reconciled HEAD;
- Stage 08 receives bounded formulas/config surfaces to tune, not unresolved architectural ownership questions.
