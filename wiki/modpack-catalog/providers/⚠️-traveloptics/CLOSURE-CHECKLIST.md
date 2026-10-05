# T.O Magic n' Extras 4.4.0.1-1.21.1 — Closure Checklist

Status: `33 REGISTERED SPELL IDS + EXACT PUBLISHER MECHANICS CATALOGED / CURRENT PHYSICAL PROMOTION BLOCKED / RUNTIME FAIL-CLOSED`

## Purpose

The current Traveloptics dossier already closes the exact publisher-release registry inventory at **33 registered spell identities**, excludes **32 residual localization-only spell IDs**, closes a 33/33 exact publisher mechanics baseline for base/per-level mana and spell-power inputs, cast type/time, max level, minimum rarity and default cooldown, and now additionally closes **37 bounded scalar accessor results across 24 spells**: 29 no-`LivingEntity` accessors plus 8 LivingEntity-signature methods proven entity-unused before strict evaluation. The remaining work is not another spell/default-stat enumeration or another generic scalar sweep. It is a finite set of current-physical/runtime/acquisition evidence gates required before strict promotion can be considered.

This checklist does not promote the provider, does not treat a third-party patch as upstream authority, and does not infer survival acquisition or assembled-pack runtime from publisher marketing language.

## Gate 1 — Physical artifact identity / patch deployment

Current physical evidence establishes the installed version line and filename:

- observed installed filename: `traveloptics-4.4.0.1-1.21.1.jar`;
- latest sibling authority rechecked at `neoforge-rpg-skilltree@b9edb403c06567423d6c101d136b73a1065f2ad4` (Traveloptics dossier blob unchanged from the prior checkpoint): `PROJECT-INSTRUCTIONS/modlist/Addons + Adventure and RPG + Armor, Tools, and Weapons + Magic + Mobs/✅-to-magic-n-extras v4.4.0.1-1.21.1.md` records physical row #550 with that filename/version/mod id and SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- physical version line: `4.4.0.1-1.21.1`;
- exact publisher file: CurseForge project/file `1046916 / 6342780`;
- exact publisher-release SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- exact publisher-release SHA-256: `0372b4b8593288726fb0d6e8cdb86202a87677d0c2dafeb96cab50bf057ec298`.

Project Library physical inventories now place SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` under the canonical `traveloptics-4.4.0.1-1.21.1.jar` filename as early as **2026-08-22**, with later repeats on 2026-09-08 and 2026-09-16. It is neither the original publisher SHA-1 nor the known patch SHA-1. A separate Project Library `minecraftinstance.json` snapshot dated 2026-08-18 records the same canonical filename in a CurseForge File `6342780` slot with publisher SHA-1 `380849...` and `isModified=true` (`isWorkingCopy=false`, `isFuzzyMatch=false`). The four-day interval between that launcher-modified state and the first direct `7b74816e...` hash capture materially narrows lineage, but it still does not prove byte continuity.

A third-party compatibility project published after the original audit exposes patched file `1690333 / 8861368`, filename `traveloptics-4.4.0.1.1-1.21.1-patched.jar`. Exact clean-room binary-diff evidence now fingerprints that candidate at SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d` / SHA-256 `05f588202900c691fb70389435c9997d090f81a699f7df7cdebcbec552298cc2`. Compared with original File `6342780`, both JARs contain 1339 entries, with zero additions/removals and exactly one changed entry: `com/gametechbc/traveloptics/loot/TOLootModifiers.class`; zero non-class resources differ. The patch publisher attributes that one-class delta to correcting the `universal_loot` codec wiring. This establishes an exact comparison target, **not** deployment. Current sibling evidence proves the installed digest `7b74816e...`, but does not materialize those bytes or identify their provenance/content delta. See [`PATCH-8861368-BINARY-DIFF.md`](PATCH-8861368-BINARY-DIFF.md).

Required authoritative result:

| Question | Required evidence | Current state |
|---|---|---|
| Is the physical JAR byte-identical to original File `6342780`? | compare physical SHA-1 with `3808493ce45cdfeb6408e85578adecf13df698e8` | `NÃO` — physical is `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` |
| Is the known patch File `8861368` physically installed? | compare physical SHA-1 with `680fa679d8ea2419a79571f455436367222f6f9d` | `NÃO` |
| What is the `OTHER_VERIFIED` replacement? | exact physical hash + contemporaneous provenance/content audit | `ABERTO` — direct `7b74816e...` capture now reaches 22/08, but entry-level provenance/content delta remains unknown |

