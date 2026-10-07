# T.O Magic n' Extras 4.4.0.1-1.21.1 — Closure Checklist

Status: `33 REGISTERED SPELL IDS + EXACT PUBLISHER MECHANICS CATALOGED / CURRENT PHYSICAL PROMOTION BLOCKED / RUNTIME FAIL-CLOSED`

## Purpose

The current Traveloptics dossier already closes the exact publisher-release registry inventory at **33 registered spell identities**, excludes **32 residual localization-only spell IDs**, closes a 33/33 exact publisher mechanics baseline for base/per-level mana and spell-power inputs, cast type/time, max level, minimum rarity and default cooldown, and additionally closes **37 File-only bounded scalar accessor results across 24 spells**: 29 no-`LivingEntity` accessors plus 8 LivingEntity-signature methods proven entity-unused before strict evaluation. A separate provider/current-host bridge closes seven effective-cast-time delegates and expands numeric accessor/bridge coverage to **28/33** spell identities. Audit #658 now dependency-classifies **all 34/34 `ENTITY_SLOT_READ` numeric accessors** into 24 host-spell-power-only methods, 9 summon-damage methods additionally using Iron's `SUMMON_DAMAGE`, and 1 spell-power + `Math.min` method. Therefore **33/33 exact spell identities have at least one bounded numeric accessor result, host bridge or entity-dependent accessor contract documented**. Numeric closure remains 28/33. The remaining work is not another spell/default-stat enumeration, generic scalar sweep or generic entity-dependency sweep. It is a finite set of current-physical/runtime/acquisition evidence gates required before strict promotion can be considered.

This checklist does not promote the provider, does not treat a third-party patch as upstream authority, and does not infer survival acquisition or assembled-pack runtime from publisher marketing language.

## Gate 1 — Physical artifact identity / patch deployment

Current physical evidence establishes the installed version line and filename:

- observed installed filename: `traveloptics-4.4.0.1-1.21.1.jar`;
- latest sibling authority rechecked at `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a` (Traveloptics dossier blob `394abc11401526a4d2e6db5bd9af39bbc962e572`, unchanged from `b9edb403...`): `PROJECT-INSTRUCTIONS/modlist/Addons + Adventure and RPG + Armor, Tools, and Weapons + Magic + Mobs/✅-to-magic-n-extras v4.4.0.1-1.21.1.md` records physical row #550 with that filename/version/mod id and SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
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

**Gate 1 disposition checkpoint:** physical identity classification itself is closed at `OTHER_VERIFIED` (current SHA-1 `7b74816e...` is neither publisher original nor known patch). What remains open is the **provenance/content delta** of those verified replacement bytes and an exact-current registry/stat bridge. Schema 4 of the removable catalog QA probe now provides the required future process-bound bridge surface: it fingerprints the FML-loaded Traveloptics file by basename/size/SHA-1 in the same complete block that enumerates Traveloptics spell rows and Gate-2 serializers. This is especially relevant after #661 positively observed all 33 publisher-baseline IDs in the first-hash-day log family: a schema-4 run can bind a future exact registry observation to the file actually loaded by that process and can also expose any additional `traveloptics:` IDs. No such schema-4 physical-pack run is yet canonical evidence, so this infrastructure does not close Gate 1. The retained Aug-17 JAR metadata provides two local candidate artifacts by name/size, but current inventories do not preserve a physical file-size field for `7b74816e...`; size therefore cannot identify the current replacement. Do not infer registry equality, File-6342780 ancestry, identity with the retained Aug-17 `fixed-keyloot.jar`, or the known later patch fix from the unchanged nominal filename/version. The next gate is still to materialize/audit the exact `7b74816e...` bytes or obtain equivalent contemporaneous exact-content provenance.

Temporary NON-MERGE PR **#474** further tested whether the current SHA-1 can be reproduced by common one-entry repacks of publisher File `6342780` using the exact changed `TOLootModifiers.class` from patch File `8861368`. Run `36649716927` succeeded, and none of the tested Info-ZIP, `jar uf`, or Python `zipfile` variants matched `7b74816e...`. The recorded Aug-17 Library `fixed-keyloot.jar` size also matched none of those candidates. This is negative lineage evidence only: it excludes those exact repack outputs but does not identify the installed replacement or its registry/content delta.

