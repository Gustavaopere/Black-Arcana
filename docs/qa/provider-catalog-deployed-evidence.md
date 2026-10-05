# Provider catalog — deployed evidence collector

Status: `SUPPORTING QA TOOL / READ-ONLY / DOES NOT CREATE CATALOG PASS BY ITSELF`

## Purpose

The remaining conditional-provider blockers are increasingly tied to the **actual assembled pack** rather than missing source enumeration.

`provider-catalog-deployed-evidence-collector.py` provides one bounded, read-only collection step for:

- Asterism Arcanum 0.1.0;
- Gaze 1.1.7.1;
- Not Enough Glyphs 4.6.2;
- Corail Tombstone 9.5.6;
- Somake Spells 1.0.9;
- Mowzie's Mobs 1.8.2;
- ShadowsZ 1.1.9;
- Simply Swords: Cataclysm 1.0.2+1.21.1+neoforge;
- T.O Magic n' Extras / Traveloptics 4.4.0.1 — current physical override/provider blocker even though it is absent from the sibling status-prefixed taxonomy;
- bounded deployed customization references relevant to those same closure gates.
- kubejsarsnouveau 1.3.2 physical JAR fingerprint against the current pack SHA-1;
- exact current KubeJS startup/server/client/data text-file inventory by relative path, SHA-256, byte size and surface label, without copying file bodies.

It does not alter the instance, generate provider configs, enable content, create datapacks, or infer defaults from absent files.

## Requirements

- Python 3.11+;
- local access to the **actual modpack instance** being used for catalog closure;
- optional access to the actual world directory if it is outside the instance's normal `saves/` or `world/` paths.

No network access is required.

## Run

From the Black Arcana repository root:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance"
```

If the authoritative world lives elsewhere:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance" \
  --world "/path/to/server/world"
```

Multiple `--world` arguments are allowed.

Default output:

`provider-catalog-deployed-evidence.json`

If `<instance>/logs/latest.log` contains a completed `[BLACK_ARCANA_CATALOG_PROBE]` block, the collector also folds that block into the JSON using a strict field whitelist. To point at a different log without copying it into the instance:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance" \
  --probe-log "/path/to/server/logs/latest.log"
```

Raw log text is never retained in the report.

Custom output:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance" \
  --output "/safe/path/provider-catalog-deployed-evidence.json"
```

## What the collector records

### KubeJS script/data inventory

The report includes `kubejs_script_inventory` with:

- whether the instance has a `kubejs/` root at all;
- total bounded file count;
- per-surface counts for `startup_scripts`, `server_scripts`, `client_scripts` and `data`;
- for each collected text file: relative path, surface label, SHA-256 and byte size.

Only files under those four roots whose suffix is already in the collector's bounded text-extension allowlist are included. Script/data bodies are never copied.

For files that contain high-confidence **Iron's Spellbooks KubeJS review markers**, the per-file row may additionally include `irons_spellbooks_kubejs_markers`. The value is a fixed marker-type → 1-based line-number-list map; at most 64 line numbers are retained per marker type, with `irons_spellbooks_kubejs_markers_truncated=true` when that cap is exceeded.

The fixed marker vocabulary is:

- `spell_registry_literal` — exact `irons_spellbooks:spells` registry literal;
- `school_registry_literal` — exact `irons_spellbooks:schools` registry literal;
- `spell_registry_key_binding` — `SpellRegistry.SPELL_REGISTRY_KEY`;
- `school_registry_key_binding` — `SchoolRegistry.SCHOOL_REGISTRY_KEY`;
- `iss_event_bridge` — `ISSEvents.*` bridge usage;
- `irons_spells_js_builder_literal` — quoted addon builder literals for core `spell`, `magic_sword`, `staff`, `spellbook` in either the official short form or `irons_spells_js:`-prefixed form, plus namespaced EntityJS `spellcasting` / `spell_projectile`.

The spell/school literals are grounded in Iron's Spells 3.11.0 source (`216d675627004562bc540b618b77600009cd6ee1`), which is the host baseline declared by the exact Iron's Spellbooks KubeJS 4.0.3 source pin. Marker rows contain no script bodies or matched text. The exact addon checkpoint `f3c05a102707a87ac3b8f0d2df5d2ffa5ae5b6c7` also ships development fixtures under `run/kubejs/` that exercise the short core builder literals; those fixture scripts validate syntax only and are not modpack content.