Physical disposition remains **`OTHER_VERIFIED`**. Current provenance is now bounded to an August local-modification window but remains **unidentified at entry level**.

**Gate 1 disposition checkpoint:** physical identity classification itself is closed at `OTHER_VERIFIED` (current SHA-1 `7b74816e...` is neither publisher original nor known patch). What remains open is the **provenance/content delta** of those verified replacement bytes and an exact-current registry/stat bridge. The retained Aug-17 JAR metadata provides two local candidate artifacts by name/size, but current inventories do not preserve a physical file-size field for `7b74816e...`; size therefore cannot identify the current replacement. Do not infer registry equality, File-6342780 ancestry, identity with the retained Aug-17 `fixed-keyloot.jar`, or the known later patch fix from the unchanged nominal filename/version. The next gate is still to materialize/audit the exact `7b74816e...` bytes or obtain equivalent contemporaneous exact-content provenance.

Temporary NON-MERGE PR **#474** further tested whether the current SHA-1 can be reproduced by common one-entry repacks of publisher File `6342780` using the exact changed `TOLootModifiers.class` from patch File `8861368`. Run `36649716927` succeeded, and none of the tested Info-ZIP, `jar uf`, or Python `zipfile` variants matched `7b74816e...`. The recorded Aug-17 Library `fixed-keyloot.jar` size also matched none of those candidates. This is negative lineage evidence only: it excludes those exact repack outputs but does not identify the installed replacement or its registry/content delta.

A separate Project Library runtime checkpoint from **2026-08-19** proves that the assembled pack discovered the same nominal filename/version and that its runtime spell analyzer emitted exactly **33 unique `traveloptics:` spell IDs**, equal as a set to the File-6342780 33-ID baseline, including `traveloptics:blackout`. A direct physical inventory only three days later, on **2026-08-22**, records SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

The retained chronology is therefore: Aug-17 local repair artifacts -> Aug-18 launcher `isModified=true` -> Aug-19 33-ID runtime observation -> Aug-22 first direct `7b74816e...` hash capture. This is substantially stronger lineage evidence than the previous September-only boundary, but the Aug-19 log still carries no JAR SHA-1. It does **not** prove that the 33-ID runtime observation used the exact Aug-22 bytes and does not close Gate 1.

## Gate 2 — Loot-modifier registry initialization

Exact clean-room structure of publisher File `6342780` established:

- `key_loot` registry name present;
- `universal_loot` registry name present;
- `KeyLootModifier.CODEC` referenced twice by the setup;
- `UniversalLootModifier.CODEC` referenced zero times by the setup.

That mismatch remains a structural risk until the **actual physical pack** proves one of these branches:

### Branch A — original artifact is installed

Required:

- assembled-pack dedicated-server or equivalent authoritative NeoForge runtime reaches and completes the relevant registry initialization with the actual installed JAR;
- evidence must identify the pack/JAR hash used;
- absence of a crash must be tied to that startup, not inferred from a standalone build or unrelated server smoke without Traveloptics.

### Branch B — verified patched/replacement artifact is installed

Required:

- exact patched/replacement physical filename and hash;
- provenance sufficient to identify what changed;
- authoritative assembled-pack startup completing registry initialization with that exact artifact.

The exact patch candidate is now cryptographically fingerprinted and independently proven to differ from the original in only `TOLootModifiers.class`. The patch publisher states that this class delta corrects the universal codec registration. That still does not prove the user's pack deploys SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`, nor that the assembled modpack completes registry initialization with the actual deployed artifact.

Current state: `CONTEMPORANEOUS PHYSICAL-RUNTIME INITIALIZATION OBSERVED / PROCESS HASH NOT EMBEDDED / DISTINCT-CODEC PROBE STILL OPEN`.

### 2026-09-08 physical/runtime correlation — current physical line

Project Library now supplies a bounded same-instance/same-day pair:

