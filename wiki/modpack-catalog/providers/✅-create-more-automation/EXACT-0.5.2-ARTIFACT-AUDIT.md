# Create: More Automation 0.5.2 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO MAGIC-ACTION DENOMINATOR CLOSED`

## Identity gate

- physical JAR: `create_more_automation-0.5.2-neoforge-1.21.1.jar`;
- mod id: `create_more_automation`;
- runtime: `0.5.2`;
- physical SHA-1: `a184d11c11fb03619dd8940cc160b3aa0d5e96fe`.

NON-MERGE PR #541 downloads Modrinth version `en1TN4J7` and fails if publisher SHA-1 differs from the physical fingerprint.

Evidence:

- audit HEAD: `ac7c1e86a62d674865edcee13012c65d72050b7a`;
- run: `37022756954` — SUCCESS;
- artifact: `11233373566`;
- digest: `sha256:f64478f633723840bbb52eb9b7a9a555fa0558cfdfb24eb7da08d83d1c6b51f6`;
- publisher SHA-1: `a184d11c11fb03619dd8940cc160b3aa0d5e96fe`;
- publisher SHA-256: `2e85408b5480667af7b2e8be4569f147d070f7be7d0d2985aade6d3adc3d8977`;
- bytes: `315,683`.

Result: exact publisher/physical equality is proven.

## Archive inventory

- entries: **73**;
- classes: **6**;
- resources: **67**;
- provider-data paths: **19**;
- provider JSON files: **15**.

The six classes are the mod/network shell, item/tab registries, `FluxCatalystItem` and `MetalScrapItem`. No spell/ritual/ability class family is present.

## Magic-semantic path audit

Exact path counts:

- spell: 0;
- magic: 0;
- ritual: 0;
- ability: 0;
- mana: 0;
- arcane: 0;
- glyph: 0;
- summon: 0;
- soul: 0;
- teleport: 0;
- portal: 0;
- enchant: 0;
- curse: 0.

## Player-action signature audit

The exhaustive bounded activation index across all six classes is empty for the audited player-action method family. There is therefore no provider-owned discrete player action surface hidden behind item subclasses in this artifact.

## Recipe/data classification

Fifteen provider JSON files were bounded. Fourteen parse as recipes; `blank_recipe.json` is an invalid/blank placeholder and does not create runtime content.

Valid recipe types:

- `create:mixing`: 7;
- `create:crushing`: 3;
- `create:compacting`: 1;
- `create:haunting`: 1;
- `create:filling`: 1;
- `minecraft:blasting`: 1.

These are Create/vanilla processing routes. Recipe input/output identities are economy/automation content rather than semantic magic objects.

## Semantic disposition

`ZERO_SEMANTIC_CREATE_RECIPE_AUTOMATION / +0 strict`.

The provider has no fixed spell, glyph, ritual, rite, supernatural ability or equivalent player-action roster in the exact installed artifact.

## Clean-room boundary

The durable catalog retains hashes, counts, class/resource names and recipe-type classification required for denominator work. No third-party JAR bytes, source implementation bodies or assets are committed.
