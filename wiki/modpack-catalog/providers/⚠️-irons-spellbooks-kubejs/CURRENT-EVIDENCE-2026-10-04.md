# Iron's Spellbooks KubeJS 4.0.3 — current evidence checkpoint (2026-10-04)

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 4.0.3 / BASE FRAMEWORK +0 / CURRENT SCRIPT TREE NOT CAPTURED / FAIL-CLOSED`

## Authority checkpoints

- Black Arcana main considered: `dec859ccf38fe2e51e343cd59a6304057dacbb81`.
- Current sibling/modlist authority: `Gustavaopere/neoforge-rpg-skilltree@fa47288bd99e1166880a8fb0ee00cab06697a88a`.
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

## Decisive closure route

Run the canonical read-only collector against the actual current assembled instance:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/modpack-instance"
```

The `kubejs_script_inventory` result is the first decisive artifact for this provider:

1. absent/empty authoritative current bounded script/data tree -> eligible for zero-content closure review;
2. non-empty tree -> inspect the exact hashed files for Iron's spell/school builder registrations;
3. every surviving custom spell must then be traced through ID, source file/range, registration condition, school, effective Iron's config and survival reachability.

A repository search alone is insufficient.

## Current semantic disposition

- fixed provider-owned built-in spells: **0 established**;
- fixed provider-owned built-in schools: **0 established**;
- script-defined current-pack spell/school objects: **UNKNOWN**;
- strict semantic contribution from the bridge itself: **+0**;
- current pack script-defined contribution: **NOT ADDITIVE until proven**;
- provider status: **⚠️ partial / conditioned**.

No catalog numerator or denominator change is justified by this checkpoint.
