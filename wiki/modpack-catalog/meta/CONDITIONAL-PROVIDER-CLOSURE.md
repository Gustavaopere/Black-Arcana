# Black Arcana — Conditional Provider Closure Index

Checkpoint: 2026-10-06 current routing

Status: `2 CATALOG-OPEN ⚠️ DIRECTORIES / 14 DEPLOYED-EVIDENCE ROUTES / CURRENT PHYSICAL MAGIC TAXONOMY 97/97 MAPPED / STRICT MINIMUM 1849`

## Purpose

This index routes providers that still have a specific deployed config/script/reachability/runtime evidence gate. Folder prefix is no longer the routing criterion: a provider can be `✅ cataloged` while retaining fail-closed deployed QA.

It does **not** replace provider dossiers, does not change the strict semantic ledger, and does not certify runtime compatibility. Its purpose is to prevent repeated registry enumeration and point each provider at the smallest authoritative evidence gate that remains open.

Current provider-directory reality is read from canonical Black Arcana `main`; physical presence/version authority is reconciled against sibling `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`. This routing document intentionally does **not** pin its own parent `main` SHA, because doing so becomes stale as soon as the document itself is merged:

- **2** provider directories carry the ⚠️ prefix: Traveloptics and Deeper and Darker;
- the table below preserves **14 bounded deployed-evidence routes** because 12 catalog-closed ✅ providers still retain specific config/reachability/runtime conditions worth routing;
- a ✅ folder means semantic denominator/materialization is catalog-closed, not that deployed runtime/config QA automatically passed;
- Immersive Portal Iron's bridge, Iron's Recolor, Spell Actionbar and Spell Codex Specs remain **✅ cataloged at +0 independent semantic identities**; their remaining interoperability/runtime QA stays separate.

A route leaves this index when its named deployed-evidence gate is satisfied or becomes irrelevant. Folder prefix changes are required only when catalog completeness itself changes.

## Current deployed-evidence routes

