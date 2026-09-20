# Provider catalog — runtime registry probe

Status: `SUPPORTING QA COMPANION / READ-ONLY OBSERVATION / NOT PRODUCTION CONTENT / DOES NOT CREATE CATALOG PASS BY ITSELF`

## Purpose

The filesystem collector in `provider-catalog-deployed-evidence-collector.py` closes physical hashes and bounded deployed configuration surfaces, but it deliberately does not infer a provider registry from localization or config filenames.

`black_arcana_catalog_qa` is a separate removable NeoForge companion used on the **actual assembled server** to observe the current Iron's spell registry through the supported Iron's API.

It is intended to reduce current conditional-provider blockers for:

- Somake Spells 1.0.9;
- Asterism Arcanum 0.1.0;
- Gaze 1.1.7.1 Iron's-hosted spell surfaces;
- T.O Magic n' Extras / Traveloptics 4.4.0.1.

For Traveloptics it also observes the two exact NeoForge global-loot-modifier serializer IDs already named by the canonical closure checklist: `traveloptics:key_loot` and `traveloptics:universal_loot`.

It does not enumerate Ars Nouveau registries and therefore does not replace the deployed Not Enough Glyphs SERVER-config checklist.

## Isolation

The probe lives in the dedicated Gradle source set:

`src/catalogQaProbe/`

and is packaged only by:

`catalogQaProbeJar`

Output JAR:

`build/libs/black_arcana_catalog_qa-<version>.jar`

The canonical Black Arcana production JAR must not contain:

- mod id `black_arcana_catalog_qa`;
- `CatalogQaProbeMod`;
- `CatalogRuntimeEvidence`.

CI explicitly verifies that isolation.

The companion requires:

- Black Arcana;
- Iron's Spells 'n Spellbooks;
- NeoForge;
- Minecraft 1.21.1.

It is server-side QA infrastructure, not gameplay content.

## Exact host API authority

The probe compiles against the project-pinned Iron's API:

`io.redspace:irons_spellbooks:1.21.1-3.16.3:api`

The exact source checkpoint already used by Black Arcana's Iron's host audit is:

`iron431/Irons-Spells-n-Spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`

At that checkpoint:

- `SpellRegistry.REGISTRY` is the public `Registry<AbstractSpell>`;
- `AbstractSpell.isEnabled()` returns the effective Iron's spell-config `enabled` value;
- `AbstractSpell.allowCrafting()` returns the effective Iron's spell-config `allow_crafting` value;
- `AbstractSpell.getSchoolType()` resolves the effective Iron's spell-config school;
- `SchoolType.getId()` exposes the resolved school identifier.

The probe uses only those public host surfaces plus NeoForge `ModList.isLoaded`.

The project is pinned to NeoForge `21.1.248`. NeoForge's 1.21-1.21.1 Global Loot Modifier contract registers each modifier `MapCodec` in `NeoForgeRegistries.Keys.GLOBAL_LOOT_MODIFIER_SERIALIZERS`; the corresponding public runtime registry is `NeoForgeRegistries.GLOBAL_LOOT_MODIFIER_SERIALIZERS`. The probe queries that registry only for the exact two Traveloptics IDs above. It does not resolve or print provider codec class names.

No provider implementation class, decompilation, method body, numerical spell formula, private state, packet internals, assets or localization prose is inspected.

## Bounded runtime output

The probe runs once on `ServerStartedEvent` and writes only log lines prefixed:

`[BLACK_ARCANA_CATALOG_PROBE]`

Target Iron's spell namespaces:

- `asterismarcanum`;
- `gaze`;
- `somakespells`;
- `traveloptics`.

For each observed Iron's spell registry entry it emits only:

- registry ID;
- effective school ID;
- effective `enabled`;
- effective `allow_crafting`.

For Traveloptics loot-modifier registration it emits only:

- whether `traveloptics:key_loot` is present in NeoForge's global-loot-modifier serializer registry;
- whether `traveloptics:universal_loot` is present;
- when both are present, whether the two registry values are distinct object instances.

