# Somake Spells 1.0.9 — exact release registry structural audit

Status: `EXACT PHYSICAL=PUBLISHER 1.0.9 / 83 DECLARED SPELL REGISTRATIONS / 67 UNCONDITIONAL + 16 OPTIONAL-GATED / CURRENT MOD-COMPOSITION 83/83 / REACHABILITY + DEPLOYED CONFIG OPEN`

## Provenance

Current physical line:

- sibling authority rechecked at `neoforge-rpg-skilltree@af648d441441dde929cd49c5e18509347f06f09a`;
- installed filename: `somakespells-1.0.9-1.21.1.jar`;
- mod id: `somakespells`;
- runtime: `1.0.9`.

Exact publisher artifact:

- CurseForge project `1461634`;
- file `8867079`;
- publisher SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- observed SHA-256 `1f48dfb93e290b45b628b280d902b2b6471b9d80c2c1b70a4980f14dbe85d48a`;
- observed size `2,543,689` bytes.

Project Library physical checkpoint `modlist(1).txt` fingerprints the installed `somakespells-1.0.9-1.21.1.jar` at SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`, exactly equal to File `8867079`. Physical installed bytes ↔ audited publisher artifact equality is therefore **closed**.

## NON-MERGE clean-room checkpoints

Registry audit commit lineage:

- initial structural checkpoint: `0fe14c09704b5c11623f39ac2cef1511dbe6edab`;
- refined checkpoint: `fcd6ce8c59cf5d7a153198fc45eff4761c274ba5`;
- audit-only run: `36092269302`;
- audit job: `107936996913`;
- result: **SUCCESS**;
- registration-gate refinement HEAD: `071bdd92fed50aea65ad47772f4d1fb0cb8b7536`;
- refinement run: `36161117761`;
- verify job: `108157871675` — **SUCCESS**;
- Stage 05 companion smoke job: `108159016060` — **SUCCESS**.

The audit retained only cryptographic hashes, archive/resource identities, class/member signatures, exact registry string identities, aggregate branch/call counts and bounded compatibility/config symbols. No implementation body or protected asset content is copied or reconstructed.

## Exact release registry topology

`com.somake.somakespells.registries.ModSpells` in File `8867079` contains:

- **83** `DeferredHolder` spell fields;
- **83** `DeferredRegister.register(...)` call sites;
- **83** unique registry IDs;
- **83** top-level provider `*Spell` classes;
- **83** base `spell.somakespells.<id>` localization roots;
- **83** matching `.guide` roots.

Set comparison:

- registry IDs absent from base localization: **0**;
- base localization IDs absent from the registry declaration: **0**.

This closes the exact publisher-release **declared registry inventory** at 83 identities. Conditional branches may still prevent a subset from becoming active in a particular assembled mod composition; deployed active registry outcome remains a separate gate.

## Exact 1.0.8-fix → 1.0.9 registry delta

Historical exact control:

- 1.0.8-fix SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7`;
- 67 fields / 67 register calls / 67 top-level spell classes.

Current release delta:

- additions: **17**;
- removals: **1**;
- net: **+16**;
- current total: **83**.

Added IDs:

- `somakespells:bloodbound_blade`;
- `somakespells:comforting_lullaby`;
- `somakespells:crimson_reflection`;
- `somakespells:funeral_bloom`;
- `somakespells:grave_sigil`;
- `somakespells:procession_of_souls`;
- `somakespells:sacred_phoenix_blessing`;
- `somakespells:soul_bastion`;
- `somakespells:soul_latch`;
- `somakespells:soul_reprisal`;
- `somakespells:soulfall_judgment`;
- `somakespells:sovereign_armory`;
- `somakespells:spectral_rondo`;
- `somakespells:spiral_of_ruin`;
- `somakespells:summon_drowned`;
- `somakespells:winged_ruin`;
- `somakespells:withered_rose_vortex`;

Removed historical ID:

- `somakespells:summon_zombie`.

The exact registry independently corroborates the publisher statement that Summon Zombie was replaced by Summon Drowned.

## Host method surface

Across the 83 top-level current `*Spell` classes:

- provider `isEnabled()` overrides: **0**;
- provider `allowCrafting()` overrides: **7**.

Constant-false `allowCrafting()` overrides:

- `somakespells:fragmented_requiem`;
- `somakespells:rose_secret`;
- `somakespells:comforting_lullaby`.

Non-constant `allowCrafting()` overrides requiring separate behavior/reachability evidence:

- `somakespells:funeral_bloom`;
- `somakespells:withered_rose_vortex`;
- `somakespells:custodia_caeli`;
- `somakespells:jingle_bell`.

For the remaining spell classes, absence of a provider-level override means host behavior is inherited; it does **not** prove the deployed Iron's config/datapack values.

## Current config/compat structural facts

The exact 1.0.9 artifact still contains:

- `enableSpellLockSystem` in `Config.class`;
- `somakespells/general/common.toml` in the main mod bootstrap surface.

The refined exact-binary audit additionally closes the `enableSpellLockSystem` NeoForge config definition with code default **`false`**. The effective deployed COMMON value remains unverified; a code default is not substituted for deployed state.

Artifact-wide `ModList.isLoaded(...)` calls were observed for current integration surfaces including:

- `mowziesmobs`;
- `iss_magicfromtheeast`;
- `legendary_monsters`;
- `born_in_chaos_v1`;
- `tunes_n_tomes`;
- `gtbcs_geomancy_plus`.

The artifact-wide compatibility checks above are broader than the spell-registration path. The refined exact-binary audit follows only `ModSpells` registration control flow and closes exactly three cached registration predicates:

- Mowzie's Mobs → 3 IDs;
- ISS: Magic From The East → 4 gate uses, including two IDs nested with Legendary Monsters;
- Legendary Monsters → 11 gate uses, including the same two nested IDs.

After deduplication, the exact 1.0.9 registry is **67 unconditional + 16 unique conditional registrations**. Born in Chaos, Tunes 'n Tomes and Geomancy Plus have compatibility checks elsewhere in the artifact but do not gate `ModSpells` registrations in this exact release.

The current physical pack contains Mowzie's Mobs, ISS: Magic From The East and Legendary Monsters. Therefore Somake's own optional-registration predicates admit **83/83** declared IDs for this pack composition. See [`EXACT-1.0.9-REGISTRATION-GATE-MAP.md`](EXACT-1.0.9-REGISTRATION-GATE-MAP.md).

## Semantic accounting

Exact publisher-release declared spell identities: **83**.

Strict semantic contribution: **+0 at this checkpoint**.

Reason: the current counting rule still requires deployed/usable semantic reachability. Remaining blockers include:

- effective Iron's `enabled` / `allow_crafting` config/datapack state;
- effective `enableSpellLockSystem` state where it affects use/progression;
- school-focus/acquisition paths;
- object-level or bounded-set survival reachability;
- Somake Aqua ↔ Traveloptics coexistence/authority.

## Result

The previous statement `1.0.9 registry UNVERIFIED` is superseded.

Current exact publisher-release registry state:

**83 exact physical spell identities / current mod-composition registration outcome 83/83 / semantic reachability and deployed host/provider config still conditional.**
