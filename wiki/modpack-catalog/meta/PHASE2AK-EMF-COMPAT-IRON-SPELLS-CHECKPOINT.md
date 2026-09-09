# Phase 2AK checkpoint — EMF Compat: Iron's Spells 2.0.0

## State

`CATALOG CLOSURE CANDIDATE / CLIENT PRESENTATION COMPAT / NOT CANONICAL UNTIL LATEST-MAIN RECONCILIATION + EXACT-HEAD CI GREEN + MERGE`

## Base

- initial canonical `main`: `83a5cbf95e2e2eeb8c4e5e161aa2eb590b78712b`
- predecessor: Phase 2AJ / PR #143, component #38
- branch: `docs/magic-catalog-phase2ak-emf-compat-irons-spells-2.0.0`
- canonical coverage at branch creation: `38/100 = 38%`
- proposed result after canonical merge: `39/100 = 39%`

No equivalent open branch or PR for this provider was found immediately before branch creation.

## Physical identity

- artifact: `emf_compat_iron_spells_1.21.1_2.0.0.jar`
- mod id: `emf_compat_iron_spells`
- version: `2.0.0`
- SHA-1: `515b545870fce128bbf01a0ccacdd19566ed3b22`
- physical NeoForge: `21.1.248`
- physical Iron's: `1.21.1-3.16.3`
- physical EMF: `3.3.5`
- physical EMF Compat Core: `2.0.0`

## Exact source

Publisher source:

`victorkozhokin/emf-compat@79d730a9d02275b7d721967c75f5f22dc815d9dc`

Dedicated NeoForge 1.21.1 subproject metadata matches physical semantic version exactly:

- `mod_version=2.0.0`
- `mod_license=GNU GPL 3.0`
- NeoForge build baseline `21.1.230`
- Java 21

Build baseline uses Iron's 3.15.6 and EMF 3.3.2; generated runtime metadata requires Iron's >=3.15.0, EMF >=3.3.2 and EMF Compat Core >=2.0.0, all client-side.

## Closed inventory

Semantic player spells: **0**.

Provider gameplay registry objects: **0 observed in exact addon subproject**.

Exact client compatibility inventory:

- 5 Java classes total in the audited addon package surface:
  - `EMFCompatIronSpellsMod`
  - `IronSpellsCompat`
  - `PlayerModelMixin`
  - `PlayerRendererMixin`
  - `EMFAnimationPauseHandlerMixin`
- 3 required client mixins;
- 2 provider config booleans;
- 1 `iron_spells` pose source with priority 10;
- 1 registered EMF first-person vanilla-model condition;
- 0 addon gameplay network payloads;
- 0 server event/casting/resource/world-effect authority.

## Semantics

- Iron's remains authority for cast state, spells, mana and cooldowns.
- Local rendering reads immediate Iron's client casting state; remote rendering reads server-synced Iron's spell data.
- `PlayerModelMixin` captures casting arm poses after animation.
- `PlayerRendererMixin` restores first-person arm/sleeve rotations.
- `EMFAnimationPauseHandlerMixin` lets EMF continue animating during Iron's casting while respecting explicit EMF entity pause.
- First-person vanilla model is forced only under the provider's explicit local first-person/casting/arms-or-items conditions.

## Black Arcana boundary

- visual pose state is not cast authority;
- no BA spell or server runtime may depend on these client mixins;
- no second Iron's animation-compat layer should be created by BA;
- BA-native EMF support, if ever needed, must be a separate bounded presentation adapter driven by BA canonical cast state;
- Phase 3 remains blocked.

## Provenance

Source inspection is read-only and recorded in `docs/provenance/REFERENCE_LEDGER.md` in this same revision. No source code or assets are copied/adapted.

Exact source metadata and publisher project metadata identify GPLv3/GNU GPL 3.0; no root `LICENSE` file was located at the inspected revision through the repository contents endpoint, so this phase makes no broader reuse claim.

## Remaining QA

Does not block semantic catalog closure but remains explicit:

- source↔physical-JAR byte reproducibility not proven;
- full-modpack client rendering with physical Iron's 3.16.3 + EMF 3.3.5 not independently exercised in this catalog phase;
- resource-pack-specific animation correctness is runtime presentation QA.

## Merge protocol

Before merge:

1. fetch current `main` again;
2. merge/reconcile it into this branch if advanced;
3. review the resulting diff;
4. ensure provenance review has no blockers;
5. run Black Arcana CI on the exact reconciled HEAD;
6. require unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke GREEN;
7. merge only with expected exact HEAD;
8. confirm resulting `main` SHA.
