# kubejsarsnouveau 1.3.2 — pack-script closure checklist

Status: `CURRENT PHYSICAL 1.3.2 IDENTIFIED / RELEASE-LINE RECIPE SURFACE AUDITED / CURRENT SCRIPT INVENTORY REQUIRED`

## Purpose

Close whether the exact current pack uses kubejsarsnouveau to change Ars Nouveau recipes, glyph acquisition or caster-tome presets.

This checklist is **not** a search for a provider-owned glyph implementation roster. The audited bridge does not expose such a builder.

## Already closed — do not redo

- current filename `kubejsarsnouveau-1.3.2.jar`;
- mod id `kubejsarsnouveau`;
- runtime `1.3.2`;
- physical SHA-1 `f39f4f409e628731be551fd961fac2964768d358`;
- CurseForge project/file identity 833926 / 7181937;
- release-line source checkpoint `BobVarioa/kjsarsnouveau@18278a05d27def7200158a6d08516d5f22318e44`;
- source checkpoint is **not** claimed byte-equivalent because it declares source metadata 1.3.1;
- base bridge exposes 3 recipe components and 6 Ars recipe schemas;
- no active bindings, registry builders or KubeJS event surface established;
- base semantic delta **+0**.

## Collector-assisted evidence

Run:

```bash
python docs/qa/provider-catalog-deployed-evidence-collector.py "/path/to/current/modpack-instance"
```

Require:

1. `mods.kubejsarsnouveau` contains the current JAR;
2. `current_physical_1_3_2_equality=true`;
3. review `kubejs_script_inventory` from the same assembled instance.

Do not substitute repository search for the physical script inventory.

## Script surfaces to inspect

Review exact hashed files from `kubejs/startup_scripts/**`, `kubejs/server_scripts/**`, `kubejs/client_scripts/**` only when needed to classify presentation-only behavior, `kubejs/data/**`, and generated/indirectly loaded scripts if the pack uses them.

For this provider, prioritize server recipe mutations and datapack recipe definitions.

## Recipe audit targets

Trace uses of:

- `ars_nouveau:enchanting_apparatus`;
- `ars_nouveau:enchantment`;
- `ars_nouveau:crush`;
- `ars_nouveau:imbuement`;
- `ars_nouveau:glyph`;
- `ars_nouveau:caster_tome`.

For every relevant script-created recipe, record script/data file and line/range, recipe ID/type, output/content referenced, registration condition, whether it replaces/removes a provider-native recipe, Source/XP costs where applicable, and whether it changes normal survival acquisition/reachability of a cataloged semantic object.

## Glyph rule

A recipe of type `ars_nouveau:glyph` is not, by itself, a new glyph implementation.

Count a new glyph semantic object only when its actual implementation/registry authority is independently established in the provider that owns it.

kubejsarsnouveau may change how an existing glyph is acquired, but the recipe bridge is not assigned ownership of that glyph.

## Caster tome rule

A `caster_tome` recipe may encode a sequence of existing glyph IDs. Treat it as preset/acquisition content, not a new atomic glyph or new provider spell implementation unless another provider defines a distinct semantic object that meets the catalog rules.

## Zero-customization closure

If authoritative current-instance evidence shows exact physical 1.3.2 match and the bounded current script/data tree contains no relevant Ars recipe mutations through this bridge, this provider can be closed as a zero-semantic recipe framework.

If relevant scripts exist, inventory their acquisition/progression effects before promotion.

## Current result

- base semantic contribution: **+0**;
- current recipe/acquisition mutation set: **UNKNOWN**;
- provider state: **⚠️ partial / conditioned**.
