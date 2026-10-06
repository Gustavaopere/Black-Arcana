# Cross-Domain Rebase — 2026-10-06 — Zero-Semantic Batch 1

Status: `CURRENT PHYSICAL CROSS-DOMAIN TRIAGE / 4 NEW ✅ ZERO-SEMANTIC PROVIDERS / PROVIDER TREE 161 = 159 ✅ + 2 ⚠️ / STRICT SEMANTIC MINIMUM UNCHANGED 1849`

Numerator note: **1849 is current**. The older 1858 checkpoint included Ars Morph (+8) and Woodwalkers SpellBooks (+1), both absent from the current physical snapshot.

## Authority

- Black Arcana base after reconciliation with current main: `main@3e87370c2d5363c06d92d107fcb11826e3820bba`;
- sibling physical/modlist authority: `neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`;
- physical-`Magic` category checkpoint remains [PHYSICAL-MAGIC-RECONCILIATION-2026-10-05.md](./PHYSICAL-MAGIC-RECONCILIATION-2026-10-05.md).

This batch does not add or remove any of the 97 physical dossiers whose category directory contains `Magic`. It extends the cross-domain structural catalog to providers outside that category whose names/features can look magical and therefore require an explicit semantic disposition.

## New provider closures

| Provider | Physical mod id | Evidence ceiling | Disposition | Strict delta |
|---|---|---|---|---:|
| Create: Dragons Plus 1.11.8b | `create_dragons_plus` | current physical identity + exact version-declared official source commit `e856977...` | `ZERO_SEMANTIC_CREATE_PROCESSING_COMPAT_INFRA` | +0 |
| Immersive Portals: True Immersion 2.0.4 | `immersive_portals_full_immersion` | current physical identity + official 2.0.4 release description | `ZERO_SEMANTIC_PORTAL_INTERACTION_BRIDGE` | +0 |
| YUNG's Better Witch Huts 4.1.1 | `betterwitchhuts` | current physical identity + official 1.21.1 branch `4cc9a8a...` declaring 4.1.1 | `ZERO_SEMANTIC_STRUCTURE_WORLDGEN_LOOT` | +0 |
| Snow! Real Magic! 12.2.2 | `snowrealmagic` | current physical identity + official project/source corroboration; exact 12.2.2 source equality not claimed | `ZERO_SEMANTIC_SNOW_WORLDSTATE` | +0 |

## Why these are cross-domain providers

These four new provider directories were not part of the 97-row physical-`Magic` category subtotal:

- Dragons Plus is categorized as Create/technology/library/processing but has Ars/Aether-facing integration names;
- True Immersion is an addon/compat layer over a portal engine;
- Better Witch Huts is worldgen/structures;
- Snow! Real Magic! is cosmetic/worldgen/weather despite the word “Magic” in its title;

They must not be inferred as magic providers merely from branding or referenced spell IDs. The explicit dossiers prevent that ambiguity.

### Existing EFIS provider — reused, not added

`efiscompat` 3.1.0 was reviewed during construction of this batch but is **not a new provider**. It is already canonically cataloged at [`../providers/✅-efiscompat/README.md`](../providers/✅-efiscompat/README.md), with the same mod id, physical JAR/SHA-1, exact source pin and zero-standalone-spell disposition. This batch therefore reuses that canonical directory and adds **no second EFIS provider**.

## Source/semantic audit summary

### Create: Dragons Plus

Exact 1.11.8b source pin:

`DragonsPlusMinecraft/CreateDragonsPlus@e856977bfef46f5a7fa287ea383fdffea13c7891`

The source declares `mod_version = 1.11.8b`. Bounded source search returns:

- `registerSpell`: 0;
- `SpellRegistry`: 0;
- `AbstractSpell`: 0;
- ritual surface: 0.

Its deferred registries are recipes/serializers, conditions, criteria, item attributes, creative tabs and fan-processing types. Optional Aether “enchanting” and Ars Dragon's Breath support are processing/compatibility surfaces.

### YUNG's Better Witch Huts

Official `1.21.1` branch resolves to:

`YUNG-GANG/YUNGs-Better-Witch-Huts@4cc9a8a6eed2306ce5db9b8dbcd8dbc6ed23bc54`

The branch declares `version=4.1.1`, `mod_id=betterwitchhuts`, `mc_version=1.21.1`.

Complete source tree:

- 175 paths;
- 32 Java files;
- no spell/ritual/ability semantic path;
- no `registerSpell`, `SpellRegistry`, `AbstractSpell`, ritual or ability registration surface found in bounded search.

Its provider-owned content is structure/worldgen/loot.


### Snow! Real Magic!

The current physical pack uses 12.2.2. Official 1.21 NeoForge source has advanced to 12.2.3, so no exact 12.2.2 source equality is claimed.

The physical dossier and official project surface describe snow-covered block state, accumulation/melting, falling snow, water→ice, collision/spawning, worldgen, gamerules and seasonal integration. Bounded official-source search finds no `registerSpell`, `SpellRegistry`, `AbstractSpell` or ritual registration surface.

### True Immersion

Exact public 2.0.4 source was not located. The official release/project scope is bounded to additional interactions through already-existing portals.

The portal engine and originating portal/spell providers retain portal identity/creation authority. True Immersion adds interaction routing and therefore contributes zero independent magic identities.

## Structural consequence

Before this batch:

- 157 top-level provider directories;
- 155 ✅;
- 2 ⚠️.

After this batch:

- **161** top-level provider directories;
- **159 ✅**;
- **2 ⚠️**;
- **0 ❌**;
- **0 🟡**;
- **0 ⛔**.

The two ⚠️ providers remain:

1. Traveloptics;
2. Deeper and Darker.

## Semantic consequence

No semantic object is added.

- strict reconstructible semantic minimum: **1849**;
- final semantic denominator: still open;
- technical cross-domain denominator: still `PENDING REBASE`;
- no final coverage percentage declared.

This batch is structural/ownership reconciliation, not a semantic-numerator increase.