Temporary NON-MERGE PR **#648** expands that bounded lineage family to **164** surgical outputs across Info-ZIP delete/add and direct-update modes, default vs `-X` extra fields, levels 0–9, four plausible replacement timestamps, and JDK `jar uf`. Dedicated run `37317446376` / job `111787652542` succeeded: **0/164** match physical SHA-1 `7b74816e...`, **0/164** match physical fingerprint `4254006126`, and **0/164** match the retained `fixed-keyloot.jar` size **18,393,641**. The closest family is **18,393,560 bytes** (delta -81). This further narrows, but does not close, provenance/content-delta Gate 1. See [`EXPANDED-SURGICAL-REPACK-AUDIT.md`](EXPANDED-SURGICAL-REPACK-AUDIT.md).

A 2026-10-05 bounded public-provenance search also found no indexed origin for the exact `7b74816e...` SHA-1, fingerprint `4254006126`, retained `fixed-keyloot` filename, or a public `Gustavaopere` repository script/commit establishing the replacement build. The related public patch File `8861368` remains the only surfaced published repair and is already excluded by hash and chronology. This does not prove that no public/local provenance exists; it closes only repeated generic public-search work. Gate 1 now requires pack-local exact bytes/checksums/provenance or equivalent exact-current content attestation. See [`PUBLIC-PROVENANCE-SEARCH-BOUNDARY-2026-10-05.md`](PUBLIC-PROVENANCE-SEARCH-BOUNDARY-2026-10-05.md).

A separate Project Library runtime checkpoint from **2026-08-19** proves that the assembled pack discovered the same nominal filename/version and that its runtime spell analyzer emitted exactly **33 unique `traveloptics:` spell IDs**, equal as a set to the File-6342780 33-ID baseline, including `traveloptics:blackout`. A direct physical inventory only three days later, on **2026-08-22**, records SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`.

The retained chronology is therefore: Aug-16 repeated duplicate-codec assembled-runtime crashes -> Aug-17 local repair artifacts -> immediate post-repair NeoForge process discovers the canonical `traveloptics-4.4.0.1-1.21.1.jar` from the real instance `mods` directory and progresses past the former fatal registration stage into Traveloptics resource reload -> Aug-18 launcher `isModified=true` -> Aug-19 33-ID runtime observation -> Aug-22 first direct `7b74816e...` hash capture. The canonical-slot discovery occurs approximately 73 seconds after the retained Library timestamp for `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar`; this strongly narrows the repair episode but does **not** prove that the candidate was copied/renamed into the canonical slot or that either Aug-17/Aug-19 process used the exact Aug-22 bytes. See [`RUNTIME-2026-08-17-POST-REPAIR-CORRELATION.md`](RUNTIME-2026-08-17-POST-REPAIR-CORRELATION.md). Gate 1 remains open.

### 2026-08-22 first-hash-day runtime registry correlation — current physical line

Project Library now provides a second current-line temporal bridge on the date of the **first direct** `7b74816e...` physical capture:

- physical inventory `fcb79de3-0e3e-41af-8136-cd524859f71c.txt` records the canonical JAR at SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4` / fingerprint `4254006126`;
- two same-day assembled debug logs, `debug(20260822-184009).log` and `debug(20260822-185838).log`, expose Traveloptics spell registrations to the runtime attribute layer shortly afterward;
- the original bounded retrieval pass positively surfaced 25/33 publisher-baseline IDs, including `traveloptics:blackout`;
- a 2026-10-06 targeted retrieval of the previously unsurfaced eight IDs now finds direct `Registered attribute [spell/traveloptics/<id>]` lines for **all eight**, so the first-hash-day log family positively observes **all 33/33 publisher-baseline IDs**.

