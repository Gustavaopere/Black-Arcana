# Epic Fight 21.17.3.1 — exact artifact skill audit

Status: `EXACT PHYSICAL=PUBLISHER / 43-SKILL REGISTRY CLOSED / 3 SUPERNATURAL ROOTS STRICT`

## Identity gate

Current physical sibling authority:

- JAR: `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`;
- mod id: `epicfight`;
- runtime: `21.17.3.1`;
- SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`.

NON-MERGE PR #562 audits CurseForge project/file `405076 / 8175609` and fails before semantic inspection unless its SHA-1 equals the physical fingerprint.

Final bounded audit:

- HEAD: `3b8e5ccd58e72bc99fdeeaac84b10d8f25538ca0`;
- run: `37170317148` — SUCCESS;
- artifact: `11291375884`;
- artifact digest: `sha256:88fbb713615e5f996a40c609facb03792df812c4a762e47247bb3e1d6466821b`;
- publisher SHA-1: `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`;
- publisher SHA-256: `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`;
- bytes: `8,578,288`.

Result: exact physical/publisher equality is proven.

## Bounded archive inventory

- archive entries: **3,213**;
- classes: **1,530**;
- resources: **1,683**;
- skill-like classes: **117**;
- skill-like resources: **280**;
- `data/epicfight/**` paths: **174**.

No third-party JAR bytes are committed to Black Arcana.

## Exact skill registry

Direct disassembly of the exact provider registrar closes **43 unique core skill IDs**. The complete object-level disposition is materialized separately; no public marketing count is used as the denominator.

Category-level disposition:

- technical/core: 2;
- dodge/wakeup: 3;
- guard: 3;
- passive: 14;
- identity: 2;
- mover: 2;
- weapon innate: 16;
- weapon passive: 1.

Total: **43**.

## Exact trident moveset binding

The exact `EpicFightMovesets.TRIDENT` innate selector checks the current trident enchantment and returns one Epic Fight skill holder:

- vanilla Riptide -> `TSUNAMI`;
- otherwise vanilla Channeling -> `WRATHFUL_LIGHTING`;
- otherwise vanilla Loyalty -> `EVERLASTING_ALLEGIANCE`;
- otherwise -> `GRASPING_SPIRE`.

This directly closes owner and normal current reachability for the three supernatural candidates. The owner is the vanilla trident; the enchantment selects the provider-owned innate action.

## Exact supernatural settlement seams

### `epicfight:wrathful_lighting`

The exact skill/animation seam attaches the provider server-side `SUMMON_THUNDER` event to the action. This establishes a deliberate lightning invocation with provider-owned execution/settlement.

### `epicfight:tsunami`

The exact artifact packages dedicated Tsunami animation resources and provider Tsunami particle paths. The exact selector resolves the skill for Riptide, and exact control flow chooses the strengthened action variant when the server player is in water or rain. The action is therefore a provider-owned supernatural tide/mobility attack, not an alias for ordinary trident use.

### `epicfight:everlasting_allegiance`

The exact skill obtains the provider patch for the thrown trident and invokes `recalledBySkill()`. Exact thrown-trident behavior then performs the provider return path and entity-hit settlement. This is a deliberate damaging supernatural recall action distinct from vanilla Loyalty's automatic passive return.

## Exclusion audit

The other 40 exact IDs remain outside the semantic-magic numerator:

- technical registry/host slots;
- dodge, wakeup and guard/parry actions;
- all 14 passive/reactive skills;
- ordinary combat identities;
- mover/mobility skills;
- conventional martial weapon-innate attacks;
- weapon-passive support.

`forbidden_strength` is a specific negative-control case: exact implementation classifies it as passive stamina/health substitution. Magical wording does not promote a passive resource rule into a spell/action identity.

## Skillbook boundary

The exact artifact contains Epic Fight's skillbook loot surface, including a provider loot modifier for `epicfight:skillbook`. That surface is not used to establish reachability for the three counted roots because they are selected as weapon innates by the exact trident moveset.

## Semantic disposition

- exact provider skill IDs: **43**;
- supernatural action roots: **3**;
- `COUNTED_EXACT`: **3**;
- `EXCLUDED`: **40**;
- strict semantic contribution: **+3**.

## Clean-room boundary

The durable catalog retains hashes, IDs, counts, category membership, moveset-selection facts and behavior-level control/settlement facts needed for cataloging and deduplication. It does not redistribute the JAR, implementation bodies, animation assets or localization prose beyond minimal identity labels.
