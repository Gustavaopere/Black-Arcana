# Phase 2AL checkpoint — `efiscompat` 3.1.0

## State

`CATALOG CLOSURE CANDIDATE / CASTING-INTERACTION+ANIMATION COMPAT / NOT CANONICAL UNTIL LATEST-MAIN RECONCILIATION + EXACT-HEAD CI GREEN + MERGE`

## Base

- initial canonical `main`: `73a425051d242a33af157a3f73ca816498e8eba8`
- predecessor: Phase 2AK / PR #144, component #39
- branch: `docs/magic-catalog-phase2al-efiscompat-3.1.0`
- canonical coverage at branch creation: `39/100 = 39%`
- proposed result after canonical merge: `40/100 = 40%`

No equivalent open branch or PR for `efiscompat` was found immediately before branch creation. Existing old Ars PRs remain separate concurrent work and are not modified by this phase.

## Physical identity

- artifact: `efiscompat-3.1.0.jar`
- mod id: `efiscompat`
- runtime: `3.1.0`
- display name: `Epic Fight & Iron's Spellbook animation compat`
- physical SHA-1: `4250e1c65732d70d1091cc50b84a91b6ed5b2b3f`
- physical NeoForge: `21.1.248`
- physical Epic Fight: `21.17.3.1`
- physical Iron's: `1.21.1-3.16.3`

## Publisher release

CurseForge:

- project `1109064`;
- file `8372294`;
- 1.21.1 NeoForge release `3.1.0`;
- published `2026-07-05`;
- client + server;
- release note: dedicated-server crash fix for certain spell casts.

## Exact source

Official publisher-linked source:

`domanhthang2110/efiscompat@b4b58aff86e707420fac8a7c29fe647d7f5aaac4`

The exact commit belongs to the dedicated `1.21.1` branch, is dated `2026-07-05`, is titled `Fixed dedicated server crash`, and changes `mod_version=3.0.0` to `3.1.0`.

Exact source metadata:

- Minecraft `1.21.1`;
- Java 21;
- NeoForge build baseline `21.1.219`;
- Iron's build baseline `1.21.1-3.15.6`;
- `mod_id=efiscompat`;
- `mod_version=3.1.0`;
- source metadata license `GNU GPLv3`.

Generated metadata requires BOTH-side Epic Fight `[21,)` and Iron's `[1.21.1-3.15.0,)`.

## Closed inventory

Semantic player spells: **0**.

Exact provider surface:

- 28 Java source files;
- 35 provider Epic Fight animation accessors;
- 12 required mixins:
  - 6 client;
  - 6 common;
- 6 common config keys;
- `SpellAnimationLoader` JSON reload path;
- 9-field chant/cast/continuous + staff-side animation schema;
- provider default mapping + built-in mappings for Iron's and selected addons;
- Iron's `SpellPreCastEvent` veto driven by Epic Fight stun/recent-action state;
- active Iron's cast cancellation from Epic Fight skill/guard/dodge paths;
- targeted `ComboBasicAttack` block while Iron's casting;
- Iron's cast-complete/cancel animation-layer cleanup;
- 0 provider-owned mana/resource system;
- 0 Black Arcana gameplay state.

## Authority result

- Iron's owns spells, cast state, mana, spell effects and cooldown semantics.
- Epic Fight owns combat action/stun/skill/animation state.
- `efiscompat` owns reconciliation policy and its animation presentation layer.
- Black Arcana does not duplicate Iron's↔Epic Fight cancellation/animation handling.
- Black Arcana retains canonical casting/cost/target/effect/cooldown, Corruption, Strain, Arcane Danger, rituals/hazards and `WorldEffectPolicy`.
- RPG Skill Tree gains no magic runtime authority from this component.

## Important QA boundary

`MixinComboBasicAttack` targets `com.p1nero.invincible.skill.ComboBasicAttack` while exact runtime metadata does not declare that namespace as a dependency and the current top-level modlist exposes no obvious `invincible`/Nightfall provider row.

This is **not** promoted to a failure claim. It remains a target-presence/ownership question for physical runtime QA.

## License / provenance

There is a license metadata conflict:

- CurseForge labels the project MIT;
- exact source `gradle.properties` declares `GNU GPLv3`;
- no root `LICENSE` file was present in the exact source tree inspected.

Disposition: read-only factual source inspection only; no code/assets copied; reuse blocked pending independent license reconciliation.

## Remaining QA

Does not block semantic catalog closure but remains explicit:

- source↔physical-JAR byte reproducibility not proven;
- exact application of all 12 required mixins on physical Epic Fight 21.17.3.1 / Iron's 3.16.3 not exercised here;
- `ComboBasicAttack` physical target owner/presence not proven;
- full-modpack dedicated-server/client multiplayer smoke not run in this catalog phase;
- third-party animation mapping parity with exact physical addon versions not proven;
- future BA-native Epic Fight adapter contract remains unimplemented/unproven.

## Merge protocol

Before merge:

1. fetch current `main` again;
2. reconcile it into this branch if advanced;
3. review the resulting diff;
4. ensure provenance review has no blockers;
5. run Black Arcana CI on the exact reconciled HEAD;
6. require the repository's applicable unit/build/GameTest/dedicated-server gates GREEN on that exact HEAD;
7. merge only with expected exact HEAD;
8. confirm resulting `main` SHA.