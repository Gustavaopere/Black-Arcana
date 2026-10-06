# Cross-Domain Rebase — 2026-10-06 — Zero-Semantic Batch 1

Status: `CURRENT PHYSICAL CROSS-DOMAIN TRIAGE / 5 NEW ✅ ZERO-SEMANTIC PROVIDERS / PROVIDER TREE 162 = 160 ✅ + 2 ⚠️ / STRICT SEMANTIC MINIMUM UNCHANGED 1858`

## Authority

- Black Arcana base: `main@9181b59635564700fe127d46f7966854296d2127`;
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
| Epic Fight & Iron's Spellbook Animation Compat 3.1.0 | `efiscompat` | current physical identity + official 1.21.1 branch `b4b58aff...` declaring 3.1.0 | `ZERO_SEMANTIC_CAST_ANIMATION_BRIDGE` | +0 |

## Why these are cross-domain providers

These five were not part of the 97-row physical-`Magic` category subtotal:

- Dragons Plus is categorized as Create/technology/library/processing but has Ars/Aether-facing integration names;
- True Immersion is an addon/compat layer over a portal engine;
- Better Witch Huts is worldgen/structures;
- Snow! Real Magic! is cosmetic/worldgen/weather despite the word “Magic” in its title;
- EFIS is cataloged physically under cosmetic/miscellaneous even though it consumes Iron's spell IDs for animation.

They must not be inferred as magic providers merely from branding or referenced spell IDs. The explicit dossiers prevent that ambiguity.

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

### EFIS

Official `1.21.1` branch resolves to:

`domanhthang2110/efiscompat@b4b58aff86e707420fac8a7c29fe647d7f5aaac4`

The branch declares `mod_version=3.1.0`.

The source contains many `data/efiscompat/spell_animations/**` mappings, including existing Iron's and Traveloptics spell IDs. Those are animation mappings, not spell registrations.

Bounded search:

- `registerSpell`: 0;
- `DeferredRegister`: 0;
- provider spell-registration surface: 0.

Its `SpellRegistry` / `AbstractSpell` references read existing Iron's spell state for animation/cancel compatibility.

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

- **162** top-level provider directories;
- **160 ✅**;
- **2 ⚠️**;
- **0 ❌**;
- **0 🟡**;
- **0 ⛔**.

The two ⚠️ providers remain:

1. Traveloptics;
2. Deeper and Darker.

## Semantic consequence

No semantic object is added.

- strict reconstructible semantic minimum: **1858**;
- final semantic denominator: still open;
- technical cross-domain denominator: still `PENDING REBASE`;
- no final coverage percentage declared.

This batch is structural/ownership reconciliation, not a semantic-numerator increase.