These markers are **triage only**. Comments, dead branches and lookup-only references may produce markers; aliases/dynamic construction may evade them. Presence is not proof of a live registration, and absence is not zero-content proof. The hashed source file or assembled-registry provenance still requires review under the provider checklist.


This inventory is evidence input for Iron's Spellbooks KubeJS deployed-instance parity review and the KubeJS Ars Nouveau closure/reachability checklist. For Iron's Spellbooks KubeJS, catalog status is already `✅ / +0` from exact provider-source closure plus the 2026-10-05 project-owner authored-content attestation; the inventory now corroborates deployment parity or triggers a catalog reopen. A non-empty inventory still requires targeted script/provenance review; hashes and paths alone do not prove semantic registrations or recipe mutations.

### Iron's Spellbooks KubeJS 4.0.3 physical fingerprint

The collector hashes only the exact current filename:

`irons_spells_js-4.0.3.jar`

and emits `current_physical_4_0_3_equality` against canonical current-pack SHA-1:

`0481395c5847e2920d1425e77833bef87df63139`.

This proves only that the assembled instance contains the certified current physical bridge artifact. It does not prove source-build byte equivalence and it does not establish whether pack scripts register custom Iron's spells, schools or items.

Pair this fingerprint with both exact current host fingerprints — Iron's Spellbooks 3.16.3 and KubeJS build 377 — plus `kubejs_script_inventory` from the same assembled instance. Provider-binary equality alone is not sufficient for deployed-instance parity review.

### Current Iron's Spellbooks host 1.21.1-3.16.3 physical fingerprint

The collector hashes only the exact current filename:

`irons_spellbooks-1.21.1-3.16.3.jar`

and emits `current_physical_3_16_3_equality` against canonical current-pack SHA-1:

`017fd8140c477f9ae602cf95594f1c23bef1d6e3`.

This is a same-instance host-identity gate for Iron's Spellbooks KubeJS deployed-instance parity review. The addon executes against Iron's registries, config and casting semantics, so zero-content/script-review routing is not valid when the assembled instance carries a different or unverified Iron's host.

### Current KubeJS host 2101.7.2-build.377 physical fingerprint

The collector hashes only the exact current filename:

`kubejs-neoforge-2101.7.2-build.377.jar`

and emits `current_physical_build_377_equality` against canonical current-pack SHA-1:

`150c5d6efc09b969ac350ea205128dff832e0850`.

This is a same-instance freshness gate for Iron's Spellbooks KubeJS deployed-instance parity review. It prevents a historical or otherwise different KubeJS host — including the previously observed build 374 instance — from being routed as a current zero-content review candidate merely because `irons_spells_js-4.0.3.jar` also exists there.

The report also emits `irons_spellbooks_kubejs_closure`, a fail-closed evidence-routing state:

- `ARTIFACT_NOT_OBSERVED` — the exact Iron's Spellbooks KubeJS artifact was not captured;
- `ARTIFACT_HASH_MISMATCH` — the provider artifact was captured but does not match the certified 4.0.3 SHA-1;
- `IRONS_HOST_NOT_OBSERVED` — the certified provider artifact was captured but the exact current Iron's 3.16.3 host artifact was not;
- `IRONS_HOST_HASH_MISMATCH` — the Iron's 3.16.3 filename was captured but its SHA-1 does not match the current physical checkpoint;
- `KUBEJS_HOST_NOT_OBSERVED` — the certified provider and Iron's host were captured but the exact current KubeJS build 377 artifact was not;
- `KUBEJS_HOST_HASH_MISMATCH` — the build-377 filename was captured but its SHA-1 does not match the current physical checkpoint;
- `ZERO_CONTENT_REVIEW_CANDIDATE` — provider + both hosts are certified and the bounded KubeJS inventory contains zero files;
- `SCRIPT_REVIEW_REQUIRED` — provider + both hosts are certified and the bounded KubeJS inventory contains one or more files.

