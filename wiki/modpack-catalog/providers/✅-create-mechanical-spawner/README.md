# Create: Mechanical Spawner — 1.3.2-6.0.10

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_KINETIC_MOB_SPAWN_INFRA / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#147**;
- JAR: `create_mechanical_spawner-1.21.1-1.3.2-6.0.10.jar`;
- mod id: `create_mechanical_spawner`;
- filename/publisher version: `1.3.2-6.0.10`;
- embedded/runtime metadata recorded by the sibling: `1.3.1-6.0.10` (stale divergence preserved);
- physical SHA-1: `d9a5a2ee44238e4a90f70057ba9ec8414594fe24`.

Create: Mechanical Spawner is cross-domain because it materializes mobs — including an exact Wither recipe — but exact inspection is required before treating machine-driven entity generation as a magical summoning action.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#534** audits CurseForge project/file `821828 / 8418593` and hard-gates the publisher artifact against the physical fingerprint.

- audit HEAD: `f0af3036c0febe075c7aeaaba57ab911bd142074`;
- exact-artifact run: `37016899558` — **SUCCESS**;
- evidence artifact: `11231435071`;
- evidence digest: `sha256:7853217a8c1ad26fb8d345c5d9297bec29dc4abb3824afd0d882876c28c0b7a8`;
- publisher SHA-1: `d9a5a2ee44238e4a90f70057ba9ec8414594fe24`;
- publisher SHA-256: `f963b0a4e450484b36ec0b5d529fa7f32527dcc60ec93261ceef5c056f0a9134`;
- bytes: `1,215,649`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-1.3.2-ARTIFACT-AUDIT.md`](EXACT-1.3.2-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact artifact contains:

- **507** archive entries;
- **52** classes;
- **455** non-class resources;
- **116** `data/create_mechanical_spawner/**` paths;
- **97** provider recipe JSONs.

Archive keyword inventory closes:

`spell=0 · magic=0 · ritual=0 · ability=0 · mana=0 · arcane=0 · glyph=0 · summon=0 · soul=0`

Spawn-related resources are abundant by design and were therefore audited structurally rather than treated as magic from naming.

## Exact spawner recipe surface — 28 machine recipes

The current artifact packages **28 `create_mechanical_spawner:spawner` recipes**:

- **27** recipes with a concrete mob output;
- **1** random biome-dependent output recipe;
- **28** corresponding spawn-fluid mixing recipes.

The exact concrete roster includes passive mobs, hostile mobs and one Wither recipe. The Wither recipe consumes provider `spawn_fluid_wither`, has a machine processing time, outputs `minecraft:wither` and defines provider custom-loot settlement.

These are **data-driven processing recipes of the Mechanical Spawner**, not 28 player-cast summoning identities.

## No player-cast surface

All 52 provider classes were signature-scanned for the catalog player-action set:

`use · useOn · useWithoutItem · releaseUsing · onUseTick · finishUsingItem · interactLivingEntity · hurtEnemy · inventoryTick · onArmorTick · onItemUseFirst`

Result: **zero provider overrides**.

`SpawnerBlockEntity` is a Create kinetic block entity using provider recipe requirements, a fluid tank, dynamic cycle behavior and spawn-point configuration. Entity creation is the machine settlement after its kinetic/recipe conditions are met.

Player interaction with Create-style configuration/scroll-value behavior configures the machine; it does not constitute an independent supernatural action identity.

## Loot Collector / custom loot

The provider also owns Loot Collector infrastructure and allows a spawn recipe to supply custom loot. In the exact default data, the Wither recipe is the only spawner recipe with custom loot.

Custom-loot settlement is machine/loot infrastructure and is not counted as a spell or ritual.

## KubeJS surface

The JAR contains KubeJS recipe schema/support for adding/removing Mechanical Spawner recipes. This mutates the machine recipe set; it does not create a provider-owned player spell registry.

Arbitrary deployed scripts may change the mob/economy recipe roster, but that does not reopen the provider's semantic-magic denominator under the current metric.

Detailed classification: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Authority boundary

Create: Mechanical Spawner remains authority for spawner recipes, spawn-fluid requirements, cadence, entity materialization, spawn position, random-biome selection, custom loot, Loot Collector behavior and KubeJS recipe integration. Create/Mechanicals infrastructure remains authority for kinetics/stress and machine-cycle mechanics.

Black Arcana records the semantic classification only and must not replay entity spawn or loot settlement.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_KINETIC_MOB_SPAWN_INFRA`.**

Strict semantic delta: **+0**.