- physical dump `modlist 08.09.2026.txt` at ~12:05 UTC: `traveloptics-4.4.0.1-1.21.1.jar`, SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`, fingerprint `4254006126`;
- assembled `debug(9).log` boot at ~12:19 UTC: Traveloptics container creation, config loading and event-handler subscription progress with no occurrence of the earlier `Adding duplicate value` / `Mod loading issue for:` path;
- later boot failure: `shine.mixins.json:ProgramMixin` shader injection, not a Traveloptics registration failure.

This materially closes the **existence of contemporaneous runtime initialization evidence** for the September physical line. It does **not** close process-embedded hash attestation, current exact spell-registry equality, exact serializer object identity, provenance or Blackout reachability.

Canonical detail: [`RUNTIME-2026-09-08-PHYSICAL-CORRELATION.md`](RUNTIME-2026-09-08-PHYSICAL-CORRELATION.md).
### Historical assembled-runtime observation — bounded

The 2026-08-19 Project Library runtime log reaches NeoForge mod discovery/resource reload with `traveloptics-4.4.0.1-1.21.1.jar` present and exposes the complete 33-ID Traveloptics spell block to the runtime analyzer. That narrows the historical startup risk: the observed August modified artifact progressed far enough for all 33 spell classes/IDs to be analyzed.

This remains **historical / hash-unbound evidence**. It neither proves the exact `TOLootModifiers` serializer objects nor ties the run to September SHA-1 `7b74816e...`; consequently Gate 2 remains open for the current physical artifact.

### Bounded runtime observation now available

The isolated `black_arcana_catalog_qa` companion can observe the public NeoForge `GLOBAL_LOOT_MODIFIER_SERIALIZERS` registry on `ServerStartedEvent` without loading or reflecting Traveloptics implementation classes.

For the exact assembled pack it emits only the bounded targets:

- `traveloptics:key_loot`;
- `traveloptics:universal_loot`;
- whether both resolved values are distinct object instances.

Canonical runbook: [`docs/qa/provider-catalog-runtime-registry-probe.md`](../../../../docs/qa/provider-catalog-runtime-registry-probe.md).

This does not create a PASS by itself. Gate 2 evidence must still pair the runtime rows with the deployed artifact hash/disposition from Gate 1.

For an exact patched/replacement artifact, a strong closure packet for this gate is:

1. physical hash classified as `PATCHED_EXACT` or another explicitly verified replacement;
2. assembled dedicated server reaches `ServerStartedEvent` with that exact artifact;
3. both serializer IDs emit `status=OBSERVED`;
4. the pair emits `status=OBSERVED distinct_codec_instances=true`.

For `ORIGINAL_EXACT`, successful startup and observed serializer rows are evidence to retain, but any result that conflicts with the already-audited duplicate-codec structure must be investigated rather than silently reclassified as fixed. The probe does not identify codec classes and does not prove loot-modifier behavior or Blackout acquisition.

## Gate 3 — `traveloptics:blackout` survival reachability

`traveloptics:blackout` is an exact registered spell identity in the audited publisher artifact and inherits `AbstractUniqueSpell.allowCrafting() = false`.

Unlike the other nine non-craftable Unique spells, the exact artifact audit found:

- no direct structured loot reference for `blackout`;
- no provider-owned reference to `TOSpells.BLACKOUT_SPELL` outside `TOSpells` itself.

The publisher's generic 1.21.1 statement that ported spells are obtainable in survival is not object-level evidence for this spell.

The current broad project page documents a Dead King → Blackout acquisition loop, and official 1.20.1 File `6010839` introduced `Blackout`, `Call Forth The Dead King` and the `Enraged Dead King` together. That is real publisher evidence for the full project/1.20.1 feature line, but not for the installed deprecated 1.21.1 alpha.

Exact File `6342780` evidence instead shows:

- `call_forth_the_dead_king` is residual localization-only content and absent from the exact 33-spell registry;
- the exact artifact's 41 loot/loot-modifier JSON resources expose no Enraged Dead King loot route;
- `blackout` remains registered, but no object-level structured acquisition route is present in the audited artifact.

See [`BLACKOUT-VERSIONED-ACQUISITION-BOUNDARY.md`](BLACKOUT-VERSIONED-ACQUISITION-BOUNDARY.md).

Therefore the broader Dead King route must not be projected into the installed alpha. This does not prove impossibility; it preserves the requirement for File-6342780-specific or actual-pack evidence.

Required closure evidence must establish an actual current-pack player path, such as an authoritative 1.21.1 provider/host route, progression grant, item/scroll source, scripted acquisition or runtime-observed survival mechanism that resolves specifically to `traveloptics:blackout`.

| Required field | Current state |
|---|---|
| exact acquisition mechanism | `NÃO VERIFICADO` |
| authoritative source/runtime evidence | `NÃO VERIFICADO` |
| prerequisite entity/structure/item/config | `NÃO VERIFICADO` |
| actual pack/world checkpoint | `NÃO VERIFICADO` |

Creative access, commands, registry presence, translation keys, generic publisher language, or the 1.20.1 Dead King acquisition loop do not close this 1.21.1 gate.

## Gate 4 — Somake Aqua ↔ T.O Aqua coexistence

Current physical authority confirms both providers are installed:

- Somake Spells `1.0.9`, with its current 83-ID registry closed;
- T.O Magic n' Extras `4.4.0.1-1.21.1`, physical SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

The exact publisher Traveloptics File `6342780` registers 33 spells and **zero Aqua spell IDs**. Its `aqua_focus.json` resource and residual Aqua localization are not active-registry proof. The installed Traveloptics bytes are nevertheless `OTHER_VERIFIED`, so exact-current Aqua absence cannot be projected from the publisher baseline.

Canonical authority boundary is now documented in Somake's [AQUA-TRAVELOPTICS-CURRENT-COEXISTENCE-CHECKPOINT.md](../✅-somake-spells/AQUA-TRAVELOPTICS-CURRENT-COEXISTENCE-CHECKPOINT.md):

- dual-installed coexistence: **PROVEN**;
- publisher-baseline Traveloptics Aqua registrations: **0 PROVEN**;
- duplicate current Aqua collision: **NOT PROVEN**;
- exact-current Traveloptics Aqua absence: **NOT PROVEN**;
- authority transfer/suppression/aliasing: **NOT AUTHORIZED BY ASSUMPTION**.

Current state: `CURRENT COEXISTENCE CONFIRMED / AQUA COLLISION+EXACT-CURRENT ABSENCE CONDITIONAL / FAIL-CLOSED`.

This remains an integration/authority gate only. It does not erase or add any of the 33 Traveloptics spell identities, and it does not justify a Black Arcana-created fallback Aqua school.

## Already closed — do not redo

The following work is already canonical and should not be repeated:

- 33 exact publisher-release registered spell identities enumerated;
- spell cards materialized under verified school membership;
- 32 residual localization-only IDs excluded;
- 10 `AbstractUniqueSpell` registrations identified;
- 2 `AbstractWeaponSpell` craftable registrations identified (`cursed_blast`, `gyro_slash`);
- nine non-craftable Unique spell structured loot routes identified;
- `blackout` isolated as the unresolved Unique reachability exception;
- structural `TOLootModifiers` codec mismatch recorded clean-room;
- 33/33 exact default mechanics baseline closed for File `6342780`;
- 29/29 selected numeric no-`LivingEntity` accessors closed across 18 spells with 0 UNKNOWN;
- 49 numeric LivingEntity-bearing methods classified: 15 ENTITY_UNUSED / 34 ENTITY_SLOT_READ;
- of the 15 ENTITY_UNUSED methods, 8 resolve exactly and 7 remain strict-evaluator UNKNOWN; no value is assigned to the 34 entity-reading methods or the 7 UNKNOWN methods;
- total exact resolved bounded accessor outputs now 37 across 24/33 spell cards; raw non-count units/final formulas remain intentionally unassigned.

## Acceptance boundary

Traveloptics remains `⚠️ Parcial / condicionado` until the relevant evidence above is closed.

No future checkpoint may claim strict semantic promotion or runtime compatibility merely because:

- the 33 registry IDs are known;
- a third-party patch exists on the internet;
- the publisher says spells are generally survival-obtainable;
- a build without the actual provider stack is green;
- exact File-6342780 default mechanics are known;
- selected File-6342780 range/radius/duration/count/health/damage-named accessor outputs are known;
- the version string matches the publisher release.

Any promotion must cite the exact physical artifact/runtime evidence and preserve Iron's/Traveloptics provider authority. Black Arcana must not silently repair the provider registry, invent a `blackout` acquisition route, or select an Aqua authority by assumption.