This materially strengthens the current-line registry correlation because it occurs on the first hash-capture day. It remains **process-hash-unbound**: neither Java process reports the SHA-1, no immutability between inventory and process is proven, and the positive 33/33 inclusion result does **not** exclude additional current-runtime Traveloptics spell IDs. Exact-current set equality therefore remains open.

Canonical detail: [`RUNTIME-2026-08-22-FIRST-HASH-REGISTRY-CORRELATION.md`](RUNTIME-2026-08-22-FIRST-HASH-REGISTRY-CORRELATION.md).

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

Current state: `HISTORICAL DUPLICATE-CODEC FAILURE REPRODUCED / CONTEMPORANEOUS CURRENT-LINE INIT OBSERVED / PROCESS HASH NOT EMBEDDED / DISTINCT-CODEC PROBE STILL OPEN`.

### 2026-08-16 assembled-runtime failure reproduction — historical pre-repair state

Project Library preserves four independent 2026-08-16 crash reports under the canonical filename `traveloptics-4.4.0.1-1.21.1.jar`. Each attributes the Traveloptics mod-loading failure to `RegisterEvent` and records `IllegalStateException: Adding duplicate value ... to registry`, where the duplicated codec is a `KeyLootModifier` `RecordCodec`.

This is direct assembled-pack reproduction of the failure mode predicted by the exact File-6342780 `TOLootModifiers` structure. The crash reports do not embed a JAR SHA-1, so they are **historical / process-hash-unbound** evidence and cannot be projected onto current `7b74816e...` bytes.

Canonical detail: [`RUNTIME-2026-08-16-LOOT-CODEC-CRASH.md`](RUNTIME-2026-08-16-LOOT-CODEC-CRASH.md).

### 2026-08-17 immediate post-repair canonical-slot correlation — historical

Project Library retains a separately named `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar`, followed approximately 73 seconds later by a NeoForge `ModDiscoverer` event that discovers the canonical `traveloptics-4.4.0.1-1.21.1.jar` from the real CurseForge instance `mods` directory. That same process progresses through Traveloptics configuration/event initialization and reaches provider resource reload, unlike the immediately preceding canonical-slot processes that terminate during `RegisterEvent` with the duplicate `KeyLootModifier` codec.

This is strong post-repair canonical-slot runtime evidence but remains **historical / process-hash-unbound**. It does not prove identity with the retained `fixed-keyloot.jar` candidate or current SHA-1 `7b74816e...`, and it does not directly observe the target serializer object pair.

Canonical detail: [`RUNTIME-2026-08-17-POST-REPAIR-CORRELATION.md`](RUNTIME-2026-08-17-POST-REPAIR-CORRELATION.md).

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

This does not create a PASS by itself. Schema 4 can now perform that pairing inside one complete exact-pack probe block: `type=mod_file id=traveloptics status=OBSERVED ... sha1=<deployed hash>` plus the spell-registry and serializer rows/pair. Gate 2 remains open until an authoritative physical-pack run actually records the expected hash, both serializer IDs as `OBSERVED`, and `distinct_codec_instances=true`.

For an exact patched/replacement artifact, a strong closure packet for this gate is:

1. physical hash classified as `PATCHED_EXACT` or another explicitly verified replacement;
2. the same complete schema-4 probe block emits `type=mod_file id=traveloptics status=OBSERVED` with that exact artifact SHA-1;
3. assembled dedicated server reaches `ServerStartedEvent` with that exact artifact;
4. both serializer IDs emit `status=OBSERVED`;
5. the pair emits `status=OBSERVED distinct_codec_instances=true`.

For `ORIGINAL_EXACT`, successful startup and observed serializer rows are evidence to retain, but any result that conflicts with the already-audited duplicate-codec structure must be investigated rather than silently reclassified as fixed. The probe does not identify codec classes and does not prove loot-modifier behavior or Blackout acquisition.