The closure object also records `artifact_certified`, `irons_host_certified`, `kubejs_host_certified`, KubeJS-root presence, bounded file count, marker-file count and sorted marker types. These are evidence workflow states, not catalog statuses. For Iron's Spellbooks KubeJS, `ZERO_CONTENT_REVIEW_CANDIDATE` corroborates the already-closed `✅ / +0` catalog state when provenance is valid; `SCRIPT_REVIEW_REQUIRED` requires exact review and any discovered Iron's spell/school registration reopens the catalog.

### KubeJS Ars Nouveau 1.3.2 physical fingerprint

The collector hashes only the exact current filename:

`kubejsarsnouveau-1.3.2.jar`

and emits `current_physical_1_3_2_equality` against canonical current-pack SHA-1:

`f39f4f409e628731be551fd961fac2964768d358`.

This closes physical artifact identity only when run against the authoritative assembled instance. It does not prove source-build byte equivalence, because the publisher's public 1.3.x repository line does not expose a commit whose Gradle metadata declares 1.3.2.

Pair the fingerprint with `kubejs_script_inventory` and the provider checklist at `wiki/modpack-catalog/providers/✅-kubejs-ars-nouveau/`. The audited bridge is a recipe-schema adapter: script inventory is used to close recipe/acquisition mutations, not to manufacture ownership of glyph implementations.


### Catalog runtime probe bundle

When a runtime-probe log is available, the collector scans it line-by-line. It accepts the exact prefix:

`[BLACK_ARCANA_CATALOG_PROBE]`

only in one of two forms:

- a pre-filtered line begins directly with the prefix; or
- a raw FML `latest.log` line has the exact companion logger field `dev.gustavopere.blackarcana.qa.catalog.CatalogRuntimeEvidence` immediately before the message.

Suffix-like text is not sufficient. Embedded occurrences — including chat/player text such as `x]: [BLACK_ARCANA_CATALOG_PROBE] ...` — are rejected and counted without retaining their contents.

It keeps only the **last complete** `type=begin ... type=end` block. Incomplete/stale trailing blocks are not promoted over an earlier complete run.

The parser accepts only the bounded fields emitted by the QA companion:

- verified target mod IDs and boolean loaded state;
- target Iron's spell IDs, school, `enabled`, `allow_crafting` and bounded failure status;
- target namespace registered counts;
- the exact 39 canonical Not Enough Glyphs candidate IDs with runtime registration/effective `enabled` state;
- Traveloptics `key_loot` / `universal_loot` serializer presence;
- Traveloptics serializer-pair status and distinct-object boolean.

Probe schemas `1`, `2` and `3` are accepted. Schema 3 adds bounded Not Enough Glyphs `type=glyph` rows while retaining backward compatibility with earlier probe logs. Unknown row types, unknown provider IDs, malformed booleans/counts/resource locations and unrecognized fields are not copied into the report. The output records only a relative/source label, parser status, schema, structured rows, a count of malformed/unrecognized prefixed rows, and a separate count of embedded-prefix rows rejected before parsing.

Possible parser states:

- `COMPLETE` — at least one complete **supported** probe block was found; the last complete block is retained;
- `UNSUPPORTED_SCHEMA` — the last complete block declares a probe schema newer/unknown to this collector; its rows are discarded fail-closed;
- `NO_COMPLETE_BLOCK` — prefixed rows exist but no complete begin/end block closed;
- `NO_PROBE_ROWS` — the selected log exists but contains no probe prefix;
- `NOT_FOUND` — no selected/default log exists;
- `READ_ERROR` — the selected log could not be read.

This bundle is still evidence input. A `COMPLETE` block does not promote any provider automatically.

### Physical JAR fingerprints

For the known current filenames it records:

- filename;
- SHA-1;
- SHA-256;
- byte size.

Special comparisons:

- Asterism Arcanum 0.1.0 is compared against the current physical sibling SHA-1 `4a25ba80116168ddcc812f71467c0598127e774a`;
- Somake 1.0.9 is compared against exact release SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- Traveloptics is classified against:
  - original SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8`;
  - exact patch candidate SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`;
