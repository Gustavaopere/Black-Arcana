# 07A — Arcane Polarity, Fusion & Metamagic

## State

`PLANNED / NOT IMPLEMENTED / SEQUENCED AFTER STAGE 07`

07A is a cross-domain semantic/runtime layer between Stage 07 and Stage 08. It is not an eighth spell domain. Stage 07 must first be canonical through 07.08 unless an explicit reviewed rescope changes that prerequisite.

Planning baseline recorded by the original plan: `main@2449f4c2d472a9c93d783a701a94933c1f9320f3`. Implementation must always resynchronize to then-current `main`.

## Goal

Add server-derived Luminal/Umbral/Arcane polarity, bounded spell fusion and bounded metamagic while preserving one canonical Black Arcana cast/ritual/hazard/world-safety authority. The Mahou 1.21.1 reference remains clean-room/reference-only; no Mahou dependency, mana-growth system, recipes, scrolls, staves, self-cutting activation, code or assets are imported.

## Runtime authority

Black Arcana owns polarity derivation, fusion admission/resolution, metamagic admission/transformation, ritual completion/unlock identity, persistence/replay protection, `WorldEffectPolicy`, Arcane Danger and fail-closed provider decisions.

Providers retain their own native resources/grammar/presentation/runtime where applicable: Iron's ordinary host behavior/mana, Ars Source/glyph grammar, Eidolon rituals/theurgy, Malum spirits, Goety minions, Vampirism vampire/thirst/feeding and RPG Skill Tree progression queries. Provider hosting/presentation never transfers Black Arcana dangerous-semantic authority.

## Semantic model

Polarity is derived from source/agency rather than damage type or color:

- Luminal: self-owned/proven-consensual/restorative or bounded non-parasitic sourcing;
- Umbral: non-consensual extraction of life, blood, soul, agency, identity or world-state;
- Arcane: neutral manipulation without inherently extractive sourcing.

Polarity is independent from forbidden/danger severity and does not replace Corruption/Strain. Detailed contract: `01-polarity-source-agency.md`.

Umbral Codex and Ankh of Continuance are semantic/access identities over canonical progression/ritual/Soul Anchor authority, not new engines. Detailed runtime contract: `02-white-black-surfaces.md`. Concrete palettes/motifs/UI/art direction are separate at `plans/visual-production/07a-arcane-polarity-fusion-metamagic/02-white-black-identity-presentation.md`.

## Fusion and metamagic

Fusion resolves admitted base+aspect semantics into one canonical cast transaction with one cast identity, target resolution, composite resource transaction, cooldown, hazard/world admission and reward causality. It is not arbitrary child casting or an Ars glyph clone. See `03-spell-fusion.md`.

Metamagic is opt-in bounded transformation over an admitted cast specification. Overchannel, Concentrate, Sanctify, Predation, Echo and Anchor are planned doctrines subject to per-spell allowlists, hard caps, hazard/resource transformations, causality and provider support. See `04-metamagic.md`.

## Provider/reference routing

`05-mahou-disposition-provider-routing.md` owns clean-room reference disposition and provider-native-first routing. Exact provider hooks must pass `07-provider-contract-verification.md`; thematic similarity never authorizes a bridge.

Ruinous Zenith remains a high-power reference-derived original concept whose unlock/target/damage/world/hazard semantics are Black Arcana-owned; provider presentation is optional/exact-version gated. Exact quantitative tuning belongs Stage 08.

## Presentation lane

Concrete sigil/mandala geometry, palette, animation, textures, shaders, particles, sounds, accessibility and ritual telegraph presentation were extracted from this stage overview. Canonical presentation planning lives at:

- `plans/visual-production/07a-arcane-polarity-fusion-metamagic/02-white-black-identity-presentation.md`;
- `plans/visual-production/07a-arcane-polarity-fusion-metamagic/06-sigils-ritual-presentation.md`.

The numbered `06-sigils-ritual-presentation.md` now retains only server-authored ritual/presentation payload safety, material settlement and provider-authority boundaries. A client may render server-authored presentation state; it never determines ritual success or polarity.

## Mahou reference baseline

The planning audit used `mahoutsukai-1.21.1-v1.36.28.jar` as a non-installed reference-only artifact and retained structural/provenance evidence in `docs/reference/mahou-v1.36.28-structural-catalog.md`. Protected implementation bodies, localization prose, recipes and assets are not implementation inputs.

## Work packages

1. `01-polarity-source-agency.md` — polarity/source/consent semantics.
2. `02-white-black-surfaces.md` — semantic/access surfaces and existing-mechanic composition.
3. `03-spell-fusion.md` — bounded single-transaction fusion.
4. `04-metamagic.md` — bounded doctrines and causality.
5. `05-mahou-disposition-provider-routing.md` — clean-room disposition/provider routing.
6. `06-sigils-ritual-presentation.md` — runtime presentation-payload/material/provider contract; concrete art lives in visual-production.
7. `07-provider-contract-verification.md` — exact-version provider gates.
8. `08-hardening-stage08-handoff.md` — deterministic hardening/performance/Stage 08 handoff.

## TDD and promotion

Each runtime package starts from fresh `main`, writes contract tests RED, implements minimal server-authoritative GREEN, adds required GameTests/provider integration evidence, runs NeoForge build/JAR/dedicated-server gates, reconciles latest `main` and reruns relevant gates before promotion.

07A is accepted only when polarity cannot be client-forged; fusion/metamagic preserve one canonical transaction and cannot double-charge/cooldown/reward/proc; WorldEffectPolicy/target/work/hazard/replay limits cannot be bypassed; blood/resurrection composition does not duplicate authority; exact provider dependencies are proven or fail closed; no protected Mahou asset/code is shipped; presentation payloads are read-only/server-authored; and Stage 08 receives bounded tunable formulas rather than unresolved ownership questions.