A bounded 2026-10-05 Project Library indexed-log search did **not** surface preserved post-repair rows directly observing both serializer IDs or `distinct_codec_instances=true`; it did resurface the historical duplicate-`KeyLootModifier` failure. Because indexed-search misses are not raw-log absence evidence, this does not close Gate 2. It does close repeated generic preserved-log keyword searching as a productive path: the next authoritative evidence is the canonical physical-pack registry probe. See [`GATE2-PRESERVED-LOG-SEARCH-BOUNDARY-2026-10-05.md`](GATE2-PRESERVED-LOG-SEARCH-BOUNDARY-2026-10-05.md).

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

A focused generic-loot audit now further proves for File `6342780`:

- Blackout ancestry has `allowLooting() = false` through `AbstractUniqueSpell`;
- 23 exact `spell_filter` / `randomize_spell` nodes were inspected;
- no forced Eldritch filter exists;
- no explicit spell list contains Blackout;
- no provider class references host `SpellFilter` or `RandomizeSpellFunction`;
- `BLACKOUT_SPELL` remains registry-only in provider code.

Under the pinned Iron's 3.16.3 host contract, this excludes the exact alpha's provider-owned built-in generic random-spell loot route as well as the already-absent direct structured route. See [`BLACKOUT-GENERIC-LOOT-EXCLUSION.md`](BLACKOUT-GENERIC-LOOT-EXCLUSION.md).

See [`BLACKOUT-VERSIONED-ACQUISITION-BOUNDARY.md`](BLACKOUT-VERSIONED-ACQUISITION-BOUNDARY.md).

Therefore the broader Dead King route must not be projected into the installed alpha. The exact alpha's provider-owned direct and generic loot surfaces are now excluded, but this does not prove impossibility in the assembled pack; external/current-physical routes remain open.

Required closure evidence must establish an actual current-pack player path, such as an authoritative 1.21.1 provider/host route, progression grant, item/scroll source, scripted acquisition or runtime-observed survival mechanism that resolves specifically to `traveloptics:blackout`.

| Required field | Current state |
|---|---|
| exact File-6342780 provider loot mechanism | `EXCLUDED — direct + built-in generic` |
| actual current-pack acquisition mechanism | `NÃO VERIFICADO` |
| authoritative source/runtime evidence | `NÃO VERIFICADO` |
| prerequisite entity/structure/item/config | `NÃO VERIFICADO` |
| actual pack/world checkpoint | `NÃO VERIFICADO` |

Creative access, commands, registry presence, translation keys, generic publisher language, or the 1.20.1 Dead King acquisition loop do not close this 1.21.1 gate.

### Retained literal/object-specific route search — negative preservation evidence

A 2026-10-05 bounded search checked the currently retained external acquisition surfaces outside Traveloptics itself for literal/object-specific Blackout routes.

- Black Arcana contains Traveloptics references in the isolated `src/catalogQaProbe` runtime evidence source. That code was inspected and is observational only: it reports mod presence and the bounded `traveloptics:key_loot` / `traveloptics:universal_loot` serializer registry targets; it does not grant spells, build loot tables, add recipes or implement acquisition.
- After excluding that QA-only surface, no literal/object-specific Blackout acquisition route was identified in the searched Black Arcana/sibling versioned surfaces.
- Project/Library semantic search for `traveloptics:blackout`, Blackout+Traveloptics, server scripts, global loot modifiers and datapack surfaces returns runtime logs, modlists or catalog/project documentation rather than a retained acquisition source.
- Retained Library `.js` / `.json` / `.toml` inventory dated 2026-08-15 through 2026-10-05 with KubeJS/server/startup-script/datapack/data/loot/Traveloptics/Blackout path-name markers contains **0 preserved source artifacts**.

