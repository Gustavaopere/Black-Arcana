# Iron's Spellbooks KubeJS 4.0.3 — current evidence checkpoint (2026-10-04)

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 4.0.3 / BASE FRAMEWORK +0 / CURRENT SCRIPT TREE NOT CAPTURED / FAIL-CLOSED`

## Authority checkpoints

- Historical Black Arcana main at the original evidence-branch creation: `e614dea1be34936b095af2a3d7c8d65c69f7e34d`.
- Historical Black Arcana main reconciled during the earlier evidence checkpoint: `21ae73850eb75b35ff09b6f0eada640cc2a1bf23`.
- Black Arcana main confirmed after the exact source-coverage closure: `04633ea786869045f8959e942dd348aff6258033`.
- Black Arcana main reconciled for the current host-377 closure hardening in PR #624: `3b386df50d3db3a8e5606529f97c7413dbf6ab32`.
- Current sibling/modlist authority: `Gustavaopere/neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`.
- Current registry row: Black Arcana `wiki/modpack-catalog/PROVIDERS.md` row 98.
- Certified sibling dossier:
  `PROJECT-INSTRUCTIONS/modlist/Addons + Adventure and RPG + KubeJS + Magic + Utility & QoL/✅-irons-spellbooks-kubejs v4.0.3.md`.

The current physical identity remains:

- JAR: `irons_spells_js-4.0.3.jar`;
- mod id: `irons_spells_js`;
- runtime: `4.0.3`;
- SHA-1: `0481395c5847e2920d1425e77833bef87df63139`;
- Iron's Spells host: `1.21.1-3.16.3`;
- KubeJS host: `2101.7.2-build.377`.

## Exact provider contract already closed

Exact official source pin remains:

`sentwayfarer/irons_spells_js@f3c05a102707a87ac3b8f0d2df5d2ffa5ae5b6c7`

At that pin:

- `IronsSpellsJSPlugin.registerBuilderTypes` installs default builders for Iron's spell and school registry keys;
- `CustomSpell.Builder` creates script-defined `AbstractSpell` instances with script-owned IDs and configurable school/cost/cast callbacks/gates;
- `IronsSpellsJSMod.runIronSpellsConfig` iterates KubeJS `RegistryObjectStorage` for the Iron's spell registry to create corresponding Iron's server-config entries;
- required exact mixins extend the bridge into host runtime: non-player pre-cast, targeted post-cast, living-entity `MagicData`, generic `PathfinderMob` Iron's casting machinery and postponed/rebuilt Iron's server config;
- all **5 declared `ISSEvents` handlers** have a verified subscription/posting path when the required exact mixins are included;
- `SpellAttributeBuilderJS` creates syncable Iron's `MagicRangedAttribute` objects only from script-supplied ranged attribute definitions;
- conditional EntityJS exposes script-built Iron's-compatible spellcasting mobs and spell projectiles, including anti-magic/particle/impact hooks;
- client bootstrap attaches Iron's spellbook Curios rendering and staff arm pose to compatible script-built items;
- the provider itself does not define a fixed gameplay spell roster.

Therefore the base bridge remains a **scriptable framework**, with strict base semantic delta **+0**.

## Current sibling repository search

Fresh default-branch searches on the current sibling were performed for:

- `startup_scripts`;
- `server_scripts`;
- `SpellRegistry.SPELL_REGISTRY_KEY`;
- `irons_spells_js`.

No matching committed current script/registering source was returned.

This is not proof that the assembled instance has no KubeJS scripts. The sibling repository is not treated as an exhaustive mirror of the physical instance's `kubejs/` directory.

## Project / Library evidence available on 2026-10-04

Available retrieval surfaces expose:

- later physical modlist metadata containing KubeJS `2101.7.2-build.377`;
- historical 2026-09-08 boot/log evidence with KubeJS `2101.7.2-build.374` and the previously documented one-script `startup_scripts:main.js` example observation.

No authoritative current `kubejs/startup_scripts/**`, `kubejs/server_scripts/**`, `kubejs/client_scripts/**` or `kubejs/data/**` tree was available in the current Project/Library retrieval.

The build-374 boot cannot be propagated to the later build-377 physical checkpoint.

### Additional closure search refresh — 2026-10-04

Further read-only checks performed after provider-source closure found no authoritative build-377 script tree:

- a recursive Library browse found no recent modpack/instance export carrying a current `kubejs/` directory;
- Library semantic search after 2026-09-15 for `startup_scripts`, `server_scripts`, `client_scripts`, `kubejs/data`, `irons_spells_js` and `2101.7.2-build.377` returned the physical modlist but no current script-tree artifact;
- three later pasted text artifacts dated 2026-09-15 through 2026-09-17 contained no exact `kubejs` matches;
- same-day Library image search produced no indexed screenshot evidencing a current KubeJS script tree;
- Desktop Commander reported no connected authorized device, so the physical instance filesystem could not be inspected through that route;
- broad GitHub code search located provider documentation, public examples and unrelated third-party packs only; no source attributable to this pack's current script tree was established.

These negative searches reduce duplicate work but are **not zero-content proof**. Only the authoritative assembled instance or equivalent exact provenance can close the script-content question.

## Current collector physical fingerprints

The canonical deployed-evidence collector now binds closure to both exact current binaries from the same assembled instance:

- `irons_spells_js-4.0.3.jar` -> `mods.irons_spells_js[*].current_physical_4_0_3_equality` against SHA-1 `0481395c5847e2920d1425e77833bef87df63139`;
- `kubejs-neoforge-2101.7.2-build.377.jar` -> `mods.kubejs[*].current_physical_build_377_equality` against SHA-1 `150c5d6efc09b969ac350ea205128dff832e0850`.

This closes binary identity/freshness only when the collector is run on the authoritative assembled instance. It does not prove source-build byte equality and it does not close script-defined content. Historical build-374 evidence cannot satisfy the build-377 gate.

## Exact provider-source closure

The exact 4.0.3 source checkpoint now has an explicit **30 / 30 Java-file coverage ledger** in `EXACT-4.0.3-FRAMEWORK-SURFACE.md`, plus review of the structural resources that declare metadata/dependencies, required mixins, KubeJS plugin loading and the official `run/kubejs` development fixtures.

Therefore the remaining `⚠️ PARTIAL / CONDITIONAL` state is not caused by unknown provider-source behavior. The unresolved variable is current assembled-pack content: the authoritative build-377 KubeJS script/provenance tree has still not been captured.

Whole-tree follow-up: the exact source repository contains **49 file paths total**, all classified; `src/generated/resources/**` is absent, and no packaged provider `data/**` or semantic `assets/**` roster exists. This reinforces that the unresolved content is pack-owned KubeJS state, not hidden fixed provider data.

## Decisive closure route

Run the canonical read-only collector against the actual current assembled instance:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance"
```

The collector now emits `irons_spellbooks_kubejs_closure.status` as the first routing decision:

1. `ARTIFACT_NOT_OBSERVED` -> certified 4.0.3 provider JAR not captured; stop;
2. `ARTIFACT_HASH_MISMATCH` -> provider JAR differs from the certified current artifact; stop;
3. `KUBEJS_HOST_NOT_OBSERVED` -> current KubeJS build 377 JAR not captured from the same instance; stop;
4. `KUBEJS_HOST_HASH_MISMATCH` -> build-377 filename exists but does not match the current physical SHA-1; stop;
5. `ZERO_CONTENT_REVIEW_CANDIDATE` -> both binaries certified + zero bounded KubeJS files; review authoritative-instance provenance before zero-content closure;
6. `SCRIPT_REVIEW_REQUIRED` -> both binaries certified + one or more bounded KubeJS files; inspect the exact hashed files even if no marker fired;
7. every surviving custom spell must then be traced through ID, source file/range, registration condition, school, effective Iron's config and survival reachability.

The machine-readable state never promotes row #98 automatically.

A repository search alone is insufficient.

## Current semantic disposition

- fixed provider-owned built-in spells: **0 established**;
- fixed provider-owned built-in schools: **0 established**;
- script-defined current-pack spell/school objects: **UNKNOWN**;
- strict semantic contribution from the bridge itself: **+0**;
- current pack script-defined contribution: **NOT ADDITIVE until proven**;
- provider status: **⚠️ partial / conditioned**.

No catalog numerator or denominator change is justified by this checkpoint.
