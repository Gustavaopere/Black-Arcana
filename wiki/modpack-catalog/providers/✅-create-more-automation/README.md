# Create: More Automation — 0.5.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_CREATE_RECIPE_AUTOMATION / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#150**;
- JAR: `create_more_automation-0.5.2-neoforge-1.21.1.jar`;
- mod id: `create_more_automation`;
- runtime: `0.5.2`;
- physical SHA-1: `a184d11c11fb03619dd8940cc160b3aa0d5e96fe`.

The sibling dossier classifies this provider as a Create recipe/data addon. Create remains authority for machine/process execution; More Automation contributes additional recipes.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#541** audits Modrinth version `en1TN4J7` and hard-gates the publisher file against the physical fingerprint.

- audit HEAD: `ac7c1e86a62d674865edcee13012c65d72050b7a`;
- exact-artifact run: `37022756954` — **SUCCESS**;
- evidence artifact: `11233373566`;
- evidence digest: `sha256:f64478f633723840bbb52eb9b7a9a555fa0558cfdfb24eb7da08d83d1c6b51f6`;
- publisher file: `create_more_automation-0.5.2-neoforge-1.21.1.jar`;
- publisher SHA-1: `a184d11c11fb03619dd8940cc160b3aa0d5e96fe`;
- publisher SHA-256: `2e85408b5480667af7b2e8be4569f147d070f7be7d0d2985aade6d3adc3d8977`;
- bytes: `315,683`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-0.5.2-ARTIFACT-AUDIT.md`](EXACT-0.5.2-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact artifact contains:

- **73** archive entries;
- **6** classes;
- **67** non-class resources;
- **19** `data/create_more_automation/**` paths;
- **15** provider JSON files inspected;
- **14** valid provider recipe JSONs plus one invalid/blank placeholder JSON.

Exact lexical/path counts are zero for:

`spell · magic · ritual · ability · mana · arcane · glyph · summon · soul · teleport · portal · enchant · curse`.

The exact activation index is empty: none of the six provider classes declares a bounded player-action override among `use`, `useOn`, `useWithoutItem`, `releaseUsing`, `onUseTick`, `finishUsingItem`, `interactLivingEntity`, `hurtEnemy`, `inventoryTick`, `onArmorTick`, `onItemUseFirst` or `mineBlock`.

## Exact recipe surface

The 14 valid provider recipes use ordinary Create/vanilla processing types:

- 7 × `create:mixing`;
- 3 × `create:crushing`;
- 1 × `create:compacting`;
- 1 × `create:haunting`;
- 1 × `create:filling`;
- 1 × `minecraft:blasting`.

Named recipe coverage includes Asurine, Calcite, Crimsite, Experience Nugget, Flux Catalyst, Ice, Moss, Netherrack, Ochrum, scrap conversion, Redstone, Snowball and Veridium automation. These are processing/economy routes, not spells or magical actions.

Detailed disposition: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Authority boundary

Create: More Automation remains authority for which extra recipes it contributes. Create remains authority for processing execution and settlement. Black Arcana must not duplicate those recipes, execute a second machine settlement or reinterpret processing recipes as spell identities.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_CREATE_RECIPE_AUTOMATION`.**

Strict semantic delta: **+0**.