A current-tree follow-up excludes the specifically named `SpellFilter` / `RandomizeSpellFunction` route and the inspected GLM/progression/script/resource surfaces. A later reproducible full-`src/main` audit on Black Arcana `da8a5c18...` and sibling `de80b186...` additionally scanned 482 + 1,144 Java files and 22 + 724 resource blobs, respectively. It found zero uses of the audited direct Iron's scroll/spell-container construction/lookup surfaces (`createScrollContainer`, `createImbuedContainer`, `ISpellContainer.set`, `addSpell*`, `SPELL_CONTAINER`, `ItemRegistry.SCROLL`, `SpellDataRegistryHolder`, `new SpellData`, `SpellRegistry.getSpell`) and zero resource tokens for Traveloptics/Blackout/Iron's scroll/spell-container. Reviewed generic item/reward candidates resolve to Malum refunds/equipment reads, Compendium preview, GameTests, point/XP rewards, existing-loot scaling and Battle Mage casts of existing `SpellData`, not a Blackout grant. See [`BLACKOUT-VERSIONED-GENERIC-ROUTE-AUDIT.md`](BLACKOUT-VERSIONED-GENERIC-ROUTE-AUDIT.md) and [`BLACKOUT-VERSIONED-ACQUISITION-SURFACE-AUDIT.md`](BLACKOUT-VERSIONED-ACQUISITION-SURFACE-AUDIT.md).

This still does **not** exclude a generic route in the actual assembled instance. External physical KubeJS folders, user/world datapacks, other installed mods and current physical Traveloptics `7b74816e...` content are not authoritatively captured here. Those assembled-pack surfaces remain **UNRESOLVED**.

Canonical detail: [`BLACKOUT-EXTERNAL-ROUTE-RETAINED-EVIDENCE-CHECKPOINT.md`](BLACKOUT-EXTERNAL-ROUTE-RETAINED-EVIDENCE-CHECKPOINT.md).

Gate 3 therefore remains open. Literal-ID searches, the named filter/GLM/progression/script/resource surfaces, and the audited direct Iron's construction/lookup + generic item/reward candidates need not be repeated on the pinned refs. The current versioned repositories are still **not universally cleared of reflection/encoded/dynamic or semantically equivalent unenumerated acquisition logic**. Strong next evidence is now an authoritative assembled physical script/datapack/other-mod capture, exact-current Traveloptics content, or a concrete runtime/world acquisition checkpoint.


### Deployed collector support — current-instance candidate capture

The canonical read-only deployed-evidence collector now covers the remaining bounded filesystem discovery surface without claiming reachability:

- the installed `traveloptics-4.4.0.1-1.21.1.jar` row reports explicit equality against current known physical SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- exact `traveloptics:blackout` references are searched across `kubejs/startup_scripts`, `kubejs/server_scripts`, `kubejs/data`, FTB Quests config/defaultconfigs and discovered/explicit world datapacks, including text-like ZIP entries;
- the same surfaces are searched for the already-audited generic host markers `SpellFilter`, `RandomizeSpellFunction`, `spell_filter` and `randomize_spell`;
- output retains only source label, relative path, line number and matched literal. Script, quest and datapack bodies are not copied.

This is evidence-discovery infrastructure only. A positive generic marker still requires inspection to determine whether it can resolve to Blackout; a zero-marker result narrows the named generic-filter path but does not exclude reflection, encoded/dynamic logic, semantically equivalent custom code, other mods, or world-state acquisition. Gate 3 remains fail-closed until an authoritative current-instance capture is reviewed under the acceptance boundary below.

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
- of the 15 ENTITY_UNUSED methods, 8 resolve as File-only scalars and the remaining 7 are proven direct delegates to host `getCastTime(level)` by audit #619;
- the seven direct delegates resolve under the current Iron's 3.16.3 host contract to 50/39/45/15/25/20/10 ticks, but remain separate from the File-only scalar denominator;
- File-only exact resolved bounded accessor outputs remain 37 across 24/33 spell cards; numeric accessor/host-bridge coverage touches 28/33;
- all 34/34 `ENTITY_SLOT_READ` numeric accessors are dependency-classified by audit #658: 24 host-spell-power-only, 9 additionally using Iron's `SUMMON_DAMAGE` attribute surface, and `AerialCollapseSpell.getDamage` additionally calling `Math.min(float,float)`; no reconstructed formula or entity-independent numeric result is assigned;
- the earlier five identity-gap classifications from audit #623 remain valid as a historical subset;
- identity-level accessor/bridge/dependency coverage therefore touches 33/33, while all 34 entity-reading methods remain numerically entity/config conditional.

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
