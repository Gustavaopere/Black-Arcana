# Provider catalog — deployed evidence collector

Status: `SUPPORTING QA TOOL / READ-ONLY / DOES NOT CREATE CATALOG PASS BY ITSELF`

## Purpose

The remaining conditional-provider blockers are increasingly tied to the **actual assembled pack** rather than missing source enumeration.

`provider-catalog-deployed-evidence-collector.py` provides one bounded, read-only collection step for:

- Asterism Arcanum 0.1.0;
- Gaze 1.1.7.1;
- Not Enough Glyphs 4.6.2;
- Somake Spells 1.0.9;
- T.O Magic n' Extras / Traveloptics 4.4.0.1;
- bounded deployed customization references relevant to those same closure gates.

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

Custom output:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance" \
  --output "/safe/path/provider-catalog-deployed-evidence.json"
```

## What the collector records

### Physical JAR fingerprints

For the known current filenames it records:

- filename;
- SHA-1;
- SHA-256;
- byte size.

Special comparisons:

- Somake 1.0.9 is compared against exact release SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`;
- Traveloptics is classified against:
  - original SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8`;
  - exact patch candidate SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`;
- Gaze 1.1.7.1 is compared against exact known artifact SHA-1 `a8cb3190bde157f78160ce65c202ce2d47fb2041`;
- Not Enough Glyphs 4.6.2 is compared against exact publisher-release SHA-1 `32eea2c478a346ee7499f6a0db156241116f73e9`.

A missing file is not converted into a replacement identity.

### Asterism Arcanum

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

### Somake Spells

Searches only for:

`enableSpellLockSystem`

within the same bounded config roots.

The physical Somake JAR is hashed independently. Matching the publisher release hash closes byte equality only; it does not close current 1.0.9 registry/reachability by itself.

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

## Privacy / minimization

The collector deliberately avoids:

- usernames;
- absolute instance paths in the JSON;
- full config dumps;
- script bodies;
- quest prose;
- datapack payload bodies;
- player data;
- logs;
- saves;
- authentication/secrets;
- unrelated mod configuration.

Only relative paths, selected values, file hashes and bounded exact-literal locations are emitted.

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
- NEG: effective `[general].enabled` for 39 candidates;
- Somake: physical 1.0.9 equality plus deployed `enableSpellLockSystem`;
- Traveloptics: original-vs-patched physical disposition plus bounded discovery of deployed `traveloptics:blackout` references that may point to a pack-specific acquisition route.

The collector does not solve Somake's exact 1.0.9 registry by itself. It also does not prove Traveloptics startup, Blackout reachability or Aqua behavior merely because a literal reference is found.