It does not emit codec class names or loot-modifier implementation details.

It also emits loaded/not-loaded state for a bounded set of provider/compat mod IDs relevant to the five remaining conditional-provider checklists.

Example shapes:

```text
[BLACK_ARCANA_CATALOG_PROBE] type=spell id=somakespells:<id> status=OBSERVED school=<namespace:id> enabled=true allow_crafting=true
[BLACK_ARCANA_CATALOG_PROBE] type=loot_modifier_serializer id=traveloptics:key_loot status=OBSERVED
[BLACK_ARCANA_CATALOG_PROBE] type=loot_modifier_pair namespace=traveloptics status=OBSERVED distinct_codec_instances=true
```

Do not treat those examples as evidence of any real assembled-pack value.

The probe emits namespace counts after the individual rows. A zero count is an observation for that exact launched assembled server only; it is not a general claim about the provider.

## Build

From the Black Arcana repository root:

```bash
./gradlew --no-daemon catalogQaProbeJar
```

On `main`, CI also publishes a temporary workflow artifact named:

`black-arcana-catalog-qa-<commit-sha>`

The artifact exists for QA convenience only and is not part of the production mod distribution.

## Exact-pack execution

1. Confirm the assembled instance is the current authoritative modpack and preserve its modlist/checkpoint.
2. Place the exact Black Arcana build under validation in the instance.
3. Place `black_arcana_catalog_qa-<version>.jar` in the server `mods/` directory.
4. Start the dedicated server normally and wait until startup completes.
5. Extract only lines beginning with `[BLACK_ARCANA_CATALOG_PROBE]`.
6. Stop the server and remove the QA probe JAR before normal gameplay/release packaging.
7. Pair the runtime rows with `provider-catalog-deployed-evidence.json` from the read-only filesystem collector.
8. Apply each provider's canonical acceptance checklist. Do not promote a provider merely because the probe ran successfully.

## Evidence meaning

A registry row from the actual assembled server can close, for that exact run:

- observed active Iron's registry identity;
- observed effective Iron's school;
- observed effective Iron's `enabled`;
- observed effective Iron's `allow_crafting`.

For Traveloptics Gate 2, a successful exact-pack startup that reaches this probe can additionally provide direct evidence that the two expected NeoForge serializer IDs are present. A `distinct_codec_instances=true` row is bounded evidence that those two registry keys do not resolve to the same codec object in that run. Gate 2 still requires the actual deployed JAR hash/disposition to be paired with the startup evidence; the probe alone does not identify the physical bytes.

It does **not** by itself close:

- survival acquisition/reachability, including `traveloptics:blackout`;
- provider-owned progression gates outside Iron's host API;
- Somake `enableSpellLockSystem`;
- exact source-level optional-registration predicate logic;
- Traveloptics loot-modifier data activation or loot behavior beyond serializer registration;
- Somake↔Traveloptics Aqua runtime authority;
- Gaze Rite initialization;
- Not Enough Glyphs `[general].enabled`.

Those remain governed by the existing provider-specific closure checklists and the filesystem collector.

## Failure discipline

If the probe cannot resolve a host value, it emits:

`status=HOST_VALUE_UNAVAILABLE`

with only the exception class name. It does not invent a fallback value.

If an Iron's spell registry key resolves without a value, it emits:

`status=REGISTRY_VALUE_UNAVAILABLE`

For the bounded Traveloptics serializer observation, missing keys emit `status=NOT_PRESENT`; a partial pair emits `status=INCOMPLETE`; registry access failure emits `status=REGISTRY_VALUE_UNAVAILABLE`.

Missing, contradictory or failed observations remain fail-closed.

## Privacy / minimization

The probe does not intentionally emit:

- usernames or UUIDs;
- player data;
- world coordinates;
- chat;
- save contents;
- config file bodies;
- script/quest text;
- authentication data;
- absolute filesystem paths.

Only the bounded provider/mod/registry fields above are emitted.

Review the extracted probe lines before attaching them to a catalog evidence PR.