| Provider | Current catalog closure already achieved | Remaining evidence gate | Canonical evidence route |
|---|---|---|---|
| Asterism Arcanum `1.21.1-0.1.0` | 11 exact registered spell identities; 10 ordinary survival spells strict-counted; `TrailblazeSpell` excluded; exact Iron's 3.16.3 host audit proves `astral_gateway` is default Astral-loot eligible | Effective deployed Iron's spell config/datapack for `asterismarcanum:astral_gateway`: `enabled`, effective `school`, `allow_crafting`, global fallback and datapack overrides; or deterministic assembled-pack equivalent | [SURVIVAL-CLOSURE-CHECKLIST.md](../providers/✅-asterism-arcanum/SURVIVAL-CLOSURE-CHECKLIST.md) |
| Gaze `1.1.7.1` | Soulward Shield strict-counted exact; 26 exact Spirit Rite identities enumerated; Geas effects/runes excluded by metric | Effective deployed COMMON `disableGazeRites` or authoritative assembled-pack proof of Rite registry initialization | [DEPLOYED-CONFIG-CHECKLIST.md](../providers/✅-gaze/DEPLOYED-CONFIG-CHECKLIST.md) |
| Not Enough Glyphs `4.6.2` | Exact physical/publisher line and source registration matrix closed: 40 registrations, 39 source-enabled candidates, Momentum source-disabled; canonical `glyph_*` resource ids corrected | Effective deployed `[general].enabled` state for the 39 candidates, via actual SERVER configs or schema-3 runtime-probe evidence | [DEPLOYED-CONFIG-CHECKLIST.md](../providers/✅-not-enough-glyphs/DEPLOYED-CONFIG-CHECKLIST.md) |
| Somake Spells `1.0.9` | Physical SHA-1 equals exact File `8867079`; exact registry = 83 IDs; exact gate topology = 67 unconditional + 16 optional; current provider composition admits 83/83 | Effective deployed `enableSpellLockSystem`; effective Iron's `enabled` / `school` / `allow_crafting` overrides; provider/host survival acquisition and current Aqua coexistence/authority where applicable | [CURRENT-1.0.9-REVALIDATION-CHECKLIST.md](../providers/✅-somake-spells/CURRENT-1.0.9-REVALIDATION-CHECKLIST.md) |
| Corail Tombstone `9.5.6` | Physical Project Library SHA-1 equals exact File `8842741`; 10 prayer/Ritual Flute actions are `COUNTED_EXACT`; 12 additional castable action families exactly deduplicated one-to-one to `allow_*` gates | Effective deployed values of the 12 `AllowedMagicItems` booleans; missing/ambiguous values remain fail-closed. Recheck the exact fingerprint in the eventual deployed-evidence report as a drift guard | [DEPLOYED-CONFIG-CHECKLIST.md](../providers/✅-corail-tombstone/DEPLOYED-CONFIG-CHECKLIST.md) |
| Mowzie's Mobs `1.8.2` | Exact physical=publisher artifact; 13 active player-ability slots reconciled to 10 strict actions + 1 conditional Tunneling action; technical `hit_boulder` / `backstab` excluded | Effective deployed `tools_and_abilities.earthrend_gauntlet.enable_tunneling` from the exact current instance/world; physical fingerprint must match the cataloged 1.8.2 SHA-1 | [DEPLOYED-CONFIG-CHECKLIST.md](../providers/✅-mowzies-mobs/DEPLOYED-CONFIG-CHECKLIST.md) |
| Deeper and Darker `1.4.1` | Public GitHub/Modrinth/CurseForge 1.4.1 artifacts are byte-identical and close a three-root supernatural baseline, while current physical SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88` is `OTHER_VERIFIED`; retained chronology and bounded repack/source-build audits do not bridge those bytes | Direct inspection/cryptographic bridge for the current physical JAR plus authoritative deployed `config/deeperdarker-common.toml -> soulElytraCooldown`; the canonical collector already captures the exact fingerprint and bounded integer key, so new scaffolding is not required. Until physical closure, the three public roots remain baseline-only and +0 strict | [README.md](../providers/⚠️-deeper-and-darker/README.md) |
| KubeJS Ars Nouveau `1.3.2` | Exact physical release identified; framework exposes six Ars recipe schemas and +0 provider-owned spell/glyph identities | Exact current `kubejs/server_scripts/**` / relevant `kubejs/data/**` mutation inventory to close recipe/tome reachability and economy effects on existing Ars objects | [PACK-SCRIPT-CLOSURE-CHECKLIST.md](../providers/✅-kubejs-ars-nouveau/PACK-SCRIPT-CLOSURE-CHECKLIST.md) |
| T.O Magic n' Extras / Traveloptics `4.4.0.1-1.21.1` | Current physical filename/SHA-1 are known; an older 2026-08-18 CurseForge snapshot records File `6342780` with `isModified=true`, but it does not prove ancestry of the later current SHA-1; physical bytes remain `OTHER_VERIFIED` vs publisher/known patch; 33-ID publisher baseline is not exact-current | Authoritative current-instance capture using the existing collector/probe: exact installed hash, schema-4 registry + serializer pair, bounded Blackout/generic-route surfaces and Iron's `traveloptics` overrides (`enabled`/`school`/`allow_crafting`); plus raw-byte provenance/content delta when available. Blackout survival and Aqua authority remain fail-closed until the captured evidence actually proves them | [CLOSURE-CHECKLIST.md](../providers/⚠️-traveloptics/CLOSURE-CHECKLIST.md) |
| Ice And Fire Community Edition `2.1.2` | Exact physical SHA-1 equals publisher File `8757837`; exact source closes 9 active action families; exact provider-data reachability promotes 7 and current-pack NeoForge 21.1.250 runtime audit `36327488231` promotes Dread Lich Staff for 8 strict total | Ghost Sword only: exact recipe is closed, but deployed Jupiter `tools.phantasmalBladeAbility` is still required | [DEPLOYED-CONFIG-AND-REACHABILITY-CHECKLIST.md](../providers/✅-ice-and-fire-ce/DEPLOYED-CONFIG-AND-REACHABILITY-CHECKLIST.md) |
| ShadowsZ `1.1.9` | Exact physical/publisher SHA-1 equality plus bounded exact-artifact audit close the complete semantic inventory at **10**: 3 Umbral spells + Shadow Eyes + Shadow Arising + Summon + Dismiss + Position Swap + Despawn Wild + Fusion; batch/group summon/dismiss are aliases and management/progression surfaces are excluded | Effective current-world `shadowszRestrictPowers` plus deployed `fusionEnabled`; all power surfaces are attunement-gated and Fusion is additionally config-gated | [DEPLOYED-STATE-CHECKLIST.md](../providers/✅-shadowsz/DEPLOYED-STATE-CHECKLIST.md) |
| Simply Swords: Cataclysm `1.0.2+1.21.1+neoforge` | Exact physical identity plus release-correlated `1.21.1-neo@a81158e...` source close exactly four semantic abilities: Blazing Brand, Accursed Rage, Mecha Pulse, Mecha Smite | Effective deployed STARTUP config for the four action gates/chances; source defaults cannot establish current active subset | [DEPLOYED-CONFIG-CHECKLIST.md](../providers/✅-simply-swords-cataclysm/DEPLOYED-CONFIG-CHECKLIST.md) |
| Simply More `1.3.0 Alpha 5` | Exact physical/publisher File 8736778 audit closes the current-pack semantic denominator at 24 player actions: 10 active-API roots + 13 legacy direct-use roots + 1 shared Mimicry transformation; Idol/TO_REMOVE, Reforming Remnant, passive/proc/implicit surfaces and absent Mythic Metals Tidesinger compat are excluded | Deployed reachability only: Simply Swords Awakening/unlock state, current acquisition/reformation paths, effective Mimicry form-disable state, and any deployed config/datapack/script suppression | [EXACT-ALPHA5-ARTIFACT-AUDIT.md](../providers/✅-simply-more/EXACT-ALPHA5-ARTIFACT-AUDIT.md) |
| Simply Swords `1.70.2-1.21.1` | Exact hash-matched File 8746001 audit plus release-correlated/version-declared source close the player-action denominator at exactly 66: 62 ACTIVE Unique roots + 4 player-use Runic families; the exact artifact narrows the residual surface to two Secondary continuations and two direct-use pass-through overrides, all +0 additional roots | Deployed reachability only: exact physical fingerprint + bounded General/Loot config route are now collector-covered; per-stack Awakening/unlock state, current acquisition/reformation, compat-dependent materialization, other deployed suppression and final addon ownership reconciliation remain open | [DEPLOYED-REACHABILITY-CHECKLIST.md](../providers/✅-simply-swords/DEPLOYED-REACHABILITY-CHECKLIST.md) |

## Catalog-closed zero-semantic technical providers

These providers are **✅ cataloged** because their independent semantic contribution is fully closed at **+0**:

- Immersive Portal Iron's Spells addon;
- Iron's Spells Recolor;
- Spell Actionbar;
- Spell Codex Specs;
- Iron's Spellbooks KubeJS — semantic denominator closed at +0 by exact-source + owner-attestation evidence; deployed `kubejs/` filesystem parity remains QA and contradictory current registration scripts reopen the provider.

Their exact implementation/interoperability/config/runtime QA remains fail-closed and separate. Do not move that technical debt into the semantic numerator or reinterpret ✅ as runtime certification.

## Deployed-evidence collector coverage

The read-only collector in [`docs/qa/provider-catalog-deployed-evidence.md`](../../../docs/qa/provider-catalog-deployed-evidence.md) currently has bounded routes for:

- Asterism physical fingerprint + Astral Gateway Iron's config/datapack;
- Gaze physical fingerprint + `disableGazeRites`;
- NEG physical fingerprint + 39 canonical enabled-state paths/runtime rows;
- Tombstone physical fingerprint + 12 `AllowedMagicItems` booleans;
- Somake physical fingerprint + spell-lock and Iron's override evidence;
- Mowzie's physical fingerprint + `enable_tunneling`;
- Ice And Fire CE physical 2.1.2 fingerprint + exact Jupiter `tools.phantasmalBladeAbility` gate;
- ShadowsZ physical 1.1.9 fingerprint + bounded `fusionEnabled` config observations + saved-world `shadowszRestrictPowers` gamerule;
- Simply Swords: Cataclysm physical 1.0.2 fingerprint + exact `config/simplycataclysm-startup.toml` ten-key activation gate;
- Simply More Alpha-5 physical fingerprint + exact 25-form `config/simplymore/unique_effect.toml -> mimicry.config.<form>.disabled` subgate; Awakening/acquisition/reformation remain outside this bounded collector route;
- Simply Swords 1.70.2 physical fingerprint + bounded `config/simplyswords/general.toml` Awakening flag and `config/simplyswords/loot.toml` loot/remnant reachability fields; per-stack Awakening/unlock, full acquisition and compat-dependent materialization remain outside this bounded collector route;
- Traveloptics physical classification + bounded `traveloptics:blackout` references.

Ice And Fire CE is now covered for the bounded Ghost Sword Jupiter gate. The collector reads only `config/iceandfire/iaf-common.json -> tools.phantasmalBladeAbility`. Dread Lich Staff acquisition is separately closed by exact provider/runtime audit `36327488231` and no longer needs collector evidence.

The collector now emits an exact bounded KubeJS script/data path+hash inventory for both KubeJS providers. That can prove an authoritative current tree is absent/empty; non-empty trees still require provider-specific script/provenance review and are not auto-closed by the collector.

## Evidence priority

For these providers, future work must use this order:

1. actual current-pack deployed config/script/datapack/runtime evidence when the checklist requires it;
2. exact physical artifact identity/hash and provider-exposed registry/resource state;
3. exact source/API/public provider documentation when legally and technically available;
4. deterministic assembled-pack runtime observation;
5. public editorial guidance only for semantic description when it cannot prove deployed state.

Source defaults, generic publisher claims, creative/command access, registry presence alone, and unrelated Black Arcana CI are not substitutes for the specific deployed evidence named by each checklist.

## Clean-room and authority rules

- All Rights Reserved providers must not be decompiled merely to force catalog closure.
- Do not invent registry IDs, hooks, classes, configs, acquisition paths, settlement semantics or runtime results.
- Do not create a Black Arcana fallback that replaces missing provider behavior.
- Black Arcana owns its runtime; provider-native magic remains provider authority; RPG Skill Tree remains progression/Mastery/perk/gate authority through real contracts only.
- Runtime/API QA may remain fail-closed after catalog closure and is not, by itself, a reason to keep a fully closed semantic catalog at ⚠️.

## Do not redo

Already closed evidence must be reused unless the physical/source line changes:

- Asterism: 11 exact registrations; 10 ordinary survival cards already strict-counted;
- Gaze: Soulward Shield + 26 exact Rite identities;
- NEG: 4.6.2 registration/fallback matrix = 40 / 39 source-enabled and canonical `glyph_*` identities;
- Somake: physical equality, exact 83-ID registry, exact 67+16 gate topology and current 83/83 registration composition;
- Tombstone: physical SHA-1 equality to File `8842741`, 10 `COUNTED_EXACT` prayer/rite actions + exact one-to-one deduplication of 12 config-gated castable families;
- Mowzie's: exact 1.8.2 physical artifact, 13 active slots, semantic split 10 strict + 1 conditional + 2 technical/subaction exclusions;
- Traveloptics: physical SHA-1 disposition is `OTHER_VERIFIED`; the older launcher snapshot records a File-6342780 slot with `isModified=true`, but temporal continuity to the later SHA-1 is unproven; publisher-baseline 33-ID inventory remains baseline only until exact current bytes/provenance are audited;
- Ice And Fire CE: exact 2.1.2 physical/publisher identity, action candidates and Dread Lich Staff inherited drop reachability are closed; only the current Ghost Sword Jupiter config remains a catalog blocker;
- KubeJS frameworks: provider-owned semantic denominators are classified; Iron's Spellbooks KubeJS deployed filesystem parity remains QA only, while KubeJS Ars Nouveau script mutations remain deployment/reachability/economy QA for externally owned Ars objects.

## Promotion discipline

When one checklist closes:

1. capture the exact evidence checkpoint/fingerprint;
2. update only provider/object rows actually proven;
3. reconcile the strict semantic ledger only if the counting rule/result changes;
4. update the provider folder prefix only when its declared catalog scope is fully closed;
5. keep runtime/integration QA separate;
6. recheck the latest physical modlist/provider version immediately before merge.

This index is a routing document. It adds no semantic objects itself. The current strict reconstructible minimum is **1849**; the prior 1858 checkpoint is historical because Ars Morph (+8) and Woodwalkers SpellBooks (+1) are absent from the current physical snapshot.