- Gaze 1.1.7.1 is compared against exact known artifact SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041`;
- Not Enough Glyphs 4.6.2 is compared against exact publisher-release SHA-1 `32eea2c478a346ee7499f6a0db156241116f73e9`;
- Corail Tombstone 9.5.6 is compared against exact publisher-release SHA-1 `d830d16caa20b0d23a44ed6b1d339bc22afc2460`;
- Mowzie's Mobs 1.8.2 is compared against the exact current physical/publisher SHA-1 `d64475cd77444b056ece6472c79d40293dc63c6c`;
- ShadowsZ 1.1.9 is compared against the exact current physical/publisher SHA-1 `f946eb3a8181e1964279f163f430ccbba6c4edcd`;
- Simply Swords: Cataclysm 1.0.2 is compared against current physical SHA-1 `a2aa0f82ae3a9be2f43a4d47b3cb2201dd4e1469`.
- Simply Swords 1.70.2 is compared against the exact current physical/publisher SHA-1 `05b074ff774467f1fe9fb5592151b7845c321cbc`.

A missing file is not converted into a replacement identity.

### Asterism Arcanum

The JAR hash entry is compared against the current physical sibling SHA-1 `4a25ba80116168ddcc812f71467c0598127e774a`. This verifies that collected config evidence came from an instance carrying the same Asterism artifact fingerprint as the current modlist checkpoint; it does not replace the deployed config gate below.

Reads only the Iron's spell-config values required by the Astral Gateway checklist:

- `irons_spellbooks:enabled`;
- `irons_spellbooks:school`;
- `irons_spellbooks:allow_crafting`.

Targets:

- `config/irons_spellbooks_spell_config/asterismarcanum/astral_gateway.json`;
- `config/irons_spellbooks_spell_config/global_config.json`;
- world datapack override `data/asterismarcanum/irons_spellbooks_spell_config/astral_gateway.json`, including direct files and ZIP datapacks;
- KubeJS datapack override `kubejs/data/asterismarcanum/irons_spellbooks_spell_config/astral_gateway.json`.

Absence is reported as absence. The collector does **not** substitute Iron's defaults and does not claim to enumerate every possible third-party datapack loader.

### Gaze

Searches the bounded config roots for the exact key:

`disableGazeRites`

Roots:

- `config/`;
- `defaultconfigs/`;
- every discovered/explicit world `serverconfig/`.

Only the matching line, relative path and line number are retained.

A `defaultconfigs` match is template evidence only and does not outrank an actual world/server config.

### Not Enough Glyphs

Checks the exact 39 relative SERVER config paths already listed in:

`wiki/modpack-catalog/providers/⚠️-not-enough-glyphs/DEPLOYED-CONFIG-CHECKLIST.md`

For each observed file, the collector parses TOML and emits only:

`[general].enabled`

It checks:

- `config/`;
- `defaultconfigs/`;
- discovered/explicit world `serverconfig/`.

The catalog must resolve precedence from the actual deployed environment. A template file is not automatically the effective world value.

When a schema-3 runtime probe block is available from the same exact assembled server, the collector may also retain `type=glyph` rows for **only** those 39 canonical IDs. `status=OBSERVED enabled=<bool>` is direct runtime evidence of the effective Ars `AbstractSpellPart.isEnabled()` value after SERVER config loading; `NOT_REGISTERED` and `HOST_VALUE_UNAVAILABLE` remain fail-closed. This runtime route can replace manual TOML precedence reconstruction for the enabled-state gate of an observed candidate, but it does not prove unrelated Binder/protection/balance behavior.

### Corail Tombstone

The collector reads only the **12 Tombstone `AllowedMagicItems` booleans that currently block semantic closure**:

- `allow_tablet_of_assistance`;
- `allow_tablet_of_cupidity`;
- `allow_tablet_of_guard`;
- `allow_tablet_of_home`;
- `allow_tablet_of_recall`;
- `allow_gemstone_of_familiar`;
- `allow_gemstone_of_guardian`;
- `allow_gemstone_of_merchant`;
- `allow_grave_key`;
- `allow_lost_tablet`;
- `allow_magic_scroll`;
- `allow_scroll_of_knowledge`.

Roots are deliberately bounded to:

- `config/`;
- `defaultconfigs/`;
- every discovered/explicit world `serverconfig/`.

Only matching key paths, boolean values, relative file paths and parser status/error are retained. The collector does **not** copy the surrounding Tombstone config.

`defaultconfigs` remains template evidence only. If multiple observations exist, the catalog reviewer must resolve actual deployed precedence from the instance/world that generated the report.

These values close only the **provider eligibility/config** part of Tombstone's remaining magic-item candidates. They do not automatically decide semantic deduplication, acquisition, use reachability, runtime settlement or whether a candidate should enter the strict numerator.

### Mowzie's Mobs

The collector hashes the exact current filename:

`mowziesmobs-1.21.1-1.8.2.jar`

and emits `current_physical_1_8_2_equality` against canonical SHA-1 `d64475cd77444b056ece6472c79d40293dc63c6c`.

It also searches only the bounded config roots:

- `config/`;
- `defaultconfigs/`;
- discovered/explicit world `serverconfig/`;

for the exact key:

`enable_tunneling`

The catalog acceptance rule is provider-specific. A matching physical fingerprint plus an authoritative effective deployed value of `tools_and_abilities.earthrend_gauntlet.enable_tunneling` resolves the current catalog blocker. `true` promotes Tunneling into the strict semantic numerator; `false` closes it as deployed-disabled with no semantic delta. Missing/ambiguous precedence remains fail-closed.

See [`wiki/modpack-catalog/providers/⚠️-mowzies-mobs/DEPLOYED-CONFIG-CHECKLIST.md`](../../wiki/modpack-catalog/providers/⚠️-mowzies-mobs/DEPLOYED-CONFIG-CHECKLIST.md).

### Ice And Fire Community Edition

The collector hashes the exact current filename:

`iceandfire-2.1.2.jar`

and emits `release_2_1_2_equality` against canonical SHA-1 `0786f4142b7cabd958688f68beef3e63e9c0ae8b`.

For the remaining Ghost Sword gate, it reads only the exact provider-native Jupiter file:

`config/iceandfire/iaf-common.json`

and only the nested key:

`tools.phantasmalBladeAbility`

The report emits the relative path, exact key path, a bounded status and the boolean value only when it is actually present and boolean. A same-named key outside `tools` is ignored. Missing files/keys, malformed JSON and invalid value types stay explicit fail-closed states; the collector never substitutes the source default.

This evidence can promote Ghost Sword only when it comes from the actual current instance, the physical JAR matches 2.1.2, the observed value is `true`, and no overriding runtime gate is found. Dread Lich Staff acquisition is already closed separately by current-pack NeoForge 21.1.250 runtime audit `36327488231`; this collector is not its evidence path.

See [`wiki/modpack-catalog/providers/⚠️-ice-and-fire-ce/DEPLOYED-CONFIG-AND-REACHABILITY-CHECKLIST.md`](../../wiki/modpack-catalog/providers/⚠️-ice-and-fire-ce/DEPLOYED-CONFIG-AND-REACHABILITY-CHECKLIST.md).

### ShadowsZ

The collector hashes the exact current filename:

`shadowsz-1.1.9.jar`

and emits `current_physical_1_1_9_equality` against canonical physical/publisher SHA-1 `f946eb3a8181e1964279f163f430ccbba6c4edcd`.

For the semantic reachability gate it records only:

- exact-key observations for `fusionEnabled` under bounded `config/`, `defaultconfigs/`, and discovered/explicit world `serverconfig/` roots;
- the saved-world boolean gamerule `shadowszRestrictPowers` from `level.dat -> Data -> GameRules`.

The NBT reader is read-only and emits only the target gamerule's bounded status/value plus relative world/file labels. It does not retain the rest of `level.dat`, world seed, player data, coordinates, or unrelated gamerules.

A `defaultconfigs` observation is template evidence only. For the gamerule, missing world files, missing keys, malformed NBT, or non-boolean string values stay explicit fail-closed states. Capture should be taken from the authoritative current world after its state has been saved; do not substitute the exact-artifact defaults.

Acceptance remains provider-specific:

- matching 1.1.9 fingerprint + effective `shadowszRestrictPowers=false` allows the nine non-Fusion roots to become normally reachable;
- `fusionEnabled=true` admits Fusion as the tenth root, while `false` closes Fusion as deployed-disabled;
- `shadowszRestrictPowers=true` keeps normal-player strict contribution at +0 unless a separate authoritative non-operator grant route is deployed and evidenced.

See [`wiki/modpack-catalog/providers/⚠️-shadowsz/DEPLOYED-STATE-CHECKLIST.md`](../../wiki/modpack-catalog/providers/⚠️-shadowsz/DEPLOYED-STATE-CHECKLIST.md).

### Simply Swords: Cataclysm

The collector hashes the exact current filename:

`simplycataclysm-1.0.2+1.21.1+neoforge.jar`

and emits `current_physical_1_0_2_equality` against canonical physical SHA-1 `a2aa0f82ae3a9be2f43a4d47b3cb2201dd4e1469`.

It then reads only the exact NeoForge STARTUP file:

`config/simplycataclysm-startup.toml`

and retains only these catalog-closure keys:

- `accursedRageChance`;
- `blazingBrandChance`;
- `mechaPulseChargeChance`;
- `mechaSmiteHarmfulEffectsChance`;
- `mechaSmiteFireDuration`;
- `mechaSmiteWitherDuration`;
- `mechaSmiteRegenChance`;
- `mechaSmiteRegenUsesPercentage`;
- `mechaSmiteRegenPercentage`;
- `mechaSmiteRegenThreshold`.

For every key the report retains only the bounded status, TOML key path and value. Missing files, parse failures, missing keys or ambiguous duplicate keys stay explicit fail-closed states. No other Simply Cataclysm config values or file body are copied, and source defaults are never substituted.

This evidence is sufficient only for the provider's deployed activation/config gate when paired with the matching physical fingerprint. Runtime combat behavior remains separate QA.

See [`wiki/modpack-catalog/providers/⚠️-simply-swords-cataclysm/DEPLOYED-CONFIG-CHECKLIST.md`](../../wiki/modpack-catalog/providers/⚠️-simply-swords-cataclysm/DEPLOYED-CONFIG-CHECKLIST.md).

### Simply More

The collector hashes the exact current filename:

`simplymore-forge-1.3.0_alpha.jar`

and emits `current_physical_alpha5_equality` against canonical physical/publisher SHA-1
`51636477cd5c378f42d9700e1fe35cd952c8f4f1`.

For the bounded Mimicry subgate it reads only the Fzzy Config file derived from the exact
Alpha-5 config id `simplymore:unique_effect`:

`config/simplymore/unique_effect.toml`

and only the 25 exact paths:

`mimicry.config.<form>.disabled`

for the forms declared by Alpha-5 `MimicryConfig`. The report retains only form id,
bounded status and boolean `disabled` value. Missing files, parse failures, missing
forms and non-boolean values remain fail-closed. Unrelated values from the config are
not copied.

This closes only the deployed Mimicry form-disable evidence surface. It does **not**
by itself close Simply More's full reachability blocker: host Simply Swords
Awakening/unlock state, acquisition/reformation routes, and any other deployed
suppression still require provider-specific evidence.

See [`wiki/modpack-catalog/providers/⚠️-simply-more/README.md`](../../wiki/modpack-catalog/providers/⚠️-simply-more/README.md).

### Simply Swords

The collector hashes the exact current filename:

`simplyswords-neoforge-1.70.2-1.21.1.jar`

and emits `current_physical_1_70_2_equality` against canonical physical/publisher
SHA-1 `05b074ff774467f1fe9fb5592151b7845c321cbc`.

The release-line source checkpoint
`Sweenus/SimplySwords@359a8031b1a3243d1a3b013dbaa0cbba70ea8278`
declares Fzzy Config `0.7.6+1.21`. At that checkpoint,
`GeneralConfig` uses id `simplyswords:general` and `LootConfig` uses id
`simplyswords:loot`. Fzzy Config 0.7.6 uses the identifier namespace as the
default config folder, identifier path as the default filename, and TOML as the
default file type. The bounded paths are therefore:

- `config/simplyswords/general.toml`;
- `config/simplyswords/loot.toml`.

From `general.toml` the report retains only:

- `enableUniqueWeaponAwakening`.

From `loot.toml` it retains only:

- `enableLootDrops`;
- `runicLootTableWeight`;
- `uniqueLootTableWeight`;
- `enableContainedRemnants`;
- `disabledUniqueWeaponLoot`;
- `uniqueLootTableOptions`.

Resource IDs in the set/map surfaces are validated before retention. Missing
files/keys, duplicate key matches, malformed TOML, non-boolean/non-numeric
values and invalid resource locations remain explicit fail-closed states.
Unrelated config values are never copied into the report.

Important semantic caveat: `enableUniqueWeaponAwakening=false` is **not** a
provider-wide ability disable switch. The 1.70.x provider semantics make
ordinary Unique weapons operate at maximum Awakening when that system is
disabled; Lichblade/Dormant Relic progression is separately preserved.
Therefore the value must be interpreted through the provider checklist rather
than translated directly into a strict-count delta.

This route closes only bounded deployed config/fingerprint evidence. Per-stack
Awakening/unlock state, complete acquisition/reformation, compat-dependent
materialization and addon ownership remain separate closure gates.

See
[`wiki/modpack-catalog/providers/⚠️-simply-swords/DEPLOYED-REACHABILITY-CHECKLIST.md`](../../wiki/modpack-catalog/providers/⚠️-simply-swords/DEPLOYED-REACHABILITY-CHECKLIST.md).

### Somake Spells

Searches for the provider-level progression key:

`enableSpellLockSystem`

within the same bounded config roots.

It also collects **bounded Iron's spell-config override evidence for the `somakespells` namespace**. Only these fields are retained when present:

- `irons_spellbooks:enabled`;
- `irons_spellbooks:school`;
- `irons_spellbooks:allow_crafting`.

Observed locations are limited to:

- `config/irons_spellbooks_spell_config/somakespells/*.json`;
- `config/irons_spellbooks_spell_config/global_config.json`;
- `kubejs/data/somakespells/irons_spellbooks_spell_config/**/*.json`;
- direct world datapack JSONs under `data/somakespells/irons_spellbooks_spell_config/`;
- ZIP datapacks under the same namespace/path.

The report retains only relative paths and those selected fields. It does not copy full JSON payloads.

The physical Somake JAR is hashed independently. Matching the publisher release hash closes byte equality only. An observed spell-config file or override is **evidence about a named config surface, not proof that the corresponding spell is enabled in every layer or survival-reachable**. The exact 1.0.9 registry and current 83/83 registration composition are already closed canonically by separate provider evidence; this collector does not replace or re-prove that registry.

### Traveloptics

Hashes the known original/patched filenames and classifies an observed hash as:

- `ORIGINAL_EXACT`;
- `PATCHED_EXACT`;
- `OTHER_VERIFIED`.

It also searches only for the exact literal `traveloptics:blackout` in bounded deployed customization surfaces:

- `kubejs/server_scripts/`;
- `kubejs/data/`;
- `config/ftbquests/`;
- `defaultconfigs/ftbquests/`;
- discovered/explicit world `datapacks/`, including text-like entries inside ZIP datapacks.

The JSON retains only source category, relative path, line number and the exact literal. It does **not** copy script bodies, quest prose or datapack payloads.

This closes physical disposition only when the collected file is the actual installed JAR. A Blackout literal match is only a **route candidate**; it must still be inspected against the Traveloptics checklist to prove an actual current-pack survival grant/acquisition mechanism.

## Iron's 3.16.3 host contract for collected paths

The bounded paths above are grounded in the exact Iron's source checkpoint already used by the Somake host audit:

`iron431/Irons-Spells-n-Spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`

At that checkpoint, `SpellConfigManager` defines:

- subconfig folder `irons_spellbooks_spell_config`;
- global file `global_config.json`;
- local per-spell layout `/config/irons_spellbooks_spell_config/<mod_id>/<spell_id>.json`;
- datapack layout `/data/<mod_id>/irons_spellbooks_spell_config/<spell_id>.json`;
- `enabled`, `school` and `allow_crafting` among the registered spell-config parameter types.

The host builds effective config by iterating the actual Iron's spell registry, applying a per-spell JSON only when an entry exists for that registered spell, then applying global values as fallback where the parameter is still at its default. Unknown spell-config files are ignored by the host.

Consequently, the collector reports observed config/override evidence but **does not use the presence or filename of a JSON file as proof that a Somake spell is currently registered**. Registry closure remains separate from filesystem evidence: the deployed current-pack registration outcome may be closed by deterministic exact assembled-server registry observation, while generalized optional-registration predicates still require permitted provider-authoritative evidence.

## Collector fixture validation — Somake Iron's overrides

The bounded Somake override extraction was validated on a synthetic instance before durable merge:

- temporary NON-MERGE PR: **#339**;
- exact fixture HEAD: `a1433f0663b2ec3bc965e285dfa0b05232c9cf09`;
- workflow: **Provider Collector Somake Override Fixture NON-MERGE**;
- run: `35451515912` — SUCCESS.

The fixture exercises local Iron's spell config, global config, KubeJS override, direct world datapack, ZIP datapack and `enableSpellLockSystem`. It also injects unselected sentinel fields and asserts that those values are absent from the emitted JSON.

This validates **collector behavior only**. It is not evidence of any value in the user's actual modpack.

## Privacy / minimization

The collector deliberately avoids:

- usernames;
- absolute instance paths in the JSON;
- full config dumps;
- script bodies;
- quest prose;
- datapack payload bodies;
- player data;
- raw log lines, timestamps, thread names, chat/player message bodies and unrelated log content;
- saves;
- authentication/secrets;
- unrelated mod configuration.

Only relative paths, selected values, file hashes, bounded exact-literal locations and whitelisted structured catalog-probe fields are emitted.

Review the JSON before attaching it anywhere.

## Evidence discipline

A collector result is **evidence input**, not an automatic catalog promotion.

For every provider:

1. verify the report came from the actual current pack/world;
2. match physical hashes to the current modlist/provider line;
3. apply the provider's canonical acceptance rule;
4. update only the rows actually proven;
5. preserve fail-closed state for missing/ambiguous values;
6. keep runtime/integration QA separate from catalog closure.

Do not convert missing files into source-default values unless the actual runtime/config contract proves that fallback for the deployed environment.

## Current blockers this can reduce

- Asterism: deployed Astral Gateway Iron's spell config/datapack;
- Gaze: effective `disableGazeRites`;
- NEG: effective enabled state for 39 candidates, via deployed TOML evidence or schema-3 exact-server `type=glyph` runtime observations;
- Corail Tombstone: physical 9.5.6 equality plus the 12 bounded `AllowedMagicItems` booleans that gate the remaining tablets/gemstones/Grave Key/Lost Tablet/Magic Scroll/Scroll of Knowledge candidates; semantic deduplication and reachability still require provider-specific review;
- Somake: physical equality and 83/83 registration composition are already closed canonically; the collector can corroborate the installed hash and reduce the remaining deployed `enableSpellLockSystem` plus Iron's per-spell/global/datapack `enabled` / `school` / `allow_crafting` gates;
- Mowzie's Mobs: current physical 1.8.2 equality plus effective deployed `enable_tunneling`;
- Ice And Fire CE: current physical 2.1.2 equality plus deployed `config/iceandfire/iaf-common.json -> tools.phantasmalBladeAbility` for the sole remaining Ghost Sword gate; Dread Lich Staff acquisition is already closed by provider-specific runtime audit `36327488231`;
- Simply Swords: Cataclysm: current physical 1.0.2 equality plus the ten exact STARTUP values needed to classify all four source-pinned abilities;
- Simply Swords: current physical 1.70.2 equality plus bounded Awakening and loot/remnant config evidence; per-stack Awakening/unlock, complete acquisition/reformation, compat materialization and addon ownership remain provider-specific;
- Traveloptics: current physical override/provider blocker — classify the actual installed JAR and discover bounded deployed `traveloptics:blackout` references; exact-current registry/loot/acquisition review remains provider-specific.
- Iron's Spellbooks KubeJS / KubeJS Ars Nouveau: use `kubejs_script_inventory` to bind the review to the exact current script/data tree; for KubeJS Ars Nouveau also require the exact 1.3.2 physical fingerprint, then inspect non-empty files for recipe/acquisition mutations according to its provider checklist.

Somake's exact 1.0.9 registry and current 83/83 registration composition are already closed by canonical provider evidence; the collector is used for deployed config/host/reachability evidence, not to redo that registry. Pair it with [`provider-catalog-runtime-registry-probe.md`](provider-catalog-runtime-registry-probe.md) when exact assembled-server Iron's registry identity and effective host `school` / `enabled` / `allow_crafting` observations are required. For the current physical pack, those runtime rows may close the deployed registration outcome when paired with physical identity/mod-presence evidence; they do not establish a universal predicate contract. The runtime probe is separate QA evidence and still does not prove survival acquisition, provider-owned progression gates, Traveloptics Blackout reachability or Somake↔Traveloptics Aqua authority.